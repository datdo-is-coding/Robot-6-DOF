#ifndef TELEMETRY_H
#define TELEMETRY_H

#include "main.h"

void Telemetry_Init(void);
void Telemetry_Send(float actual_pos, float target_pos, float velocity,
                    float vq);
void Telemetry_ProcessRxByte(uint8_t ch);
void Telemetry_Task(void);

#endif /* TELEMETRY_H */
