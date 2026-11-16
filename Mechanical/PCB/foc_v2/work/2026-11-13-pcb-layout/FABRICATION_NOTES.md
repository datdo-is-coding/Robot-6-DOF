FOC v2 — yêu cầu gia công PCB, 2026-11-14

- PCB tròn Ø70 mm; 4 lớp, dày danh nghĩa 1,6 mm; đồng hoàn thiện 70 µm (2 oz) trên cả 4 lớp; ENIG. Stackup danh nghĩa: Cu 0,07 / dielectric 0,20 / Cu 0,07 / dielectric 0,90 / Cu 0,07 / dielectric 0,20 / Cu 0,07 mm, cộng hai lớp soldermask 0,01 mm.
- Track/space tối thiểu 0,15/0,15 mm; copper–edge ≥0,5 mm. Via tín hiệu Ø0,4/lỗ hoàn thiện Ø0,2 mm, annular ring ≥0,1 mm. Via công suất Ø0,8/lỗ Ø0,4 mm; giữ nguyên các mảng 9 via song song.
- **10 via trong `VIPPO_REQUIRED.csv` bắt buộc resin fill và copper cap.** Không thay bằng via hở hoặc chỉ tent bằng soldermask. Các via này cũng đã có thuộc tính filling/capping trong file KiCad.
- Tọa độ CSV là mm tuyệt đối theo KiCad; tâm PCB và trục MA730 ở (100, 100). Đối chiếu cùng gốc tọa độ với dữ liệu khoan khi CAM dịch gốc.
- 4 lỗ NPTH Ø2,7 mm trên vòng Ø26 mm, chọn cho vít M2.5; góc lỗ 45°/135°/225°/315°. MA730 nằm chính tâm mặt dưới. Cần đối chiếu cỡ vít, trụ đệm, chiều cao nam châm và phần chân linh kiện xuyên lỗ với motor thực tế.

Đây là cấu hình cần xưởng xác nhận đồng thời về stackup 2 oz, track/space và via fill/cap. Chưa đặt gia công. Tham chiếu khả năng quy trình nâng cao: [PCBWay Advanced](https://www.pcbway.com/advanced-pcb-capabilities.html); đây không phải xác nhận báo giá hoặc DFM của xưởng cho board này.

ERC và DRC đã sạch trên dữ liệu thiết kế; chưa thử mẫu thật, nhiệt ở dòng tải hoặc khoảng hở/độ mạnh nam châm.
