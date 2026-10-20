# DEVLOG - NHẬT KÝ PHÁT TRIỂN MODULE ATTENDANCE MANAGEMENT

## Tuần 1 - Tuần 4: Khảo sát & Chuẩn bị Môi trường
- **Công việc:** Nghiên cứu kiến trúc Odoo 17, thiết lập môi trường WSL 2 Ubuntu, PostgreSQL 16.
- **Kết quả:** Chạy thành công Odoo core, tạo cấu trúc module `attendance_management`.

## Tuần 5: Xây dựng Model Cơ sở dữ liệu
- **Công việc:** Xây dựng `attendance.employee` và `attendance.record`, thiết kế quan hệ 1-N.
- **Kết quả:** Migrate schema thành công vào database PostgreSQL.

## Tuần 6: Xây dựng Views & Giao diện Chấm công
- **Công việc:** Viết Form, Tree, Search view. Thiết kế thẻ điểm danh nhanh với nút Check-in/Check-out lớn.
- **Kết quả:** Hoàn thành giao diện chấm công một chạm không cần qua nút lưu đám mây.

## Tuần 7: Phân quyền & Báo cáo PDF QWeb
- **Công việc:** 
  - Tạo 3 nhóm bảo mật: Employee, HR, Admin.
  - Cấu hình Record Rules: Phân tách dữ liệu cá nhân giữa nhân viên và quản lý.
  - Viết template QWeb xuất báo cáo chấm công PDF có xác nhận chữ ký.
- **Commit:** `feat: implement security groups, record rules and QWeb PDF report`

## Kế hoạch Tuần 8:
- [ ] Fix ca làm việc qua đêm và ràng buộc trạng thái nghỉ việc.
- [ ] Thêm Unit Tests trong thư mục `tests/`.
- [ ] Soạn thảo README.md mô tả dự án.