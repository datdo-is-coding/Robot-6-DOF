#ifndef DRV83XX_H
#define DRV83XX_H

#include "main.h"

uint8_t DRV_Init(void);
void DRV_WriteReg(uint8_t reg_addr, uint16_t reg_val);
uint16_t DRV_ReadReg(uint8_t reg_addr);

#endif
