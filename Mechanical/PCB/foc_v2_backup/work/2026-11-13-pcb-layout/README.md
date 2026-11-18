PCB FOC v2 — bản layout hoàn chỉnh

Thiết kế cho bus 24 V, dòng pha đỉnh mục tiêu ≤10 A. PCB tròn Ø70 mm, 4 lớp; 4 lỗ Ø2,7 mm trên PCD Ø26 mm. MA730 dùng SPI, ở đúng tâm mặt dưới. Đường kính Ø70 mm dành chỗ cho XT30, cầu chì và hai tụ bulk Ø10 mm đang có trong thiết kế.

Đã đi đủ dây, nối các vùng GND, dùng sáu net tie để lấy tín hiệu Kelvin tại shunt và giữ đường công suất rộng cùng 81 via Ø0,8/0,4 mm. Bus 24 V trước cầu chì được đi lại ở mặt dưới, rộng 3 mm, để thoát GND của LDO. Không đổi chân MCU trong bước PCB; `src.ioc` giữ nguyên byte.

KiCad kiểm tra: ERC 0 trên toàn bộ 5 sheet; DRC 0, kết nối hở 0, sai khác PCB–schematic 0. Báo cáo và hash ở `final-erc.json`, `final-drc.json`, `final-checks.json`; kiểm tra sau khi đưa vào dự án ở `published-drc.json`.

Ảnh bố trí: `PCB_TOP.png`, `PCB_BOTTOM.png`. Một số model 3D của connector/IC chưa có trên máy nên ảnh có thể chỉ hiện pad; dữ liệu footprint vẫn có trong PCB. Ảnh 3D không xác nhận được khoảng hở cơ khí với motor.

**Gia công cần theo `FABRICATION_NOTES.md` và `VIPPO_REQUIRED.csv`, gồm 10 via resin fill + copper cap.** Lỗ Ø2,7 mm chọn cho M2.5; cần kiểm tra kích thước vít và chiều cao lắp thực tế. Chưa thử mẫu thật hoặc xác nhận nhiệt/dòng 10 A và khe hở nam châm.

File dự án chính nằm ở thư mục `foc_v2` phía trên `work`. `before/` giữ bản đầu tác vụ; `before-publish-live/` giữ bản PCB trống và project KiCad vừa được lưu; `publish-backup/` giữ các file ngay trước khi thay thế. Mở lại PCB trong KiCad để nạp dữ liệu mới và tránh lưu đè từ cửa sổ PCB trống cũ.
