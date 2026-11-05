#include "foc_core.h"
#include <math.h>
#include <stdio.h>

FOC_Handle_t g_foc;

void FOC_Init(void) {
  g_foc.mode = FOC_MODE_POSITION;
  g_foc.is_enabled = 1;
  g_foc.vbus = 24.0f;
  g_foc.voltage_limit = 10.0f; // Headroom cho 1000 RPM

  g_foc.max_velocity = 105.0f; // ~1002 RPM
  g_foc.acceleration = 120.0f; // rad/s^2 (gia tốc tăng tốc)
  g_foc.deceleration =
      1000.0f; // rad/s^2 (phanh khẩn cấp từ 1000 RPM xuống 0 trong ~0.1s)

  g_foc.zero_clamp_active = 0;
  g_foc.zero_clamp_angle = 0.0f;

  g_foc.target_position = 0.0f;
  g_foc.profile_position = 0.0f;
  g_foc.target_velocity = 0.0f;
  g_foc.profile_velocity = 0.0f;
  g_foc.target_torque = 0.0f;
  g_foc.target_iq = 0.0f;
  g_foc.target_id = 0.0f;

  g_foc.full_rotations = 0;
  g_foc.home_offset = 0.0f;
  g_foc.mech_angle_prev = 0.0f;
  g_foc.full_angle = 0.0f;
  g_foc.velocity = 0.0f;
  g_foc.velocity_filtered = 0.0f;

  g_foc.is_in_position = 0;
  g_foc.is_at_speed = 0;

  PID_Init(&g_foc.pid_vel, 0.18f, 0.010f, 0.0f, -g_foc.voltage_limit,
           g_foc.voltage_limit);
  PID_Init(&g_foc.pid_pos, 22.0f, 0.0f, 0.0f, -g_foc.max_velocity,
           g_foc.max_velocity);

  DRV_Init();
  PWM_Init();
  PWM_Start();
  MT6701_Init(&g_foc.encoder, 11);
}

void FOC_SetHome(void) {
  g_foc.home_offset =
      (float)g_foc.full_rotations * MT6701_2PI + g_foc.encoder.mech_angle;
  g_foc.full_angle = 0.0f;
  g_foc.target_position = 0.0f;
  g_foc.profile_position = 0.0f;
  g_foc.zero_clamp_angle = 0.0f;
}

void FOC_AlignSensor(void) {
  float v_align = 2.5f;
  uint16_t du, dv, dw;

  SVPWM_Calculate(v_align, 0.0f, g_foc.vbus, PWM_PERIOD_MAX, &du, &dv, &dw);
  PWM_SetDuty(du, dv, dw);
  HAL_Delay(1000);

  float angle_start = 0.0f;
  for (int i = 0; i < 64; i++) {
    MT6701_Update(&g_foc.encoder, 0.0f);
    angle_start += g_foc.encoder.mech_angle;
    HAL_Delay(2);
  }
  angle_start /= 64.0f;

  SVPWM_Calculate(0.0f, v_align, g_foc.vbus, PWM_PERIOD_MAX, &du, &dv, &dw);
  PWM_SetDuty(du, dv, dw);
  HAL_Delay(800);

  float angle_moved = 0.0f;
  for (int i = 0; i < 64; i++) {
    MT6701_Update(&g_foc.encoder, 0.0f);
    angle_moved += g_foc.encoder.mech_angle;
    HAL_Delay(2);
  }
  angle_moved /= 64.0f;

  float diff = angle_moved - angle_start;
  if (diff < -3.14159f)
    diff += MT6701_2PI;
  else if (diff > 3.14159f)
    diff -= MT6701_2PI;

  if (diff > 0.0f)
    g_foc.encoder.direction = 1;
  else
    g_foc.encoder.direction = -1;

  SVPWM_Calculate(v_align, 0.0f, g_foc.vbus, PWM_PERIOD_MAX, &du, &dv, &dw);
  PWM_SetDuty(du, dv, dw);
  HAL_Delay(500);

  MT6701_Update(&g_foc.encoder, 0.0f);
  g_foc.encoder.elec_offset = (float)g_foc.encoder.direction *
                              g_foc.encoder.mech_angle *
                              (float)g_foc.encoder.pole_pairs;
  g_foc.encoder.elec_offset = fmodf(g_foc.encoder.elec_offset, MT6701_2PI);
  if (g_foc.encoder.elec_offset < 0.0f)
    g_foc.encoder.elec_offset += MT6701_2PI;

  g_foc.mech_angle_prev = g_foc.encoder.mech_angle;
  g_foc.full_rotations = 0;
  g_foc.home_offset = g_foc.encoder.mech_angle;
  g_foc.full_angle = 0.0f;
  g_foc.target_position = 0.0f;
  g_foc.profile_position = 0.0f;
  g_foc.zero_clamp_angle = 0.0f;

  PWM_SetDuty(PWM_PERIOD_HALF, PWM_PERIOD_HALF, PWM_PERIOD_HALF);
  HAL_Delay(200);
}

void FOC_CurrentLoop_ISR(void) {
  // Lấy mẫu góc điện với vận tốc đã lọc mượt mà, triệt tiêu 100% rung lắc góc
  MT6701_Update(&g_foc.encoder, g_foc.velocity_filtered);

  if (!g_foc.is_enabled) {
    PWM_SetDuty(PWM_PERIOD_HALF, PWM_PERIOD_HALF, PWM_PERIOD_HALF);
    return;
  }

  float sin_th = sinf(g_foc.encoder.elec_angle_comp);
  float cos_th = cosf(g_foc.encoder.elec_angle_comp);

  float vd = 0.0f;
  float vq = g_foc.target_iq;

  if (vq > g_foc.voltage_limit)
    vq = g_foc.voltage_limit;
  else if (vq < -g_foc.voltage_limit)
    vq = -g_foc.voltage_limit;

  float v_alpha, v_beta;
  InvPark_Transform(vd, vq, sin_th, cos_th, &v_alpha, &v_beta);

  uint16_t du, dv, dw;
  SVPWM_Calculate(v_alpha, v_beta, g_foc.vbus, PWM_PERIOD_MAX, &du, &dv, &dw);
  PWM_SetDuty(du, dv, dw);
}

void FOC_MotionLoop(void) {
  const float dt = 0.001f;

  float delta_angle = g_foc.encoder.mech_angle - g_foc.mech_angle_prev;
  if (delta_angle > 3.14159f) {
    delta_angle -= MT6701_2PI;
    g_foc.full_rotations--;
  } else if (delta_angle < -3.14159f) {
    delta_angle += MT6701_2PI;
    g_foc.full_rotations++;
  }
  g_foc.mech_angle_prev = g_foc.encoder.mech_angle;

  float raw_cum =
      (float)g_foc.full_rotations * MT6701_2PI + g_foc.encoder.mech_angle;
  g_foc.full_angle = raw_cum - g_foc.home_offset;

  float vel_raw = delta_angle * 1000.0f;
  g_foc.velocity_filtered = 0.88f * g_foc.velocity_filtered + 0.12f * vel_raw;

  switch (g_foc.mode) {
  case FOC_MODE_POSITION: {
    g_foc.zero_clamp_active = 0;

    float pos_err = g_foc.target_position - g_foc.profile_position;
    float max_step = g_foc.max_velocity * dt;

    if (fabsf(pos_err) > max_step) {
      if (pos_err > 0.0f)
        g_foc.profile_position += max_step;
      else
        g_foc.profile_position -= max_step;
    } else {
      g_foc.profile_position = g_foc.target_position;
    }

    g_foc.target_velocity =
        PID_Calculate(&g_foc.pid_pos, g_foc.profile_position, g_foc.full_angle);
    g_foc.target_iq = PID_Calculate(&g_foc.pid_vel, g_foc.target_velocity,
                                    g_foc.velocity_filtered);

    float real_err = fabsf(g_foc.target_position - g_foc.full_angle);
    g_foc.is_in_position =
        (real_err < 0.035f && fabsf(g_foc.velocity_filtered) < 1.0f) ? 1 : 0;
    g_foc.is_at_speed = 0;
    break;
  }

  case FOC_MODE_VELOCITY: {
    float vel_err = g_foc.target_velocity - g_foc.profile_velocity;

    // Tách biệt gia tốc tăng tốc và gia tốc giảm tốc (phanh chủ động)
    float active_rate;
    if (fabsf(g_foc.target_velocity) < fabsf(g_foc.profile_velocity) ||
        (g_foc.target_velocity * g_foc.profile_velocity < 0.0f)) {
      active_rate = g_foc.deceleration; // Đang phanh/giảm tốc/đảo chiều
    } else {
      active_rate = g_foc.acceleration; // Đang tăng tốc
    }

    float max_dv = active_rate * dt;

    if (fabsf(vel_err) > max_dv) {
      if (vel_err > 0.0f)
        g_foc.profile_velocity += max_dv;
      else
        g_foc.profile_velocity -= max_dv;
    } else {
      g_foc.profile_velocity = g_foc.target_velocity;
    }

    // ZERO-SPEED ACTIVE CLAMP (KHÓA CỨNG VỊ TRÍ TỨC THÌ KHI DỪNG VỀ 0 RPM)
    if (g_foc.target_velocity == 0.0f && fabsf(g_foc.profile_velocity) < 0.5f &&
        fabsf(g_foc.velocity_filtered) < 2.5f) {
      if (!g_foc.zero_clamp_active) {
        g_foc.zero_clamp_angle = g_foc.full_angle;
        g_foc.zero_clamp_active = 1;
        PID_Reset(&g_foc.pid_vel);
      }
      // Khóa cứng servo bằng vòng lặp vị trí Position Loop
      float v_cmd = PID_Calculate(&g_foc.pid_pos, g_foc.zero_clamp_angle,
                                  g_foc.full_angle);
      g_foc.target_iq =
          PID_Calculate(&g_foc.pid_vel, v_cmd, g_foc.velocity_filtered);
      g_foc.is_at_speed = 1;
    } else {
      g_foc.zero_clamp_active = 0;
      g_foc.target_iq = PID_Calculate(&g_foc.pid_vel, g_foc.profile_velocity,
                                      g_foc.velocity_filtered);
      g_foc.is_at_speed =
          (fabsf(g_foc.target_velocity - g_foc.velocity_filtered) < 2.5f) ? 1
                                                                          : 0;
    }
    g_foc.is_in_position = 0;
    break;
  }

  case FOC_MODE_TORQUE: {
    g_foc.zero_clamp_active = 0;
    g_foc.target_iq = g_foc.target_torque;
    g_foc.is_in_position = 0;
    g_foc.is_at_speed = 0;
    break;
  }
  }
}
