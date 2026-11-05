#include "telemetry.h"
#include "MotorControl/foc_core.h"
#include "usbd_cdc_if.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define RX_BUF_SIZE 64
static char rx_buf[RX_BUF_SIZE];
static uint8_t rx_idx = 0;
static uint8_t usb_tx_buffer[128];

extern USBD_HandleTypeDef hUsbDeviceFS;

void Telemetry_Init(void) { rx_idx = 0; }

void Telemetry_Send(float actual_pos, float target_pos, float velocity,
                    float vq) {
  USBD_CDC_HandleTypeDef *hcdc =
      (USBD_CDC_HandleTypeDef *)hUsbDeviceFS.pClassData;

  if (hcdc != NULL && hcdc->TxState == 0) {
    float act_deg = actual_pos * (180.0f / 3.14159265f);
    float tar_val = 0.0f;
    if (g_foc.mode == FOC_MODE_POSITION) {
      tar_val = target_pos * (180.0f / 3.14159265f); // degrees
    } else if (g_foc.mode == FOC_MODE_VELOCITY) {
      tar_val = g_foc.target_velocity * (30.0f / 3.14159265f); // RPM
    } else {
      tar_val = g_foc.target_torque; // Vq (V)
    }
    float rpm = velocity * (30.0f / 3.14159265f);

    // Định dạng gói tin công nghiệp:
    // T:act_deg,tar_val,rpm,vq,mode,in_pos,at_spd
    int len = snprintf((char *)usb_tx_buffer, sizeof(usb_tx_buffer),
                       "T:%.2f,%.2f,%.1f,%.2f,%d,%d,%d\r\n", act_deg, tar_val,
                       rpm, vq, (int)g_foc.mode, (int)g_foc.is_in_position,
                       (int)g_foc.is_at_speed);
    if (len > 0) {
      CDC_Transmit_FS(usb_tx_buffer, (uint16_t)len);
    }
  }
}

static void Telemetry_ParseCommand(char *cmd) {
  if (cmd[0] == 'M' && cmd[1] == ':') {
    // Đổi chế độ: M:0 (Position), M:1 (Velocity), M:2 (Torque)
    int m = atoi(&cmd[2]);
    if (m >= 0 && m <= 2) {
      g_foc.mode = (FOC_ControlMode_t)m;
      g_foc.profile_position = g_foc.full_angle;
      g_foc.profile_velocity = g_foc.velocity_filtered;
    }
  } else if (cmd[0] == 'P' && cmd[1] == ':') {
    // Đặt góc mục tiêu (Degrees): ví dụ P:180.0
    float deg = atof(&cmd[2]);
    g_foc.target_position = deg * (3.14159265f / 180.0f);
  } else if (cmd[0] == 'V' && cmd[1] == ':') {
    // Đặt tốc độ mục tiêu (RPM): ví dụ V:300.0
    float rpm = atof(&cmd[2]);
    g_foc.target_velocity = rpm * (3.14159265f / 30.0f); // RPM sang rad/s
  } else if (cmd[0] == 'T' && cmd[1] == ':') {
    // Đặt mô-men / Vq mục tiêu (V): ví dụ T:2.5
    float tq = atof(&cmd[2]);
    g_foc.target_torque = tq;
  } else if (cmd[0] == 'S' && cmd[1] == ':') {
    // Bật / Dừng Motor (E-STOP)
    int state = atoi(&cmd[2]);
    g_foc.is_enabled = (state != 0) ? 1 : 0;
  } else if (cmd[0] == 'H' && cmd[1] == ':') {
    // Re-Zero / Set Home Position: H:0
    FOC_SetHome();
  } else if (cmd[0] == 'L' && cmd[1] == ':') {
    // Giới hạn tốc độ góc ở Mode Position (RPM): ví dụ L:300
    float rpm = atof(&cmd[2]);
    if (rpm > 10.0f) {
      g_foc.max_velocity = rpm * (3.14159265f / 30.0f);
      g_foc.pid_pos.out_max = g_foc.max_velocity;
      g_foc.pid_pos.out_min = -g_foc.max_velocity;
    }
  } else if (cmd[0] == 'A' && cmd[1] == ':') {
    // Gia tốc tăng tốc (rad/s^2): ví dụ A:150
    float acc = atof(&cmd[2]);
    if (acc > 5.0f) {
      g_foc.acceleration = acc;
    }
  } else if (cmd[0] == 'D' && cmd[1] == ':') {
    // Gia tốc giảm tốc / phanh chủ động (rad/s^2): ví dụ D:1200
    float dec = atof(&cmd[2]);
    if (dec > 20.0f) {
      g_foc.deceleration = dec;
    }
  }
}

void Telemetry_ProcessRxByte(uint8_t ch) {
  if (ch == '\n' || ch == '\r') {
    if (rx_idx > 0) {
      rx_buf[rx_idx] = '\0';
      Telemetry_ParseCommand(rx_buf);
      rx_idx = 0;
    }
  } else {
    if (rx_idx < (RX_BUF_SIZE - 1)) {
      rx_buf[rx_idx++] = (char)ch;
    } else {
      rx_idx = 0;
    }
  }
}
