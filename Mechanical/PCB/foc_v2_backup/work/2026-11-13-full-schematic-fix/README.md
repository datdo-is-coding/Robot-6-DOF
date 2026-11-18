# Sửa schematic FOC một động cơ — 2026-11-13

Đã áp dụng vào dự án `foc_v2` cho bus danh định **24 V**, dòng pha đỉnh **≤10 A**. Giữ một động cơ, đọc góc MA730 qua SPI3. KiCad đang mở và CubeMX đang mở cần được đóng/mở lại từ file trên đĩa trước khi lưu tiếp, để tránh ghi đè bằng bản còn nằm trong bộ nhớ.

## Thay đổi chính

- Cả 5 sheet: sửa trùng reference, điểm dây lệch lưới, nhãn nguồn và các kết nối phân cấp. Thêm thư viện `foc_v2.kicad_sym` và `sym-lib-table` với kiểu chân điện đúng cho DRV8323RS để ERC phát hiện được lỗi điện.
- MCU: thêm AP2112K-3.3 từ nguồn buck 5 V, nối VBAT, sửa VCAP1/2 thành 2,2 µF low ESR, đầu SWD có 3V3/GND/NRST, thêm RC 100 Ω + 1 nF cho từng ADC dòng pha.
- Công suất: shunt 5 mΩ/3 W/1%, ba pha riêng biệt; nối CAL về PC4, kéo lên SDO open drain và CS, kéo xuống ENABLE/CAL; mỗi MOSFET có điện trở 100 kΩ trực tiếp giữa gate-source. Giữ điện trở gate 2,2 Ω.
- Bus: đầu XT30, cầu chì 10 A/58 V, TVS SMBJ30A, hai tụ 470 µF/50 V (mỗi tụ ripple tối thiểu 1,5 A RMS) và tụ gốm bus 50 V; diode buck SS16/60 V; điện cảm 22 µH có dòng bão hòa tối thiểu 1,5 A. Đo bus bằng 150 kΩ/10 kΩ + 10 nF, 24 V → 1,5 V tại ADC.
- USB-C: hai Rd 5,1 kΩ độc lập, sửa chân shield, bỏ đường cấp ngược VBUS→5 V và pull-up D+ ngoài; dùng termination nội của STM32. Bảo vệ USBLC6 có tụ bypass VBUS. Phát hiện cáp bằng 2N7002, **USB_VBUS tại PA0 tích cực mức thấp**, an toàn khi MCU chưa có nguồn.
- CAN: VCC=5 V, VIO=3,3 V, S=GND; thay các điện trở song song sai bằng split termination 60,4 Ω + 60,4 Ω, 4,7 nF ở điểm giữa. Chỉ nối JP1 khi board nằm ở đầu/cuối bus CAN.
- MA730: bỏ đường ABI/motor 2; SPI3 mode 3, 16 bit, 5,25 MHz và CS có kéo lên 10 kΩ.

## Chân đã đối chiếu trong CubeMX

| Chức năng | Chân STM32F405RG |
|---|---|
| MA730 SPI3 | PB3=SCK, PC11=MISO, PC12=MOSI, PA15=CS |
| DRV8323 SPI1 | PA5=SCK, PB4=MISO, PB5=MOSI, PC10=CS |
| PWM A/B/C | PA8/PA9/PA10; bổ sung PB13/PB14/PB15 |
| Dòng pha A/B/C | PC3/PA3/PA4, ADC injected ranks 1/2/3 |
| Đo điện áp bus | PA6, ADC injected rank 4 |
| Driver ENABLE / nFAULT / CAL | PC9 / PB11 / PC4 |
| CAN RX / TX | PB8 / PB9 |
| USB D− / D+ / phát hiện VBUS | PA11 / PA12 / PA0-WKUP |

`src.ioc` được CubeMX **6.18.1 / DB.6.0.181** nạp và lưu thử thành công qua MCP trước khi sửa chân trên schematic (`cubemx-validation.json`, `valid=true`). TIM1 đặt center aligned, PSC=0, ARR=4199 (~20 kHz), dead time=84 (~500 ns tại 168 MHz), CCR4=2100 để tạo trigger ADC. Hai CS được khởi tạo mức cao.

## Kết quả kiểm tra

- ERC của bản đã áp dụng: **0 lỗi, 0 cảnh báo trên cả 5 sheet**, KiCad CLI 10.0.7; xem `final-erc.json`.
- Netlist của 114 linh kiện đã kiểm tra các nhánh MOSFET, shunt, 6 PWM, SPI, nguồn, USB, CAN, SWD và chia áp bus; xem `check_design.py` và `checks.json`.
- Không thêm ERC exclusion hoặc hạ mức nghiêm trọng của quy tắc. Các mục ignore có sẵn của dự án được giữ nguyên (four-way junction, single global label, SPICE model, footprint filter).
- `before/` chứa bản trước khi sửa; `applied-sha256.json` ghi hash trước/sau. File PCB không thay đổi.

## Khi làm PCB và firmware

Giữ ENABLE thấp đến khi nguồn ổn, kiểm tra SPI/nFAULT, hiệu chuẩn offset CSA rồi mới bật PWM. Cấu hình DRV8323 ở 6-PWM, CSA gain=20 và VREF_DIV=1; với shunt 5 mΩ, hệ số là 0,1 V/A, tâm 1,65 V, ±10 A tương ứng 0,65–2,65 V. Giới hạn dòng đỉnh 10 A phải được thực hiện trong firmware; điện trở shunt không tự giới hạn dòng.

Firmware chỉ kết nối pull-up USB nội khi PA0 `USB_VBUS=0` và ngắt khi cáp mất VBUS. IOC mới xác nhận cấu hình chân; chưa thêm phần xử lý trạng thái này hoặc thuật toán FOC vào firmware.

Nguồn bus cần hấp thụ được năng lượng tái sinh, hoặc phải có mạch hãm ngoài phù hợp với động cơ/quán tính tải. TVS bảo vệ xung, không thay thế điện trở hãm cho tái sinh kéo dài. PCB cần Kelvin cho shunt, vòng gate/nguồn ngắn, tản nhiệt MOSFET và kiểm tra DRC sau khi cập nhật từ schematic. **Chưa xác nhận vận hành bằng phần cứng hoặc thử tải.**

## Tài liệu đối chiếu

- [ST AN4488: phần cứng STM32F4](https://www.st.com/resource/en/application_note/an4488-getting-started-with-stm32f4xxxx-mcu-hardware-development-stmicroelectronics.pdf)
- [ST AN4879: phần cứng USB STM32](https://www.st.com/resource/en/application_note/an4879-usb-hardware-design-guidelines-for-stm32-microcontrollers-stmicroelectronics.pdf)
- [TI DRV8323](https://www.ti.com/lit/ds/symlink/drv8323.pdf), [TI CSD18532Q5B](https://www.ti.com/lit/ds/symlink/csd18532q5b.pdf)
- [Diodes AP2112](https://www.diodes.com/datasheet/download/AP2112.pdf), [NXP TJA1051](https://www.nxp.com/docs/en/data-sheet/TJA1051.pdf)
