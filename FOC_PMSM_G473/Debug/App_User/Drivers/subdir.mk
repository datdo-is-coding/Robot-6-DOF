################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (13.3.rel1)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../App_User/Drivers/drv83xx.c \
../App_User/Drivers/mt6701.c 

OBJS += \
./App_User/Drivers/drv83xx.o \
./App_User/Drivers/mt6701.o 

C_DEPS += \
./App_User/Drivers/drv83xx.d \
./App_User/Drivers/mt6701.d 


# Each subdirectory must supply rules for building sources it contributes
App_User/Drivers/%.o App_User/Drivers/%.su App_User/Drivers/%.cyclo: ../App_User/Drivers/%.c App_User/Drivers/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m4 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32G473xx -c -I../USB_Device/App -I../USB_Device/Target -I../Core/Inc -I../Drivers/STM32G4xx_HAL_Driver/Inc -I../Drivers/STM32G4xx_HAL_Driver/Inc/Legacy -I../Middlewares/ST/STM32_USB_Device_Library/Core/Inc -I../Middlewares/ST/STM32_USB_Device_Library/Class/CDC/Inc -I../Drivers/CMSIS/Device/ST/STM32G4xx/Include -I../Drivers/CMSIS/Include -I"/home/tuan/STM32CubeIDE/workspace_1.19.0/FOC_PMSM_G473/App_User" -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-App_User-2f-Drivers

clean-App_User-2f-Drivers:
	-$(RM) ./App_User/Drivers/drv83xx.cyclo ./App_User/Drivers/drv83xx.d ./App_User/Drivers/drv83xx.o ./App_User/Drivers/drv83xx.su ./App_User/Drivers/mt6701.cyclo ./App_User/Drivers/mt6701.d ./App_User/Drivers/mt6701.o ./App_User/Drivers/mt6701.su

.PHONY: clean-App_User-2f-Drivers

