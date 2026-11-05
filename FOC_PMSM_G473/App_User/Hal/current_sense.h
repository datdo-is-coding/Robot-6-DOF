#ifndef CURRENT_SENSE_H
#define CURRENT_SENSE_H

#include "main.h"

// Hệ số quy đổi chuẩn: Shunt 2mOhm + DRV8353 CSA 40V/V
#define CURRENT_SENSE_SCALE 0.01007325f

typedef struct {
  uint16_t offset_a;
  uint16_t offset_b;
  float ia;
  float ib;
  float ic;
  float i_alpha;
  float i_beta;
  float id;
  float iq;
  float id_filtered;
  float iq_filtered;
} CurrentSense_t;

extern CurrentSense_t g_current;

void CurrentSense_Init(void);
void CurrentSense_CalibrateOffset(void);
void CurrentSense_Read(float sin_th, float cos_th);

#endif /* CURRENT_SENSE_H */
