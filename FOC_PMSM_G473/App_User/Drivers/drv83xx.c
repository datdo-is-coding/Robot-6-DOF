#include "drv83xx.h"
#include "spi.h"

uint8_t DRV_Init(void) {
  // 1. Kéo chân ENABLE lên HIGH
  GPIOC->BSRR = (1U << 7); // PC7
  HAL_Delay(10);

  // 2. Kéo CS lên HIGH
  GPIOC->BSRR = (1U << 6); // PC6
  HAL_Delay(2);

  // 3. Driver Control (0x02): 6x PWM Mode
  DRV_WriteReg(0x02, 0x0000);

  // 4. OCP Control (0x05): VDS Threshold cao an toàn chống ngắt bậy
  DRV_WriteReg(0x05, 0x015F);

  // 5. CSA Control (0x06): NÂNG ĐỘ LỢI CSA LÊN TỐI ĐA 40 V/V (Bits CSA_GAIN =
  // 11) Tăng gấp đôi độ nhạy cho điện trở Shunt 2mOhm nhỏ!
  DRV_WriteReg(0x06, 0x02B3);

  // Đọc lại Fault Status
  uint16_t fault = DRV_ReadReg(0x00);
  return (fault == 0) ? 0 : 1;
}

void DRV_WriteReg(uint8_t reg_addr, uint16_t reg_val) {
  uint16_t tx_data =
      ((0 << 15) | ((reg_addr & 0x0F) << 11) | (reg_val & 0x07FF));
  GPIOC->BSRR = (1U << (6 + 16));

  HAL_SPI_Transmit(&hspi1, (uint8_t *)&tx_data, 1, 10);

  GPIOC->BSRR = (1U << 6);
}

uint16_t DRV_ReadReg(uint8_t reg_addr) {
  uint16_t tx_data = ((1 << 15) | ((reg_addr & 0x0F) << 11));
  uint16_t rx_data = 0;

  GPIOC->BSRR = (1U << (6 + 16));

  HAL_SPI_TransmitReceive(&hspi1, (uint8_t *)&tx_data, (uint8_t *)&rx_data, 1,
                          10);

  GPIOC->BSRR = (1U << 6);

  return (rx_data & 0x07FF);
}
