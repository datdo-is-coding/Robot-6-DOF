/**
  ******************************************************************************
  * @file    foc.c
  * @brief   FOC (Field Oriented Control) - Dieu khien dong co BLDC bang dien ap
  *
  *          Cau truc du lieu da duoc dong goi rieng biet:
  *            - Encoder_MT6701_t: Du lieu tho (RAW SSI) va goc xu ly
  *            - Motor_BLDC_t:     Thong so dong co va bo dieu khien PID van toc
  *            - FOC_System_t:     He thong FOC tong hop
  *
  *          Vong dieu khien (Voltage Mode - KHONG CAN CURRENT SENSING):
  *            [Target Velocity] -> PID Velocity -> [Uq] -> Inverse Park/Clarke SVPWM
  *
  * @author  Generated for STM32G474 + BLDC 4015 + MT6701 + SimpleFOC Mini v2
  * @note    SimpleFOC Mini v2 (DRV8313) KHONG co dien tro shunt do dong,
  *          nen chi ho tro dieu khien bang dien ap (voltage torque control).
  ******************************************************************************
  */

#include "foc.h"
#include "spi.h"   /* extern SPI_HandleTypeDef hspi1 */
#include "tim.h"   /* extern TIM_HandleTypeDef htim1 */
#include <math.h>

/* ======================== Private defines ======================== */
#define TIM1_ARR  3999  /* Phai khop voi CubeMX: Counter Period */

/* ======================== Fast Sin/Cos Lookup Table ======================== */
/* 512 diem, phu toan bo 1 chu ky [0, 2*PI)
 * Tranh dung cosf()/sinf() trong vong lap 1kHz vi co the rat cham
 * tren Cortex-M4 neu compiler khong bat FPU hard-float dung cach.
 * Lookup table dam bao thoi gian chay co dinh ~0.5us bat ke compiler flags.
 */
#define SINCOS_TABLE_SIZE  512
#define SINCOS_INDEX_MASK  (SINCOS_TABLE_SIZE - 1)  /* 0x1FF */
/* Nhan goc (rad) voi he so nay de ra index float */
#define SINCOS_RAD_TO_IDX  (SINCOS_TABLE_SIZE / FOC_2PI)  /* ~81.487 */

static float _sin_table[SINCOS_TABLE_SIZE];
static uint8_t _sincos_initialized = 0;

/**
 * @brief Khoi tao bang sin lookup 1 lan duy nhat
 */
static void _SinCos_Init(void)
{
    if (_sincos_initialized) return;
    for (int i = 0; i < SINCOS_TABLE_SIZE; i++)
    {
        _sin_table[i] = sinf((float)i * FOC_2PI / (float)SINCOS_TABLE_SIZE);
    }
    _sincos_initialized = 1;
}

/**
 * @brief Tra bang sin voi noi suy tuyen tinh, do chinh xac ~14 bit
 * @param angle Goc bat ky (rad), khong can normalize truoc
 */
static float _fast_sin(float angle)
{
    float idx_f = angle * SINCOS_RAD_TO_IDX;
    /* FIX: Dung floorf thay vi (int) de xu ly goc am dung.
     * (int) truncate ve 0 (vd: (int)(-0.3) = 0), con floorf lam tron xuong (vd: floorf(-0.3) = -1).
     * Khi dung (int), frac co the AM -> noi suy sai -> sin/cos sai -> motor bi ghim dien.
     */
    int idx = (int)floorf(idx_f);
    float frac = idx_f - (float)idx;   /* Luon >= 0 nho floorf */

    /* Wrap index ve [0, 511] - dung modulo an toan cho so am */
    int i0 = ((idx % SINCOS_TABLE_SIZE) + SINCOS_TABLE_SIZE) % SINCOS_TABLE_SIZE;
    int i1 = (i0 + 1) & SINCOS_INDEX_MASK;

    /* Noi suy tuyen tinh */
    return _sin_table[i0] + frac * (_sin_table[i1] - _sin_table[i0]);
}

/**
 * @brief Tra bang cos = sin(angle + PI/2)
 */
static float _fast_cos(float angle)
{
    return _fast_sin(angle + FOC_PI * 0.5f);
}

/* ======================== Private helpers ======================== */

/**
 * @brief Gioi han gia tri float trong khoang [min, max]
 */
static inline float _constrainf(float val, float min_val, float max_val)
{
    if (val < min_val) return min_val;
    if (val > max_val) return max_val;
    return val;
}

/**
 * @brief Chuan hoa goc ve khoang [0, 2*PI)
 */
static inline float _normalizeAngle(float angle)
{
    float a = fmodf(angle, FOC_2PI);
    return (a >= 0.0f) ? a : (a + FOC_2PI);
}

/* ================================================================
 *  SPI - Doc MT6701 RAW 14-bit qua SSI
 *
 *  QUAN TRONG: SPI1 duoc cau hinh RX-Only mode (SPI_DIRECTION_2LINES_RXONLY).
 *  Trong che do nay, SPI tu dong tao clock lien tuc khi SPE=1.
 *  Neu khong disable SPI sau moi lan doc, overrun se tich luy
 *  va HAL_SPI_Receive se bi treo/tra du lieu sai.
 *
 *  Giai phap: Disable SPI (SPE=0) sau moi lan doc xong,
 *  va re-enable (SPE=1) ngay truoc lan doc tiep theo.
 *
 *  Giao thuc SSI: Keo CSN LOW -> tao 16 clock -> nhan 16-bit
 *  Data format: [D13..D0][MGH][MGL]
 *  Bit[15:2] = 14-bit goc, Bit[1] = MGH, Bit[0] = MGL
 * ================================================================ */
uint16_t MT6701_SPI_ReadRaw(Encoder_MT6701_t *enc)
{
    uint16_t rx_data = 0;
    HAL_StatusTypeDef status = HAL_ERROR;

    for (int retry = 0; retry < 3; retry++)
    {
        /* === FIX: Clear moi trang thai truoc khi doc === */
        /* Disable SPI truoc de dam bao khong con clock cu dang chay */
        __HAL_SPI_DISABLE(&hspi1);

        /* Flush RX FIFO: doc het du lieu con lai trong buffer */
        while (__HAL_SPI_GET_FLAG(&hspi1, SPI_FLAG_RXNE))
        {
            (void)hspi1.Instance->DR;
        }
        /* Clear Overrun flag (doc DR roi doc SR) */
        __HAL_SPI_CLEAR_OVRFLAG(&hspi1);

        /* Reset HAL state ve READY de HAL_SPI_Receive chap nhan goi tiep */
        hspi1.State = HAL_SPI_STATE_READY;
        hspi1.ErrorCode = HAL_SPI_ERROR_NONE;

        /* Keo CSN LOW de MT6701 chuan bi du lieu */
        HAL_GPIO_WritePin(CSN_GPIO_Port, CSN_Pin, GPIO_PIN_RESET);
        /* Delay ngan cho MT6701 (t_clk_delay >= 100ns) */
        for (volatile int d = 0; d < 20; d++);

        /* HAL_SPI_Receive se tu dong enable SPI (SPE=1) va tao clock */
        status = HAL_SPI_Receive(&hspi1, (uint8_t *)&rx_data, 1, 2);

        /* === FIX: Disable SPI NGAY LAP TUC sau khi nhan xong === */
        /* Dieu nay DUNG clock SPI, tranh overrun tich luy */
        __HAL_SPI_DISABLE(&hspi1);

        /* Keo CSN HIGH de MT6701 chot du lieu cho lan doc tiep */
        HAL_GPIO_WritePin(CSN_GPIO_Port, CSN_Pin, GPIO_PIN_SET);
        /* Delay CSN high (t_timeout >= 2us) */
        for (volatile int d = 0; d < 40; d++);

        if (status == HAL_OK)
        {
            break;
        }
    }

    if (status == HAL_OK)
    {
        uint16_t raw = (rx_data >> 2) & 0x3FFF;
        if (enc != NULL)
        {
            enc->raw_angle  = raw;
            enc->status_mgh = (rx_data >> 1) & 0x01;
            enc->status_mgl = rx_data & 0x01;
            enc->raw_rad    = (float)raw * (FOC_2PI / (float)MT6701_CPR);
        }
        return raw;
    }

    /* Neu doc loi: TUYET DOI KHONG ghi 0 vao raw_rad, giu nguyen gia tri hop le truoc do */
    return (enc != NULL) ? enc->raw_angle : 0;
}

/* ================================================================
 *  SVPWM - Xuat xung PWM 3 pha tu (Uq, Ud, goc_dien)
 *  Su dung bien doi nguoc Park + Clarke
 *  Dung fast sin/cos lookup table thay vi cosf/sinf de dam bao
 *  thoi gian chay co dinh, tranh treo khi compiler thieu FPU flags.
 * ================================================================ */
static void _FOC_WritePWM(float Uq, float Ud, float angle_el, float v_supply)
{
    /* FIX: Dam bao angle_el luon trong [0, 2*PI) truoc khi tinh sin/cos
     * Tranh truong hop goc am lot vao _fast_sin/_fast_cos */
    angle_el = _normalizeAngle(angle_el);

    /* Su dung fast lookup table thay vi cosf/sinf */
    float cos_a = _fast_cos(angle_el);
    float sin_a = _fast_sin(angle_el);

    /* Inverse Park: (Ud, Uq) -> (U_alpha, U_beta) */
    float U_alpha = cos_a * Ud - sin_a * Uq;
    float U_beta  = sin_a * Ud + cos_a * Uq;

    /* Inverse Clarke: (U_alpha, U_beta) -> (Ua, Ub, Uc) */
    float Ua = U_alpha;
    float Ub = (-U_alpha + FOC_SQRT3 * U_beta) * 0.5f;
    float Uc = (-U_alpha - FOC_SQRT3 * U_beta) * 0.5f;

    /* Chuyen sang duty cycle [0.0 .. 1.0], offset trung tam = 0.5 */
    float duty_a = _constrainf((Ua / v_supply) + 0.5f, 0.0f, 1.0f);
    float duty_b = _constrainf((Ub / v_supply) + 0.5f, 0.0f, 1.0f);
    float duty_c = _constrainf((Uc / v_supply) + 0.5f, 0.0f, 1.0f);

    /* Ghi vao thanh ghi so sanh TIM1 */
    __HAL_TIM_SET_COMPARE(&htim1, TIM_CHANNEL_1, (uint32_t)(duty_a * TIM1_ARR));
    __HAL_TIM_SET_COMPARE(&htim1, TIM_CHANNEL_2, (uint32_t)(duty_b * TIM1_ARR));
    __HAL_TIM_SET_COMPARE(&htim1, TIM_CHANNEL_3, (uint32_t)(duty_c * TIM1_ARR));
}

/* ================================================================
 *  PID Controller
 * ================================================================ */
void PID_Init(PID_Controller_t *pid, float Kp, float Ki, float Kd, float limit)
{
    pid->Kp = Kp;
    pid->Ki = Ki;
    pid->Kd = Kd;
    pid->integral = 0.0f;
    pid->prev_error = 0.0f;
    pid->output_limit = limit;
    pid->integral_limit = limit;
}

float PID_Update(PID_Controller_t *pid, float error, float dt)
{
    if (dt <= 0.0f) return 0.0f;

    /* P term */
    float p_term = pid->Kp * error;

    /* I term voi anti-windup clamp */
    pid->integral += pid->Ki * error * dt;
    pid->integral = _constrainf(pid->integral, -pid->integral_limit, pid->integral_limit);

    /* D term */
    float d_term = pid->Kd * (error - pid->prev_error) / dt;
    pid->prev_error = error;

    /* Output */
    float output = p_term + pid->integral + d_term;
    return _constrainf(output, -pid->output_limit, pid->output_limit);
}

void PID_Reset(PID_Controller_t *pid)
{
    pid->integral = 0.0f;
    pid->prev_error = 0.0f;
}

/* ================================================================
 *  Encoder MT6701 - Tracking goc va tinh van toc
 * ================================================================ */
void Encoder_Update(Encoder_MT6701_t *enc, uint8_t pole_pairs)
{
    /* 1. Doc raw qua SSI */
    MT6701_SPI_ReadRaw(enc);
    float raw_rad = enc->raw_rad;
    uint32_t now = HAL_GetTick();

    /* 2. Lan dau tien chay: khoi tao moc */
    if (!enc->initialized)
    {
        enc->prev_raw_rad = raw_rad;
        enc->timestamp_prev = now;
        enc->mechanical_angle = 0.0f;
        enc->velocity = 0.0f;
        enc->initialized = 1;

        float elec = (float)(enc->direction * pole_pairs) * raw_rad - enc->zero_electrical_offset;
        enc->electrical_angle = _normalizeAngle(elec);
        return;
    }

    /* 3. Tinh delta goc tren 1 vong (xu ly tran vong [-PI, PI]) */
    float d_angle = raw_rad - enc->prev_raw_rad;
    if (d_angle > FOC_PI)        d_angle -= FOC_2PI;
    else if (d_angle < -FOC_PI)  d_angle += FOC_2PI;

    /* LUON LUON cap nhat prev_raw_rad moi nhat: TUYET DOI KHONG dat trong if condition de tranh deadlock */
    enc->prev_raw_rad = raw_rad;

    /* Tich luy goc co hoc */
    enc->mechanical_angle += d_angle * (float)enc->direction;

    /* 4. Tinh van toc va loc thong thap LPF */
    float dt = (float)(now - enc->timestamp_prev) / 1000.0f;
    if (dt >= 0.001f)
    {
        float vel_raw = (d_angle * (float)enc->direction) / dt;
        /* Clamp vel_raw de tranh glitch spike bat thuong do nhieu SPI lam vot PID */
        if (vel_raw > 150.0f) vel_raw = 150.0f;
        else if (vel_raw < -150.0f) vel_raw = -150.0f;

        float alpha = dt / (enc->filter_Tf + dt);
        enc->velocity = alpha * vel_raw + (1.0f - alpha) * enc->velocity;
        enc->timestamp_prev = now;
    }

    /* 5. Goc dien rotor tuyet doi: tinh truc tiep tu raw_rad moi nhat */
    float elec = (float)(enc->direction * pole_pairs) * raw_rad - enc->zero_electrical_offset;
    enc->electrical_angle = _normalizeAngle(elec);
}

/* ================================================================
 *  Khoi tao He thong FOC
 * ================================================================ */
void FOC_Init(FOC_System_t *foc, uint8_t pole_pairs, float voltage_supply, float voltage_limit)
{
    /* 0. Khoi tao bang sin/cos lookup (1 lan duy nhat) */
    _SinCos_Init();

    /* 1. Thong so dong co */
    foc->motor.pole_pairs = pole_pairs;
    foc->motor.voltage_supply = voltage_supply;
    foc->motor.voltage_limit = voltage_limit;
    foc->motor.mode = FOC_MODE_DISABLED;
    foc->motor.target_velocity = 0.0f;
    foc->motor.target_Uq = 1.0f;
    foc->motor.Uq = 0.0f;
    foc->motor.Ud = 0.0f;
    foc->motor.is_calibrated = 0;
    foc->motor.calib_success = 0;
    foc->motor.pp_check_result = 0.0f;
    foc->motor.tick_prev = 0;

    /* Open-loop defaults */
    foc->motor.openloop_angle = 0.0f;
    foc->motor.openloop_voltage = 2.0f;
    foc->motor.openloop_velocity = 3.0f;

    /* 2. Thong so encoder */
    foc->encoder.raw_angle = 0;
    foc->encoder.status_mgh = 0;
    foc->encoder.status_mgl = 0;
    foc->encoder.raw_rad = 0.0f;
    foc->encoder.mechanical_angle = 0.0f;
    foc->encoder.electrical_angle = 0.0f;
    foc->encoder.velocity = 0.0f;
    foc->encoder.prev_raw_rad = 0.0f;
    foc->encoder.zero_electrical_offset = 0.0f;
    foc->encoder.filter_Tf = 0.015f;    /* Bo loc van toc Tf = 15ms */
    foc->encoder.direction = 1;         /* Mac dinh CW */
    foc->encoder.timestamp_prev = 0;
    foc->encoder.initialized = 0;

    /* 3. PID Van toc: Kp = 0.20f, Ki = 2.0f, Kd = 0 (phu hop voi BLDC 4015 gimbal) */
    PID_Init(&foc->motor.pid_velocity, 0.20f, 2.0f, 0.0f, voltage_limit);
}

/**
 * @brief Tinh trung binh 10 mau goc tren vong tron [0, 2*PI)
 *        Su dung vector (sin, cos) triet tieu hoan toan loi nhay tai ranh gioi 0 <-> 2*PI
 */
static float _averageAngle10(Encoder_MT6701_t *enc)
{
    float sum_sin = 0.0f;
    float sum_cos = 0.0f;
    for (int k = 0; k < 10; k++)
    {
        MT6701_SPI_ReadRaw(enc);
        sum_sin += sinf(enc->raw_rad);
        sum_cos += cosf(enc->raw_rad);
        HAL_Delay(2);
    }
    return _normalizeAngle(atan2f(sum_sin, sum_cos));
}

/* ================================================================
 *  Tu dong can chinh FOC (Calibrate chieu encoder va offset goc dien)
 *  Theo chuan SimpleFOC alignSensor():
 *    1. Thang hang Pha A (3*PI/2)
 *    2. Quet 1 chu ky dien ve phia truoc (400 buoc x 2ms = 800ms)
 *    3. Quet 1 chu ky dien nguoc lai ve dung vi tri Pha A ban dau
 *    4. Tinh toan direction, pole pairs va zero_electrical_offset
 * ================================================================ */
void FOC_Calibrate(FOC_System_t *foc)
{
    foc->motor.mode = FOC_MODE_CALIBRATING;
    foc->motor.is_calibrated = 0;
    foc->motor.calib_success = 0;

    /* Dien ap calibrate: 2.0V giup dong co 4015 vuot cogging va khong nong driver */
    float cal_v = 2.0f;
    if (cal_v > foc->motor.voltage_limit) cal_v = foc->motor.voltage_limit;

    float start_angle = 1.5f * FOC_PI; /* 3*PI/2: vector tu truong nam tai Pha A */

    /* ===========================================================
     *  BUOC 1: Dinh huong rotor tai Pha A (Ramp ap tu tu tranh shock)
     * =========================================================== */
    for (int i = 1; i <= 30; i++)
    {
        float v = cal_v * (float)i / 30.0f;
        _FOC_WritePWM(v, 0.0f, start_angle, foc->motor.voltage_supply);
        HAL_Delay(10);
    }
    HAL_Delay(500);

    /* Doc goc co hoc ban dau sau khi da thang hang vao Pha A (loc circular) */
    float start_raw = _averageAngle10(&foc->encoder);

    /* ===========================================================
     *  BUOC 2: Quet 1 chu ky dien ve phia truoc (2*PI electrical)
     *  400 buoc x 2ms = 800ms giup rotor theo sat tu truong khong bi slip
     * =========================================================== */
    int steps = 400;
    for (int i = 0; i <= steps; i++)
    {
        float angle = start_angle + FOC_2PI * (float)i / (float)steps;
        _FOC_WritePWM(cal_v, 0.0f, angle, foc->motor.voltage_supply);
        HAL_Delay(2);
    }
    HAL_Delay(100);

    /* Doc goc co hoc tai diem cuc dai chu ky quay thuan */
    float mid_raw = _averageAngle10(&foc->encoder);

    /* ===========================================================
     *  BUOC 3: Quet 1 chu ky dien nguoc lai ve vi tri start_angle ban dau
     *  Giup rotor quay tro ve dung vi tri Pha A ban dau, khong bao gio bi truot pole
     * =========================================================== */
    for (int i = steps; i >= 0; i--)
    {
        float angle = start_angle + FOC_2PI * (float)i / (float)steps;
        _FOC_WritePWM(cal_v, 0.0f, angle, foc->motor.voltage_supply);
        HAL_Delay(2);
    }
    HAL_Delay(200);

    /* Tinh do dich chuyen goc co hoc khi di tu start -> mid (xu ly tran vong [-PI, PI]) */
    float moved = mid_raw - start_raw;
    if (moved > FOC_PI)        moved -= FOC_2PI;
    else if (moved < -FOC_PI)  moved += FOC_2PI;

    /* Xac dinh chieu quay encoder:
     * Stator quay ve phia duong (angle tang).
     * Neu encoder doc tang (moved > 0) -> direction = +1 (CW)
     * Neu encoder doc giam (moved < 0) -> direction = -1 (CCW)
     */
    if (moved > 0.02f)
    {
        foc->encoder.direction = 1;
    }
    else if (moved < -0.02f)
    {
        foc->encoder.direction = -1;
    }
    else
    {
        /* Dong co khong quay duoc (do ket co hoac ap cal_v qua thap) */
        foc->encoder.direction = 1;
        foc->motor.calib_success = 0;
        foc->motor.is_calibrated = 0;
        foc->motor.mode = FOC_MODE_DISABLED;  /* FIX: Ve DISABLED thay vi de CALIBRATING */
        _FOC_WritePWM(0.0f, 0.0f, 0.0f, foc->motor.voltage_supply);
        return;
    }

    /* Kiem tra ti so pole pairs thuc te: 2*PI / |moved| */
    float moved_abs = fabsf(moved);
    foc->motor.pp_check_result = FOC_2PI / moved_abs;
    if (fabsf(foc->motor.pp_check_result - (float)foc->motor.pole_pairs) < 4.0f)
    {
        foc->motor.calib_success = 1;
    }
    else
    {
        foc->motor.calib_success = 0;
    }

    /* ===========================================================
     *  BUOC 4: Giu tai Pha A va do chinh xac Zero Electrical Offset
     * =========================================================== */
    _FOC_WritePWM(cal_v, 0.0f, start_angle, foc->motor.voltage_supply);
    HAL_Delay(300);

    /* Doc goc Pha A chuan xac bang loc circular */
    float raw_rad = _averageAngle10(&foc->encoder);

    /* Tinh zero_electrical_offset */
    float elec_zero = (float)(foc->encoder.direction * foc->motor.pole_pairs) * raw_rad;
    foc->encoder.zero_electrical_offset = _normalizeAngle(elec_zero);

    /* ===========================================================
     *  BUOC 5: Ngat ap, reset bo loc va PID
     * =========================================================== */
    _FOC_WritePWM(0.0f, 0.0f, 0.0f, foc->motor.voltage_supply);
    HAL_Delay(50);

    /* Reset encoder tracking */
    foc->encoder.initialized = 0;
    Encoder_Update(&foc->encoder, foc->motor.pole_pairs);

    /* Reset PID */
    PID_Reset(&foc->motor.pid_velocity);

    foc->motor.is_calibrated = 1;

    /* FIX: Chi chuyen sang VELOCITY neu calibrate THANH CONG.
     * Neu calib_success = 0, giu o DISABLED de tranh motor giat.
     */
    if (foc->motor.calib_success)
    {
        foc->motor.mode = FOC_MODE_VELOCITY;
    }
    else
    {
        foc->motor.mode = FOC_MODE_DISABLED;
    }

    foc->motor.tick_prev = HAL_GetTick();
}

/* ================================================================
 *  Dat van toc muc tieu (Closed-Loop FOC Velocity)
 * ================================================================ */
void FOC_SetVelocity(FOC_System_t *foc, float target_velocity)
{
    if (foc->motor.mode != FOC_MODE_VELOCITY)
    {
        foc->motor.mode = FOC_MODE_VELOCITY;
        PID_Reset(&foc->motor.pid_velocity);
    }
    foc->motor.target_velocity = target_velocity;
}

/* ================================================================
 *  Dat moment/dien ap Uq truc tiep (Closed-Loop FOC Torque/Voltage)
 * ================================================================ */
void FOC_SetTorque(FOC_System_t *foc, float target_Uq)
{
    foc->motor.mode = FOC_MODE_TORQUE;
    foc->motor.target_Uq = target_Uq;
}

/* ================================================================
 *  Chay Open-Loop (de test phan cung khong can encoder)
 * ================================================================ */
void FOC_RunOpenLoop(FOC_System_t *foc, float voltage, float velocity)
{
    foc->motor.mode = FOC_MODE_OPENLOOP;
    foc->motor.openloop_voltage = _constrainf(voltage, 0.0f, foc->motor.voltage_limit);
    foc->motor.openloop_velocity = velocity;
}

/* ================================================================
 *  Vong lap FOC chinh - Goi moi 1ms (~1kHz)
 * ================================================================ */
void FOC_Loop(FOC_System_t *foc)
{
    if (foc->motor.mode == FOC_MODE_DISABLED || foc->motor.mode == FOC_MODE_CALIBRATING)
        return;

    /* Tinh dt */
    uint32_t now = HAL_GetTick();
    float dt = (float)(now - foc->motor.tick_prev) / 1000.0f;
    foc->motor.tick_prev = now;
    if (dt <= 0.0f || dt > 0.1f) dt = 0.001f;

    /* 1. Luon doc va cap nhat cam bien encoder */
    Encoder_Update(&foc->encoder, foc->motor.pole_pairs);

    /* 2. Xu ly theo che do */
    if (foc->motor.mode == FOC_MODE_OPENLOOP)
    {
        /* FIX: Goc dien open-loop: openloop_velocity la van toc dien (electrical rad/s)
         * KHONG nhan them pole_pairs o day. Neu muon dat van toc co hoc, nguoi dung
         * tu nhan pole_pairs khi truyen vao openloop_velocity.
         */
        foc->motor.openloop_angle += foc->motor.openloop_velocity * dt;
        foc->motor.openloop_angle = _normalizeAngle(foc->motor.openloop_angle);

        foc->motor.Uq = foc->motor.openloop_voltage;
        foc->motor.Ud = 0.0f;
        _FOC_WritePWM(foc->motor.Uq, foc->motor.Ud, foc->motor.openloop_angle,
                      foc->motor.voltage_supply);
        return;
    }

    if (foc->motor.mode == FOC_MODE_TORQUE)
    {
        if (!foc->motor.is_calibrated) return;

        foc->motor.Uq = _constrainf(foc->motor.target_Uq, -foc->motor.voltage_limit, foc->motor.voltage_limit);
        foc->motor.Ud = 0.0f;

        /* SVPWM theo goc dien rotor do duoc */
        _FOC_WritePWM(foc->motor.Uq, foc->motor.Ud, foc->encoder.electrical_angle,
                      foc->motor.voltage_supply);
        return;
    }

    if (foc->motor.mode == FOC_MODE_VELOCITY)
    {
        if (!foc->motor.is_calibrated) return;

        /* Sai so van toc = target - feedback */
        float vel_error = foc->motor.target_velocity - foc->encoder.velocity;

        /* PID tinh dien ap Uq muc tieu */
        float target_Uq = PID_Update(&foc->motor.pid_velocity, vel_error, dt);
        target_Uq = _constrainf(target_Uq, -foc->motor.voltage_limit, foc->motor.voltage_limit);

        /* Ramp dien ap em ai (slew rate 15V/giay) tranh shock dong gay treo hoac giat cuc */
        float max_step = 15.0f * dt;
        float diff = target_Uq - foc->motor.Uq;
        if (diff > max_step) foc->motor.Uq += max_step;
        else if (diff < -max_step) foc->motor.Uq -= max_step;
        else foc->motor.Uq = target_Uq;

        foc->motor.Ud = 0.0f;

        /* SVPWM theo goc dien rotor do duoc */
        _FOC_WritePWM(foc->motor.Uq, foc->motor.Ud, foc->encoder.electrical_angle,
                      foc->motor.voltage_supply);
    }
}

/* ================================================================
 *  Tat dong co
 * ================================================================ */
void FOC_Disable(FOC_System_t *foc)
{
    foc->motor.mode = FOC_MODE_DISABLED;
    foc->motor.Uq = 0.0f;
    foc->motor.Ud = 0.0f;

    __HAL_TIM_SET_COMPARE(&htim1, TIM_CHANNEL_1, 0);
    __HAL_TIM_SET_COMPARE(&htim1, TIM_CHANNEL_2, 0);
    __HAL_TIM_SET_COMPARE(&htim1, TIM_CHANNEL_3, 0);

    PID_Reset(&foc->motor.pid_velocity);
}

/* ================================================================
 *  Tinh chinh PID van toc
 * ================================================================ */
void FOC_SetVelocityPID(FOC_System_t *foc, float Kp, float Ki, float Kd)
{
    foc->motor.pid_velocity.Kp = Kp;
    foc->motor.pid_velocity.Ki = Ki;
    foc->motor.pid_velocity.Kd = Kd;
    PID_Reset(&foc->motor.pid_velocity);
}
