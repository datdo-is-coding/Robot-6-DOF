#ifndef FOC_MATH_H
#define FOC_MATH_H

#include "main.h"
#include <math.h>

#define _SQRT3 1.73205080757f
#define _1_SQRT3 0.57735026919f
#define _2_SQRT3 1.15470053838f
#define _SQRT3_2 0.86602540378f

// Biến đổi Clarke: (Ia, Ib, Ic) -> (I_alpha, I_beta)
// Sử dụng công thức không phụ thuộc Ic (Ia + Ib + Ic = 0)
static inline void Clarke_Transform(float ia, float ib, float *i_alpha,
                                    float *i_beta) {
  *i_alpha = ia;
  *i_beta = (ia + 2.0f * ib) * _1_SQRT3;
}

// Biến đổi Park: (I_alpha, I_beta, theta) -> (Id, Iq)
static inline void Park_Transform(float i_alpha, float i_beta, float sin_th,
                                  float cos_th, float *id, float *iq) {
  *id = i_alpha * cos_th + i_beta * sin_th;
  *iq = -i_alpha * sin_th + i_beta * cos_th;
}

// Biến đổi Park ngược (Inverse Park): (Vd, Vq, theta) -> (V_alpha, V_beta)
static inline void InvPark_Transform(float vd, float vq, float sin_th,
                                     float cos_th, float *v_alpha,
                                     float *v_beta) {
  *v_alpha = vd * cos_th - vq * sin_th;
  *v_beta = vd * sin_th + vq * cos_th;
}

// Bộ điều chế vector không gian SVPWM: (V_alpha, V_beta, Vbus, MaxDuty) ->
// (DutyU, DutyV, DutyW)
void SVPWM_Calculate(float v_alpha, float v_beta, float vbus, uint16_t max_duty,
                     uint16_t *duty_u, uint16_t *duty_v, uint16_t *duty_w);

#endif /* FOC_MATH_H */
