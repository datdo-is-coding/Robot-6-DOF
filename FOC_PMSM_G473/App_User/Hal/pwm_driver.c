#include "pwm_driver.h"
#include "tim.h"

void PWM_Init(void) {
  // Đảm bảo CCR ban đầu = 0 trước khi mở cầu H
  TIM1->CCR1 = 0;
  TIM1->CCR2 = 0;
  TIM1->CCR3 = 0;
}

void PWM_Start(void) {
  // Bật kênh thuận (High-side) và kênh bù (Low-side) cho cả 3 pha
  HAL_TIM_PWM_Start(&htim1, TIM_CHANNEL_1);
  HAL_TIMEx_PWMN_Start(&htim1, TIM_CHANNEL_1);

  HAL_TIM_PWM_Start(&htim1, TIM_CHANNEL_2);
  HAL_TIMEx_PWMN_Start(&htim1, TIM_CHANNEL_2);

  HAL_TIM_PWM_Start(&htim1, TIM_CHANNEL_3);
  HAL_TIMEx_PWMN_Start(&htim1, TIM_CHANNEL_3);
}

void PWM_Stop(void) {
  // Tắt PWM 3 pha, đưa cầu H về trạng thái thả nổi (Hi-Z) an toàn
  HAL_TIM_PWM_Stop(&htim1, TIM_CHANNEL_1);
  HAL_TIMEx_PWMN_Stop(&htim1, TIM_CHANNEL_1);

  HAL_TIM_PWM_Stop(&htim1, TIM_CHANNEL_2);
  HAL_TIMEx_PWMN_Stop(&htim1, TIM_CHANNEL_2);

  HAL_TIM_PWM_Stop(&htim1, TIM_CHANNEL_3);
  HAL_TIMEx_PWMN_Stop(&htim1, TIM_CHANNEL_3);

  TIM1->CCR1 = 0;
  TIM1->CCR2 = 0;
  TIM1->CCR3 = 0;
}

void PWM_SetDuty(uint16_t u, uint16_t v, uint16_t w) {
  // Giới hạn an toàn không vượt quá ARR
  if (u > PWM_PERIOD_MAX)
    u = PWM_PERIOD_MAX;
  if (v > PWM_PERIOD_MAX)
    v = PWM_PERIOD_MAX;
  if (w > PWM_PERIOD_MAX)
    w = PWM_PERIOD_MAX;

  // Nạp trực tiếp vào thanh ghi CCR của TIM1 (chỉ tốn vài chu kỳ clock)
  TIM1->CCR1 = u;
  TIM1->CCR2 = v;
  TIM1->CCR3 = w;
}
