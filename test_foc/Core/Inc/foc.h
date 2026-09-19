/**
  ******************************************************************************
  * @file    foc.h
  * @brief   FOC (Field Oriented Control) module cho dong co BLDC 4015
  *          Encoder MT6701 (14-bit SSI) + SimpleFOC Mini v2 (DRV8313)
  *          Kien truc module tach biet:
  *            - Encoder_MT6701_t: chua toan bo du lieu raw va goc xu ly
  *            - Motor_BLDC_t:     chua thong so dong co va bo dieu khien van toc
  *            - FOC_System_t:     he thong FOC tong hop
  ******************************************************************************
  */
#ifndef __FOC_H
#define __FOC_H

#ifdef __cplusplus
extern "C" {
#endif

#include "main.h"
#include <stdint.h>

/* ======================== Hang so toan hoc & phan cung ======================== */
#define FOC_2PI              6.28318530718f
#define FOC_PI               3.14159265359f
#define FOC_SQRT3            1.73205080757f
#define MT6701_CPR           16384          /* 14-bit = 2^14 counts/vong */

/* ======================== Bo dieu khien PID ======================== */
typedef struct {
    float Kp;                /* He so ti le (Proportional) */
    float Ki;                /* He so tich phan (Integral) */
    float Kd;                /* He so vi phan (Derivative) */
    float integral;          /* Gia tri tich phan tich luy */
    float prev_error;        /* Sai so chu ky truoc (tinh vi phan) */
    float output_limit;      /* Gioi han bien do dau ra tuyet doi */
    float integral_limit;    /* Gioi han chong bao hoa tich phan (anti-windup) */
} PID_Controller_t;

void  PID_Init(PID_Controller_t *pid, float Kp, float Ki, float Kd, float limit);
float PID_Update(PID_Controller_t *pid, float error, float dt);
void  PID_Reset(PID_Controller_t *pid);

/* ======================== Che do hoat dong ======================== */
typedef enum {
    FOC_MODE_DISABLED = 0,   /* Tat dong co, PWM = 0 */
    FOC_MODE_OPENLOOP,       /* Quay Open-Loop (khong can encoder) - de test */
    FOC_MODE_CALIBRATING,    /* Dang trong qua trinh can chinh (calibrate) */
    FOC_MODE_VELOCITY,       /* Dieu khien van toc kin (Closed-Loop FOC Velocity) */
    FOC_MODE_TORQUE          /* Dieu khien Uq truc tiep khong qua PID (Closed-Loop FOC Torque) */
} FOC_Mode_t;

/* ======================== Struct Du lieu Encoder MT6701 ======================== */
typedef struct {
    /* --- Du lieu tho (RAW) tu giao tiep SSI --- */
    uint16_t raw_angle;             /* Goc tho 14-bit: 0 -> 16383 (CPR = 16384) */
    uint8_t  status_mgh;            /* Bit trang thai: Tu truong qua manh (Magnetic High) */
    uint8_t  status_mgl;            /* Bit trang thai: Tu truong qua yeu (Magnetic Low) */
    float    raw_rad;               /* Goc tho chuyen doi sang radian [0, 2*PI) */

    /* --- Du lieu goc da xu ly --- */
    float    mechanical_angle;      /* Goc co hoc lien tuc (rad), tich luy multi-turn */
    float    electrical_angle;      /* Goc dien rotor hien tai (rad, [0, 2*PI)) */
    float    velocity;              /* Van toc thuc te da qua bo loc LPF (rad/s) */

    /* --- Thong so can chinh & theo doi --- */
    int8_t   direction;             /* +1 (CW) hoac -1 (CCW) - tu tinh khi calib */
    float    zero_electrical_offset;/* Offset goc dien tai vi tri Pha A (rad) */
    float    filter_Tf;             /* Hang so thoi gian bo loc van toc (s), mac dinh 15ms */

    /* --- Noi bo --- */
    float    prev_raw_rad;          /* Goc tho vong truoc (tinh d_angle) */
    uint32_t timestamp_prev;        /* Timestamp truoc (ms) */
    uint8_t  initialized;           /* 1 = Da khoi tao moc goc */
} Encoder_MT6701_t;

/* ======================== Struct Thong so Dong co BLDC ======================== */
typedef struct {
    /* --- Thong so phan cung dong co --- */
    uint8_t  pole_pairs;            /* So cap cuc (11 cho dong co BLDC 4015) */
    float    voltage_supply;        /* Dien ap nguon cap VM (V), vd: 12.0V */
    float    voltage_limit;         /* Gioi han dien ap Uq toi da (V), vd: 3.5V */

    /* --- Che do hoat dong --- */
    FOC_Mode_t mode;                /* FOC_MODE_DISABLED, OPENLOOP, VELOCITY, TORQUE */

    /* --- Dieu khien van toc / moment FOC (Closed-Loop) --- */
    float    target_velocity;       /* Van toc muc tieu (rad/s) */
    float    target_Uq;             /* Dien ap Uq muc tieu khi chay Torque Mode (V) */
    float    Uq;                    /* Dien ap truc q tao moment quay (V) */
    float    Ud;                    /* Dien ap truc d (V, mac dinh = 0) */
    PID_Controller_t pid_velocity;  /* Bo dieu khien PID van toc -> Uq */

    /* --- Thong so chay Open-Loop --- */
    float    openloop_angle;        /* Goc dien khi chay open-loop (rad) */
    float    openloop_voltage;      /* Dien ap Uq khi test open-loop (V) */
    float    openloop_velocity;     /* Toc do quay open-loop (rad/s) */

    /* --- Trang thai Calibrate --- */
    uint8_t  is_calibrated;         /* 1 = Da calibrate xong */
    uint8_t  calib_success;         /* 1 = Calibrate thanh cong */
    float    pp_check_result;       /* Ti so pole pairs thuc te do duoc */

    /* --- Thoi gian --- */
    uint32_t tick_prev;             /* Timestamp vong lap truoc (ms) */
} Motor_BLDC_t;

/* ======================== Struct Tong the He thong FOC ======================== */
typedef struct {
    Motor_BLDC_t     motor;         /* Toan bo bien va thong so dong co */
    Encoder_MT6701_t encoder;       /* Toan bo du lieu raw va goc encoder */
} FOC_System_t;

/* ======================== Cac ham API giao tiep ======================== */

/**
 * @brief Doc gia tri tho 14-bit tu MT6701 qua SSI khong gay block/overrun
 * @param enc Con tro toi struct encoder (co the NULL neu chi muon doc raw)
 * @return Goc tho 14-bit (0 - 16383)
 */
uint16_t MT6701_SPI_ReadRaw(Encoder_MT6701_t *enc);

/**
 * @brief Cap nhat du lieu encoder (raw -> mechanical rad -> velocity -> electrical angle)
 */
void Encoder_Update(Encoder_MT6701_t *enc, uint8_t pole_pairs);

/**
 * @brief Khoi tao toan bo he thong FOC
 */
void FOC_Init(FOC_System_t *foc, uint8_t pole_pairs, float voltage_supply, float voltage_limit);

/**
 * @brief Tu dong can chinh FOC: tim chieu encoder va offset goc dien Pha A
 */
void FOC_Calibrate(FOC_System_t *foc);

/**
 * @brief Dat van toc muc tieu (chay closed-loop FOC velocity)
 * @param target_velocity Van toc rad/s (duong = thuan, am = nguoc)
 */
void FOC_SetVelocity(FOC_System_t *foc, float target_velocity);

/**
 * @brief Dat dien ap Uq muc tieu (chay closed-loop FOC torque/voltage khong qua PID)
 * @param target_Uq Dien ap Uq (V, duong = thuan, am = nguoc)
 */
void FOC_SetTorque(FOC_System_t *foc, float target_Uq);

/**
 * @brief Chay open-loop (dung de test phan cung khong can encoder)
 */
void FOC_RunOpenLoop(FOC_System_t *foc, float voltage, float velocity);

/**
 * @brief Vong lap FOC - Goi ham nay trong while(1) moi 1ms (~1kHz)
 */
void FOC_Loop(FOC_System_t *foc);

/**
 * @brief Tat dau ra dong co (dat duty cycle ve 0)
 */
void FOC_Disable(FOC_System_t *foc);

/**
 * @brief Tinh chinh he so PID van toc
 */
void FOC_SetVelocityPID(FOC_System_t *foc, float Kp, float Ki, float Kd);

#ifdef __cplusplus
}
#endif

#endif /* __FOC_H */
