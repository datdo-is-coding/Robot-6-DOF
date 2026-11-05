#ifndef MT6701_H
#define MT6701_H

#include "main.h"

#define MT6701_CPR 16384.0f
#define MT6701_2PI 6.28318530718f

typedef struct {
  uint16_t raw_angle; // Giá trị raw 14-bit (0 -> 16383)
  float mech_angle;   // Góc cơ học (rad)
  float mech_angle_prev;
  float elec_angle;      // Góc điện thực tế
  float elec_angle_comp; // Góc điện ĐÃ ĐƯỢC BÙ TRỄ PHA (Compensated)
  float elec_offset;     // Góc lệch tĩnh zero calibration
  float velocity_elec;   // Vận tốc góc điện (rad/s)
  int8_t pole_pairs;     // 11 cặp cực
  int8_t direction;      // Chiều quay (-1 hoặc +1)
} MT6701_t;

void MT6701_Init(MT6701_t *enc, int8_t pole_pairs);
uint16_t MT6701_ReadRaw(void);
void MT6701_Update(MT6701_t *enc, float w_mech);

#endif /* MT6701_H */
