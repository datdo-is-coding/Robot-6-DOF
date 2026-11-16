# FOC BLDC một động cơ — MA730 đọc góc bằng SPI

Ngày thực hiện: 13/11/2026. Dự án: `foc_v2`. MCU: STM32F405RGT6, LQFP64.

Đã cập nhật trực tiếp `src.ioc`, `MCU.kicad_sch`, `hall.kicad_sch` và `foc_v2.kicad_sch`. Phương án chân đã được CubeMX 6.17.0 nạp/lưu và xác thực trước khi tạo các thay đổi schematic. Các chỉnh sửa người dùng vừa lưu trước khi thực hiện được giữ trong thư mục `saved-before/`.

## Cấu hình cuối

| Chức năng | Chân STM32 | Số chân LQFP64 | Đích MA730 |
|---|---|---:|---|
| SPI3 SCK | PB3 | 55 | SCLK, chân 12 |
| SPI3 MISO | PC11 | 52 | MISO, chân 7 |
| SPI3 MOSI | PC12 | 53 | MOSI, chân 4 |
| GPIO chip select | PA15 | 50 | CS, chân 5 |

SPI3 chạy master full duplex, mode 3 (CPOL=1, CPHA=1), 16 bit, MSB trước, 5.25 MHz. PA15 khởi tạo mức cao, có pull-up; CS chủ động mức thấp. Đã thêm `MX_SPI3_Init` vào danh sách khởi tạo trong IOC. Chưa sinh mã firmware.

MA730 giữ tụ 1 µF, nguồn 3.3 V, TEST và pad nối GND. Các đầu ra ABZ/PWM và giao tiếp SSI không dùng được đánh dấu no-connect. Không dùng `SSCK`/`SSD` làm chân SPI; chỉ còn bốn tín hiệu SPI giữa sheet HALL và MCU.

SPI1 tiếp tục phục vụ DRV8323: PA5–SCK, PB4–MISO, PB5–MOSI, PC10–CS. Sửa nối đảo MISO/MOSI tại sheet tổng. Tốc độ SPI1 giảm từ 21 MHz xuống 5.25 MHz, đáp ứng chu kỳ SCLK tối thiểu 100 ns của DRV8323. PC10 cũng khởi tạo mức cao.

Tại sheet tổng, đã sửa nối CAN cho đúng cấu hình CubeMX: PB8/CAN1_RX nối RXD của TJA1051, PB9/CAN1_TX nối TXD. Sheet phần cứng communication được giữ nguyên.

Đã bỏ các cổng, nhãn và dây MCU dành cho motor 2: PWM2, ISENSE2, ENCD2, EN_GATE2, NFAULT2 và chip select thứ hai. PC11 và PC12 được dùng cho SPI3. Các chân còn lại được giải phóng và đánh dấu no-connect; bỏ ABI của encoder 1. Giữ nguyên TIM1 sáu PWM, ba ngõ đo dòng, ADC điện áp, USB, CAN và SWD.

## Bằng chứng kiểm tra

- `cubemx-stage-final.json`: MCP áp dụng phương án SPI mới trên bản sao; `cubemx_validated=true`. CubeMX giữ đủ các chân và tham số SPI3 sau khi nạp/lưu.
- `cubemx-stage-init.json`: MCP xác thực việc thêm `MX_SPI3_Init`; SHA-256 của IOC này trùng file `src.ioc` đã áp dụng.
- `cubemx-final.json`: MCP đọc lại IOC thực tế sau khi cập nhật, nhận đủ SPI1 và SPI3 cùng bốn chân MA730.
- `verification.json`: 21 kết nối quan trọng được kiểm tra bằng netlist do KiCad CLI xuất; kiểm tra thêm 14 chân MCU và 6 chân MA730 không dùng, đồng thời xác nhận không còn nhãn ABI/motor 2.
- `kicad-final.json`: MCP KiCad đọc lại netlist từ schematic thực tế thành công. Tự động reload schematic không được KiCad 10 hỗ trợ.
- `applied-changes.json`: SHA-256 trước/sau, danh sách file cập nhật và file được giữ nguyên.
- `schematic-overview.png`: bản xem trước sheet tổng sau sửa. Các SVG đầy đủ ở `candidate-svg/`.

ERC trước sửa: **16 lỗi, 120 cảnh báo**. Sau sửa: **3 lỗi, 97 cảnh báo**. Không có lỗi ERC mới. Ba lỗi còn lại đều có từ bản ban đầu:

1. `PV_SENSE` ở sheet tổng chưa nối nguồn đo điện áp.
2. Hai lỗi input power chưa được output power điều khiển, liên quan các symbol +3V3 `#PWR01` và `#PWR05` trong MCU.

KiCad vẫn báo annotation chưa hợp lệ; các cảnh báo cũ về grid, thư viện, footprint và dây hở cũng còn trong dự án. Báo cáo này xác nhận phạm vi đổi SPI/bỏ motor 2, chưa xác nhận toàn bộ mạch sẵn sàng sản xuất hoặc vận hành động cơ.

## Mở lại và khôi phục

Trong cửa sổ KiCad đang mở, chọn **File → Revert** để nạp thay đổi từ đĩa; CubeMX cần mở lại `src.ioc`. KiCad 10 không hỗ trợ reload schematic bằng MCP, nên thao tác này chưa được tự động hóa.

Bản sao lưu đúng thời điểm người dùng xác nhận đã lưu nằm trong `saved-before/`. Chỉ bốn file nêu trên được thay đổi; PCB, project KiCad, phần công suất `gatedrv.kicad_sch` và sheet `communication.kicad_sch` giữ nguyên theo SHA-256. Chưa cập nhật PCB, sinh code, build hay thử phần cứng.

## Tài liệu đối chiếu

- [MPS MA730 datasheet Rev. 1.1](https://www.monolithicpower.com/en/documentview/productdocument/index/version/2/document_type/Datasheet/lang/en/sku/MA730/document_id/3563), trang 8, 11–12: chân SPI/SSI, kéo nội, mode 0/3, khung 16 bit và giới hạn SCLK.
- [ST STM32F405/407 datasheet](https://www.st.com/resource/en/datasheet/stm32f405rg.pdf) và cơ sở dữ liệu MCU cục bộ `/home/tuan/STM32CubeMX/db/mcu/STM32F405RGTx.xml`: đối chiếu chức năng chân SPI3. Các chân cũng đã được CubeMX kiểm tra nạp/lưu.
- [TI DRV8323 datasheet](https://www.ti.com/lit/ds/symlink/drv8323.pdf), mục 7.6: chu kỳ SCLK tối thiểu 100 ns.
