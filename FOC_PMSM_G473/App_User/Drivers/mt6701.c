#include "mt6701.h"
#include "spi.h"
#include <math.h>

#define MT6701_CS_LOW() GPIOB->BSRR = (1U << (7 + 16)) // PB7 LOW
#define MT6701_CS_HIGH() GPIOB->BSRR = (1U << 7)       // PB7 HIGH

// Thời gian trễ trung bình của cảm biến + chu kỳ lấy mẫu PWM ~ 75 microsecond
#define LATENCY_COMPENSATION_SEC 0.000075f

void MT6701_Init(MT6701_t *enc, int8_t pole_pairs) {
  enc->raw_angle = 0;
  enc->mech_angle = 0.0f;
  enc->mech_angle_prev = 0.0f;
  enc->elec_angle = 0.0f;
  enc->elec_angle_comp = 0.0f;
  enc->elec_offset = 0.0f;
  enc->velocity_elec = 0.0f;
  enc->pole_pairs = pole_pairs;
  enc->direction = -1; // Chiều nghịch pha

  GPIOB->BSRR = (1U << 6);
  MT6701_CS_HIGH();
  HAL_Delay(2);
}

uint16_t MT6701_ReadRaw(void) {
  uint16_t rx_data = 0;
  uint16_t tx_dummy = 0xFFFF;

  MT6701_CS_LOW();
  HAL_SPI_TransmitReceive(&hspi3, (uint8_t *)&tx_dummy, (uint8_t *)&rx_data, 1,
                          5);
  MT6701_CS_HIGH();

  return (rx_data >> 2) & 0x3FFF;
}

void MT6701_Update(MT6701_t *enc, float w_mech) {
  enc->raw_angle = MT6701_ReadRaw();

  // 1. Góc cơ học hiện tại
  enc->mech_angle = ((float)enc->raw_angle / MT6701_CPR) * MT6701_2PI;

  // 2. Góc điện tức thời: theta_e = direction * theta_mech * pole_pairs -
  // offset
  float e_ang =
      ((float)enc->direction * enc->mech_angle * (float)enc->pole_pairs) -
      enc->elec_offset;

  // 3. BÙ GÓC TRỄ PHA (Sử dụng vận tốc cơ học đã được lọc mượt, triệt tiêu hoàn
  // toàn nhiễu răng cưa)
  float w_elec = (float)enc->direction * w_mech * (float)enc->pole_pairs;
  enc->velocity_elec = w_elec;

  float compensated_e_ang =
      e_ang + (enc->velocity_elec * LATENCY_COMPENSATION_SEC);

  // Chuẩn hóa về [0, 2*PI)
  compensated_e_ang = fmodf(compensated_e_ang, MT6701_2PI);
  if (compensated_e_ang < 0.0f) {
    compensated_e_ang += MT6701_2PI;
  }

  enc->elec_angle = fmodf(e_ang, MT6701_2PI);
  if (enc->elec_angle < 0.0f)
    enc->elec_angle += MT6701_2PI;

  enc->elec_angle_comp = compensated_e_ang;
}
