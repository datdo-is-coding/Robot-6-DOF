#include "pid.h"

void PID_Init(PID_Controller_t *pid, float kp, float ki, float kd,
              float out_min, float out_max) {
  pid->kp = kp;
  pid->ki = ki;
  pid->kd = kd;
  pid->integral = 0.0f;
  pid->prev_error = 0.0f;
  pid->out_min = out_min;
  pid->out_max = out_max;
}

void PID_Reset(PID_Controller_t *pid) {
  pid->integral = 0.0f;
  pid->prev_error = 0.0f;
}

float PID_Calculate(PID_Controller_t *pid, float setpoint, float feedback) {
  float error = setpoint - feedback;

  // Tỉ lệ (Proportional)
  float p_out = pid->kp * error;

  // Tích phân (Integral)
  pid->integral += pid->ki * error;

  // Chống bão hòa tích phân (Anti-windup clamping)
  if (pid->integral > pid->out_max) {
    pid->integral = pid->out_max;
  } else if (pid->integral < pid->out_min) {
    pid->integral = pid->out_min;
  }

  // Vi phân (Derivative)
  float d_out = pid->kd * (error - pid->prev_error);
  pid->prev_error = error;

  // Tổng ngõ ra
  float output = p_out + pid->integral + d_out;

  // Bão hòa ngõ ra (Output Saturation)
  if (output > pid->out_max) {
    output = pid->out_max;
  } else if (output < pid->out_min) {
    output = pid->out_min;
  }

  return output;
}
