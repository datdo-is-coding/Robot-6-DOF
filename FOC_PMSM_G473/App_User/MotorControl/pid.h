#ifndef PID_H
#define PID_H

typedef struct {
  float kp;
  float ki;
  float kd;
  float integral;
  float prev_error;
  float out_max;
  float out_min;
} PID_Controller_t;

void PID_Init(PID_Controller_t *pid, float kp, float ki, float kd,
              float out_min, float out_max);
void PID_Reset(PID_Controller_t *pid);
float PID_Calculate(PID_Controller_t *pid, float setpoint, float feedback);

#endif /* PID_H */
