#include "app_main.h"
#include "Hal/telemetry.h"
#include "MotorControl/foc_core.h"
#include <math.h>
#include <stdio.h>

void App_Init(void) {
  HAL_Delay(1000);

  // 1. Khởi tạo FOC Servo công nghiệp
  FOC_Init();

  // 2. Tự động tìm góc và chiều quay
  FOC_AlignSensor();

  // 3. Khởi tạo kênh giao tiếp Telemetry qua USB-CDC
  Telemetry_Init();
}

void App_Loop(void) {
  static uint32_t last_motion_tick = 0;
  static uint32_t last_telemetry_tick = 0;

  // 1. VÒNG LẶP FOC CORE
  FOC_CurrentLoop_ISR();

  uint32_t now = HAL_GetTick();

  // 2. VÒNG ĐIỀU KHIỂN CHUYỂN ĐỘNG (1 kHz): Motion Profile + 3 Modes
  if (now - last_motion_tick >= 1) {
    last_motion_tick = now;
    FOC_MotionLoop();
  }

  // 3. GỬI DỮ LIỆU LÊN MATLAB INDUSTRIAL HMI (100 Hz)
  if (now - last_telemetry_tick >= 10) {
    last_telemetry_tick = now;

    Telemetry_Send(g_foc.full_angle, g_foc.target_position,
                   g_foc.velocity_filtered, g_foc.target_iq);

    GPIOC->ODR ^= (1U << 14); // Toggle LED1 nhịp tim
  }
}
