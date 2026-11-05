#include "foc_math.h"

/**
 * @brief Thuật toán SVPWM (Midpoint Clamping / Space Vector PWM)
 * Tận dụng 100% biên độ điện áp bus (cao hơn Sinusoidal PWM 15.5%)
 */
void SVPWM_Calculate(float v_alpha, float v_beta, float vbus, uint16_t max_duty,
                     uint16_t *duty_u, uint16_t *duty_v, uint16_t *duty_w) {
  if (vbus <= 0.1f) {
    *duty_u = max_duty / 2;
    *duty_v = max_duty / 2;
    *duty_w = max_duty / 2;
    return;
  }

  // 1. Nghịch đảo Clarke để tính điện áp pha tham chiếu: Va, Vb, Vc
  float va = v_alpha;
  float vb = -0.5f * v_alpha + _SQRT3_2 * v_beta;
  float vc = -0.5f * v_alpha - _SQRT3_2 * v_beta;

  // 2. Kỹ thuật đưa điện áp thứ tự không (Zero-sequence voltage / Midpoint
  // clamp)
  float v_max = va;
  if (vb > v_max)
    v_max = vb;
  if (vc > v_max)
    v_max = vc;

  float v_min = va;
  if (vb < v_min)
    v_min = vb;
  if (vc < v_min)
    v_min = vc;

  // Điện áp bù offset SVPWM
  float v_com = 0.5f * (v_max + v_min);

  // Chuẩn hóa và chuyển đổi sang Duty Cycle [0 -> max_duty]
  float half_period = 0.5f * max_duty;
  float scale = (float)max_duty / vbus;

  int32_t du = (int32_t)(half_period + (va - v_com) * scale);
  int32_t dv = (int32_t)(half_period + (vb - v_com) * scale);
  int32_t dw = (int32_t)(half_period + (vc - v_com) * scale);

  // Kẹp bão hòa an toàn [0, max_duty]
  if (du < 0)
    du = 0;
  else if (du > max_duty)
    du = max_duty;
  if (dv < 0)
    dv = 0;
  else if (dv > max_duty)
    dv = max_duty;
  if (dw < 0)
    dw = 0;
  else if (dw > max_duty)
    dw = max_duty;

  *duty_u = (uint16_t)du;
  *duty_v = (uint16_t)dv;
  *duty_w = (uint16_t)dw;
}
