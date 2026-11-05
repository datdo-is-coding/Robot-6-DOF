#ifndef FOC_CORE_H
#define FOC_CORE_H

#include "Drivers/drv83xx.h"
#include "Drivers/mt6701.h"
#include "Hal/pwm_driver.h"
#include "MotorControl/foc_math.h"
#include "MotorControl/pid.h"
#include "main.h"

typedef enum {
  FOC_MODE_POSITION = 0, // Chế độ Vị trí (Position Servo với Motion Profile)
  FOC_MODE_VELOCITY,     // Chế độ Tốc độ (Velocity Control)
  FOC_MODE_TORQUE        // Chế độ Mô-men (Torque / Current Control)
} FOC_ControlMode_t;

typedef struct {
  FOC_ControlMode_t mode;
  MT6701_t encoder;

  // Đo lường góc & vận tốc
  float mech_angle_prev;
  int32_t full_rotations;
  float home_offset;
  float full_angle; // Góc thực tế không giới hạn (rad)
  float velocity;
  float velocity_filtered; // Vận tốc đã lọc LPF (rad/s)

  // Mục tiêu điều khiển (User Targets)
  float target_position;  // Góc đặt cuối cùng (rad)
  float profile_position; // Góc quỹ đạo bám theo thời gian thực (Trapezoidal
                          // ramp)
  float target_velocity;  // Tốc độ đặt (rad/s)
  float profile_velocity; // Tốc độ quỹ đạo bám
  float target_torque;    // Mô-men / Vq đặt (V)
  float target_iq;
  float target_id;

  // Thông số động học Motion Profile
  float max_velocity;  // Tốc độ tối đa cho phép (rad/s)
  float acceleration;  // Gia tốc tăng tốc (rad/s^2)
  float deceleration;  // Gia tốc giảm tốc phanh chủ động (rad/s^2)
  float voltage_limit; // Giới hạn điện áp bus
  float vbus;

  // Zero-speed Position Clamp (Khóa cứng trục tức thì khi dừng)
  uint8_t zero_clamp_active;
  float zero_clamp_angle;

  // Cờ trạng thái Servo công nghiệp
  uint8_t is_in_position; // 1 khi đã đến đích vị trí (|Error| < 0.05 rad)
  uint8_t is_at_speed;    // 1 khi đã đạt đúng tốc độ mong muốn
  uint8_t is_enabled;     // 1: Motor Run, 0: Motor Free (E-STOP)

  // Bộ điều khiển PID
  PID_Controller_t pid_vel; // PI Vận tốc
  PID_Controller_t pid_pos; // P Vị trí
} FOC_Handle_t;

extern FOC_Handle_t g_foc;

void FOC_Init(void);
void FOC_AlignSensor(void);
void FOC_CurrentLoop_ISR(void);
void FOC_MotionLoop(void); // Chạy 1kHz: Motion Profile + Position/Velocity Loop
void FOC_SetHome(void);

#endif /* FOC_CORE_H */
