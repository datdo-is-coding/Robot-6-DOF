#include "current_sense.h"
#include "MotorControl/foc_math.h"
#include "adc.h"

CurrentSense_t g_current;

void CurrentSense_Init(void) {
  g_current.offset_a = 2048;
  g_current.offset_b = 2048;
  g_current.ia = 0.0f;
  g_current.ib = 0.0f;
  g_current.ic = 0.0f;
  g_current.id = 0.0f;
  g_current.iq = 0.0f;
  g_current.id_filtered = 0.0f;
  g_current.iq_filtered = 0.0f;
}

void CurrentSense_CalibrateOffset(void) {
  uint32_t sum_a = 0;
  uint32_t sum_b = 0;
  const uint16_t samples = 1024;

  for (uint16_t i = 0; i < samples; i++) {
    HAL_ADCEx_InjectedStart(&hadc1);
    HAL_ADCEx_InjectedStart(&hadc2);

    HAL_ADCEx_InjectedPollForConversion(&hadc1, 10);
    HAL_ADCEx_InjectedPollForConversion(&hadc2, 10);

    sum_a += (uint16_t)ADC1->JDR1;
    sum_b += (uint16_t)ADC2->JDR1;
    HAL_Delay(1);
  }

  g_current.offset_a = (uint16_t)(sum_a / samples);
  g_current.offset_b = (uint16_t)(sum_b / samples);

  HAL_ADCEx_InjectedStart_IT(&hadc1);
  HAL_ADCEx_InjectedStart_IT(&hadc2);
}

void CurrentSense_Read(float sin_th, float cos_th) {
  int32_t raw_a = (int32_t)ADC1->JDR1 - (int32_t)g_current.offset_a;
  int32_t raw_b = (int32_t)ADC2->JDR1 - (int32_t)g_current.offset_b;

  // Dòng pha thực tế (Gain 40V/V)
  g_current.ia = (float)raw_a * CURRENT_SENSE_SCALE;
  g_current.ib = (float)raw_b * CURRENT_SENSE_SCALE;
  g_current.ic = -(g_current.ia + g_current.ib);

  // Biến đổi Clarke
  Clarke_Transform(g_current.ia, g_current.ib, &g_current.i_alpha,
                   &g_current.i_beta);

  // Biến đổi Park
  Park_Transform(g_current.i_alpha, g_current.i_beta, sin_th, cos_th,
                 &g_current.id, &g_current.iq);

  // BỘ LỌC THÔNG THẤP IIR BẬC 1 (Fc ~ 2.5 kHz) TRIỆT TIÊU SWITCHING NOISE
  g_current.id_filtered = 0.80f * g_current.id_filtered + 0.20f * g_current.id;
  g_current.iq_filtered = 0.80f * g_current.iq_filtered + 0.20f * g_current.iq;
}
