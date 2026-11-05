/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.h
  * @brief          : Header for main.c file.
  *                   This file contains the common defines of the application.
  ******************************************************************************
  * @attention
  *
  * Copyright (c) 2026 STMicroelectronics.
  * All rights reserved.
  *
  * This software is licensed under terms that can be found in the LICENSE file
  * in the root directory of this software component.
  * If no LICENSE file comes with this software, it is provided AS-IS.
  *
  ******************************************************************************
  */
/* USER CODE END Header */

/* Define to prevent recursive inclusion -------------------------------------*/
#ifndef __MAIN_H
#define __MAIN_H

#ifdef __cplusplus
extern "C" {
#endif

/* Includes ------------------------------------------------------------------*/
#include "stm32g4xx_hal.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */

/* USER CODE END Includes */

/* Exported types ------------------------------------------------------------*/
/* USER CODE BEGIN ET */

/* USER CODE END ET */

/* Exported constants --------------------------------------------------------*/
/* USER CODE BEGIN EC */

/* USER CODE END EC */

/* Exported macro ------------------------------------------------------------*/
/* USER CODE BEGIN EM */

/* USER CODE END EM */

/* Exported functions prototypes ---------------------------------------------*/
void Error_Handler(void);

/* USER CODE BEGIN EFP */

/* USER CODE END EFP */

/* Private defines -----------------------------------------------------------*/
#define LED1_Pin GPIO_PIN_14
#define LED1_GPIO_Port GPIOC
#define LED2_Pin GPIO_PIN_15
#define LED2_GPIO_Port GPIOC
#define VSENSE_C_Pin GPIO_PIN_0
#define VSENSE_C_GPIO_Port GPIOC
#define VBUS_SENSE_Pin GPIO_PIN_2
#define VBUS_SENSE_GPIO_Port GPIOC
#define FET_TEMP_Pin GPIO_PIN_0
#define FET_TEMP_GPIO_Port GPIOA
#define VSENSE_A_Pin GPIO_PIN_3
#define VSENSE_A_GPIO_Port GPIOA
#define DRV_SCK_Pin GPIO_PIN_5
#define DRV_SCK_GPIO_Port GPIOA
#define DRV_MISO_Pin GPIO_PIN_6
#define DRV_MISO_GPIO_Port GPIOA
#define DRV_BKIN_Pin GPIO_PIN_10
#define DRV_BKIN_GPIO_Port GPIOB
#define CAN_RX_Pin GPIO_PIN_12
#define CAN_RX_GPIO_Port GPIOB
#define CAN_TX_Pin GPIO_PIN_13
#define CAN_TX_GPIO_Port GPIOB
#define VSENSE_B_Pin GPIO_PIN_14
#define VSENSE_B_GPIO_Port GPIOB
#define DRV_CS_Pin GPIO_PIN_6
#define DRV_CS_GPIO_Port GPIOC
#define DRV_EN_Pin GPIO_PIN_7
#define DRV_EN_GPIO_Port GPIOC
#define ENC_SCL_Pin GPIO_PIN_8
#define ENC_SCL_GPIO_Port GPIOC
#define ENC_SDA_Pin GPIO_PIN_9
#define ENC_SDA_GPIO_Port GPIOC
#define ENC_SCK_Pin GPIO_PIN_10
#define ENC_SCK_GPIO_Port GPIOC
#define ENC_MISO_Pin GPIO_PIN_11
#define ENC_MISO_GPIO_Port GPIOC
#define ENC_MOSI_Pin GPIO_PIN_12
#define ENC_MOSI_GPIO_Port GPIOC
#define DRV_MOSI_Pin GPIO_PIN_5
#define DRV_MOSI_GPIO_Port GPIOB
#define ENC_EN_Pin GPIO_PIN_6
#define ENC_EN_GPIO_Port GPIOB
#define ENC_CS_Pin GPIO_PIN_7
#define ENC_CS_GPIO_Port GPIOB

/* USER CODE BEGIN Private defines */

/* USER CODE END Private defines */

#ifdef __cplusplus
}
#endif

#endif /* __MAIN_H */
