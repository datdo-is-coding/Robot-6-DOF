#ifndef PWM_DRIVER_H
#define PWM_DRIVER_H

#include "main.h"

// ARR của TIM1: 170MHz / (2 * 4250) = 20kHz Center-Aligned
#define PWM_PERIOD_MAX 4249
#define PWM_PERIOD_HALF (PWM_PERIOD_MAX / 2)

void PWM_Init(void);
void PWM_Start(void);
void PWM_Stop(void);
void PWM_SetDuty(uint16_t u, uint16_t v, uint16_t w);

#endif /* PWM_DRIVER_H */
