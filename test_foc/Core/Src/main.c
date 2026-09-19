/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.c
  * @brief          : FOC Position Control - BLDC 4015 + MT6701 + SimpleFOC Mini v2
  *
  *   Thuat toan: Closed-loop FOC voi cascade PID
  *     [Target Position] -> PID Position -> [Target Velocity] -> PID Velocity -> [Uq] -> SVPWM
  *
  *   Cach su dung:
  *     1. Nap code, motor se tu dong calibrate (giat nhe ~3 giay)
  *     2. Sau calibrate, motor ghim giu tai vi tri hien tai
  *     3. Thay doi bien "cmd_target_position" trong Live Expressions de xoay motor
  *        Vi du: dat = 3.14 -> motor quay den 180 do roi giu
  *     4. Thay doi "cmd_max_velocity" de thay doi toc do di chuyen
  *
  ******************************************************************************
  */
/* USER CODE END Header */
/* Includes ------------------------------------------------------------------*/
#include "main.h"
#include "adc.h"
#include "spi.h"
#include "tim.h"
#include "gpio.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */
#include "foc.h"
#include <math.h>
/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */

/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */

/* ==================== THONG SO DONG CO ====================
 * BLDC 4015 gimbal: 11 cap cuc (22 nam cham)
 * Kiem tra: dem so nam cham tren rotor chia 2
 */
#define MOTOR_POLE_PAIRS    11

/* Dien ap nguon cap vao SimpleFOC Mini v2 (V) */
#define VOLTAGE_SUPPLY      12.0f

/* Gioi han Uq (V) - dong co gimbal nen de 2-4V */
#define VOLTAGE_LIMIT       3.5f

/* Van toc toi da mac dinh khi di chuyen (rad/s) */
#define DEFAULT_MAX_VELOCITY  10.0f

/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/

/* USER CODE BEGIN PV */

/* ===========================================================
 *  CHE DO HOAT DONG - Mac dinh khi reset chip: MODE 1 (FOC VELOCITY)
 *  Co the thay doi qua Live Expressions / Debugger bat cu luc nao.
 *
 *  cmd_mode = 1 : FOC VELOCITY (Closed-Loop toc do) - [MAC DINH]
 *                 Reset chip -> doi 1s -> tu calibrate -> quay FOC toc do cmd_target_velocity
 *  cmd_mode = 0 : OPEN-LOOP (khong can encoder)
 *                 Dung de test phan cung cong suat
 * =========================================================== */
volatile uint8_t cmd_mode = 1;              /* 0 = Open-Loop, 1 = FOC Velocity [MAC DINH], 2 = FOC Torque/Voltage */
volatile uint8_t cmd_recalibrate = 0;       /* Dat = 1 trong Live Expressions de calibrate lai */

/* VELOCITY CONTROL (mode 1) */
volatile float cmd_target_velocity = 5.0f;  /* Van toc muc tieu (rad/s). 5 rad/s ~ 48 RPM */

/* TORQUE / VOLTAGE CONTROL (mode 2 - Test FOC truc tiep khong qua PID) */
volatile float cmd_target_Uq = 1.5f;        /* Dien ap Uq (V) - dat 1.5V dong co se quay tron em */

/* OPEN-LOOP (mode 0) */
volatile float cmd_openloop_voltage  = 2.0f;  /* Dien ap Uq (V) */
volatile float cmd_openloop_velocity = 3.0f;  /* Toc do quay (rad/s) */

/* Ghi de chieu quay thu cong neu can (0 = auto theo calib, 1 = CW, -1 = CCW) */
volatile int8_t cmd_direction_override = 0;

/* ===========================================================
 *  HE THONG FOC TONG HOP (chua motor + encoder struct)
 *  Co the add truc tiep "foc" vao Live Expressions de xem toan bo struct!
 * =========================================================== */
FOC_System_t foc;

/* ===========================================================
 *  BIEN GIAM SAT NHANH - Xem trong STM32CubeIDE Live Expressions
 * =========================================================== */
volatile uint32_t dbg_heartbeat     = 0;      /* Tang lien tuc moi 1ms -> khang dinh 100% CPU khong treo */
volatile uint16_t dbg_raw_angle     = 0;      /* Encoder raw 14-bit: 0 - 16383 */
volatile uint8_t  dbg_status_mgh    = 0;      /* Bit MGH: Tu truong qua manh */
volatile uint8_t  dbg_status_mgl    = 0;      /* Bit MGL: Tu truong qua yeu */
volatile float    dbg_mech_angle    = 0.0f;   /* Goc co hoc multi-turn (rad) */
volatile float    dbg_elec_angle    = 0.0f;   /* Goc dien (rad, 0 -> 2*PI) */
volatile float    dbg_velocity      = 0.0f;   /* Van toc thuc te da loc (rad/s) */
volatile float    dbg_Uq            = 0.0f;   /* Dien ap Uq (V) */
volatile uint8_t  dbg_is_calibrated = 0;      /* 1 = Da calibrate */
volatile uint8_t  dbg_calib_ok      = 0;      /* 1 = Calibrate thanh cong */
volatile int8_t   dbg_direction     = 0;      /* Chieu encoder (+1 CW hoac -1 CCW) */
volatile float    dbg_zero_offset   = 0.0f;   /* Offset goc dien Pha A (rad) */
volatile float    dbg_pp_check      = 0.0f;   /* Ti so pole pairs thuc do (~11) */
volatile uint8_t  driver_fault      = 0;      /* 1 = Bao loi driver SimpleFOC Mini */

/* Theo doi mode truoc do de phat hien thay doi */
static uint8_t prev_mode = 255;

/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
/* USER CODE BEGIN PFP */

void    Driver_Enable(void);
void    Driver_Disable(void);
uint8_t Driver_IsFault(void);
void    PWM_Start(void);
void    PWM_Stop(void);

/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */

void Driver_Enable(void)  { HAL_GPIO_WritePin(EN_GPIO_Port, EN_Pin, GPIO_PIN_SET); }
void Driver_Disable(void) { HAL_GPIO_WritePin(EN_GPIO_Port, EN_Pin, GPIO_PIN_RESET); }
uint8_t Driver_IsFault(void) {
    /* SimpleFOC Mini v2 khong keo chan nFAULT ra header ngoai (PB1 floating tren STM32).
     * Luon tra ve 0 de khong bao gio gay treo CPU boi nhieu PB1. */
    return 0;
}

void PWM_Start(void) {
    HAL_TIM_PWM_Start(&htim1, TIM_CHANNEL_1);
    HAL_TIM_PWM_Start(&htim1, TIM_CHANNEL_2);
    HAL_TIM_PWM_Start(&htim1, TIM_CHANNEL_3);
}

void PWM_Stop(void) {
    __HAL_TIM_SET_COMPARE(&htim1, TIM_CHANNEL_1, 0);
    __HAL_TIM_SET_COMPARE(&htim1, TIM_CHANNEL_2, 0);
    __HAL_TIM_SET_COMPARE(&htim1, TIM_CHANNEL_3, 0);
    HAL_TIM_PWM_Stop(&htim1, TIM_CHANNEL_1);
    HAL_TIM_PWM_Stop(&htim1, TIM_CHANNEL_2);
    HAL_TIM_PWM_Stop(&htim1, TIM_CHANNEL_3);
}

/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{

  /* USER CODE BEGIN 1 */

  /* USER CODE END 1 */

  /* MCU Configuration--------------------------------------------------------*/

  /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
  HAL_Init();

  /* USER CODE BEGIN Init */

  /* USER CODE END Init */

  /* Configure the system clock */
  SystemClock_Config();

  /* USER CODE BEGIN SysInit */

  /* USER CODE END SysInit */

  /* Initialize all configured peripherals */
  MX_GPIO_Init();
  MX_ADC1_Init();
  MX_SPI1_Init();
  MX_TIM1_Init();
  /* USER CODE BEGIN 2 */

  /* CSN = HIGH (MT6701 SSI idle) */
  HAL_GPIO_WritePin(CSN_GPIO_Port, CSN_Pin, GPIO_PIN_SET);

  /* Kiem tra nFault driver (khong dung while(1) tranh treo chip) */
  if (Driver_IsFault()) {
      driver_fault = 1;
  }

  /* Khoi tao he thong FOC */
  FOC_Init(&foc, MOTOR_POLE_PAIRS, VOLTAGE_SUPPLY, VOLTAGE_LIMIT);

  /* Bat driver + PWM */
  PWM_Start();
  Driver_Enable();

  /* Cho 1 giay cho nguon va cam bien on dinh */
  HAL_Delay(1000);

  /* Doc thu encoder 1 lan de kiem tra ket noi */
  MT6701_SPI_ReadRaw(&foc.encoder);
  dbg_raw_angle  = foc.encoder.raw_angle;
  dbg_status_mgh = foc.encoder.status_mgh;
  dbg_status_mgl = foc.encoder.status_mgl;

  /* ===========================================================
   *  KHOI DONG CHE DO BAN DAU
   * =========================================================== */
  if (cmd_mode == 1)
  {
      /* Tu dong Calibrate khi khoi dong */
      FOC_Calibrate(&foc);

      dbg_is_calibrated = foc.motor.is_calibrated;
      dbg_calib_ok      = foc.motor.calib_success;
      dbg_direction     = foc.encoder.direction;
      dbg_zero_offset   = foc.encoder.zero_electrical_offset;
      dbg_pp_check      = foc.motor.pp_check_result;

      /* Chay FOC van toc ngay neu calib thanh cong */
      if (foc.motor.is_calibrated)
      {
          FOC_SetVelocity(&foc, cmd_target_velocity);
      }
      else
      {
          FOC_Disable(&foc);
      }
  }
  else
  {
      /* Mode 0: Chay open-loop de test */
      FOC_RunOpenLoop(&foc, cmd_openloop_voltage, cmd_openloop_velocity);
  }

  foc.motor.tick_prev = HAL_GetTick();
  prev_mode = cmd_mode;

  /* USER CODE END 2 */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
  while (1)
  {
    /* USER CODE END WHILE */

    /* USER CODE BEGIN 3 */

    /* =========================================================
     *  LENH RE-CALIBRATE TU DEBUGGER (Dat cmd_recalibrate = 1)
     * ========================================================= */
    if (cmd_recalibrate)
    {
        cmd_recalibrate = 0;
        FOC_Disable(&foc);
        HAL_Delay(200);
        FOC_Calibrate(&foc);
        dbg_is_calibrated = foc.motor.is_calibrated;
        dbg_calib_ok      = foc.motor.calib_success;
        dbg_direction     = foc.encoder.direction;
        dbg_zero_offset   = foc.encoder.zero_electrical_offset;
        dbg_pp_check      = foc.motor.pp_check_result;
        if (cmd_mode == 1)
        {
            if (foc.motor.is_calibrated)
            {
                FOC_SetVelocity(&foc, cmd_target_velocity);
            }
            else
            {
                FOC_Disable(&foc);
            }
        }
        else if (cmd_mode == 2)
        {
            if (foc.motor.is_calibrated)
            {
                FOC_SetTorque(&foc, cmd_target_Uq);
            }
            else
            {
                FOC_Disable(&foc);
            }
        }
    }

    /* =========================================================
     *  PHAT HIEN THAY DOI CHE DO (tu Live Expressions)
     * ========================================================= */
    if (cmd_mode != prev_mode)
    {
        if (cmd_mode == 0)
        {
            /* Chuyen sang OPEN-LOOP */
            FOC_RunOpenLoop(&foc, cmd_openloop_voltage, cmd_openloop_velocity);
        }
        else if (cmd_mode == 1 || cmd_mode == 2)
        {
            /* Chuyen sang CLOSED-LOOP FOC (Velocity hoac Torque) */
            if (!foc.motor.is_calibrated)
            {
                /* Dung em motor truoc khi calibrate de tranh shock dong */
                FOC_Disable(&foc);
                HAL_Delay(200);
                FOC_Calibrate(&foc);
                dbg_is_calibrated = foc.motor.is_calibrated;
                dbg_calib_ok      = foc.motor.calib_success;
                dbg_direction     = foc.encoder.direction;
                dbg_zero_offset   = foc.encoder.zero_electrical_offset;
                dbg_pp_check      = foc.motor.pp_check_result;
            }
            if (foc.motor.is_calibrated)
            {
                if (cmd_mode == 1)
                {
                    FOC_SetVelocity(&foc, cmd_target_velocity);
                }
                else
                {
                    FOC_SetTorque(&foc, cmd_target_Uq);
                }
            }
            else
            {
                FOC_Disable(&foc);
            }
        }
        prev_mode = cmd_mode;
    }

    /* =========================================================
     *  CAP NHAT THONG SO TU DEBUGGER
     * ========================================================= */
    if (cmd_mode == 0)
    {
        foc.motor.openloop_voltage  = cmd_openloop_voltage;
        foc.motor.openloop_velocity = cmd_openloop_velocity;
    }
    else if (cmd_mode == 1)
    {
        foc.motor.target_velocity = cmd_target_velocity;
    }
    else if (cmd_mode == 2)
    {
        foc.motor.target_Uq = cmd_target_Uq;
    }

    /* Cho phep ghi de chieu quay thu cong neu can (tu dong recalibrate de tinh zero offset chuan) */
    static int8_t prev_dir_override = 0;
    if (cmd_direction_override != prev_dir_override)
    {
        prev_dir_override = cmd_direction_override;
        if (cmd_direction_override != 0)
        {
            foc.encoder.direction = cmd_direction_override;
            cmd_recalibrate = 1;
        }
    }

    /* =========================================================
     *  CHAY VONG LAP FOC (~1kHz)
     * ========================================================= */
    FOC_Loop(&foc);

    /* =========================================================
     *  CAP NHAT BIEN GIAM SAT
     * ========================================================= */
    dbg_heartbeat++;
    dbg_raw_angle     = foc.encoder.raw_angle;
    dbg_status_mgh    = foc.encoder.status_mgh;
    dbg_status_mgl    = foc.encoder.status_mgl;
    dbg_mech_angle    = foc.encoder.mechanical_angle;
    dbg_elec_angle    = foc.encoder.electrical_angle;
    dbg_velocity      = foc.encoder.velocity;
    dbg_Uq            = foc.motor.Uq;
    dbg_is_calibrated = foc.motor.is_calibrated;
    dbg_calib_ok      = foc.motor.calib_success;
    dbg_direction     = foc.encoder.direction;
    dbg_zero_offset   = foc.encoder.zero_electrical_offset;
    dbg_pp_check      = foc.motor.pp_check_result;

    /* =========================================================
     *  KIEM TRA LOI DRIVER (Khong bao gio dung while(1) treo CPU)
     * ========================================================= */
    if (Driver_IsFault())
    {
        driver_fault = 1;
        FOC_Disable(&foc);
        Driver_Disable();
        PWM_Stop();
    }

    HAL_Delay(1);
  }
  /* USER CODE END 3 */
}

/**
  * @brief System Clock Configuration
  * @retval None
  */
void SystemClock_Config(void)
{
  RCC_OscInitTypeDef RCC_OscInitStruct = {0};
  RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};

  /** Configure the main internal regulator output voltage
  */
  HAL_PWREx_ControlVoltageScaling(PWR_REGULATOR_VOLTAGE_SCALE1_BOOST);

  /** Initializes the RCC Oscillators according to the specified parameters
  * in the RCC_OscInitTypeDef structure.
  */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSE;
  RCC_OscInitStruct.HSEState = RCC_HSE_ON;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
  RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSE;
  RCC_OscInitStruct.PLL.PLLM = RCC_PLLM_DIV2;
  RCC_OscInitStruct.PLL.PLLN = 85;
  RCC_OscInitStruct.PLL.PLLP = RCC_PLLP_DIV2;
  RCC_OscInitStruct.PLL.PLLQ = RCC_PLLQ_DIV2;
  RCC_OscInitStruct.PLL.PLLR = RCC_PLLR_DIV2;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler();
  }

  /** Initializes the CPU, AHB and APB buses clocks
  */
  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV1;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV1;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_4) != HAL_OK)
  {
    Error_Handler();
  }
}

/* USER CODE BEGIN 4 */

/* USER CODE END 4 */

/**
  * @brief  This function is executed in case of error occurrence.
  * @retval None
  */
void Error_Handler(void)
{
  /* USER CODE BEGIN Error_Handler_Debug */
  /* User can add his own implementation to report the HAL error return state */
  __disable_irq();
  while (1)
  {
  }
  /* USER CODE END Error_Handler_Debug */
}
#ifdef USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t *file, uint32_t line)
{
  /* USER CODE BEGIN 6 */
  /* User can add his own implementation to report the file name and line number,
     ex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */

