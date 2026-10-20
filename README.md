# Module Quản Lý Chấm Công - Odoo 17 Community

> **Đồ án Lập trình 2**  
> **Sinh viên thực hiện:** Lê Hồng Phước  
> **Mã sinh viên:** 2374801030058  
> **Nền tảng:** Odoo 17.0 Community Edition (Python 3.11, PostgreSQL 16)

---

## 1. Giới thiệu đề tài
Module **Attendance Management** được xây dựng nhằm nghiên cứu kiến trúc Framework Odoo, cơ chế ORM, XML Views, Security Record Rules và quy trình quản lý thời gian làm việc của nhân viên trong doanh nghiệp thực tế.

## 2. Các chức năng chính
* **Quản lý thông tin nhân viên:** Quản lý mã NV, họ tên, phòng ban, chức vụ, trạng thái hồ sơ, ràng buộc toàn vẹn dữ liệu.
* **Ghi nhận chấm công thông minh:**
  * Tự động nhận diện nhân viên đăng nhập, tính tổng giờ làm việc.
  * Tự động xác định trạng thái ca làm: *Đúng giờ, Đi muộn, Đang làm việc, Hoàn thành*.
  * Xử lý chính xác múi giờ Việt Nam (UTC+7) và ca làm việc vắt qua đêm.
* **Bảo mật & Phân quyền đa cấp:**
  * **Nhân viên:** Chỉ xem hồ sơ cá nhân và lịch sử chấm công của chính mình (Record Rules).
  * **Quản lý / HR & Admin:** Theo dõi chấm công toàn công ty 24/7, quản lý nhân sự, xem dashboard phân tích.
* **Báo cáo & Thống kê:**
  * Dashboard ma trận Pivot và Biểu đồ Graph phân tích giờ làm theo phòng ban.
  * Xuất Báo cáo chấm công chi tiết dạng **PDF (QWeb Report)** có chữ ký xác nhận của Người lập biểu và Trưởng phòng nhân sự.
* **Kiểm thử tự động (Unit Testing):**
  * Tích hợp bộ kiểm thử `tests/test_attendance.py` kiểm tra logic tính giờ và ràng buộc trạng thái.

## 3. Cấu trúc thư mục
```text
attendance_management/
├── models/             # Định nghĩa Object ORM (employee, attendance)
├── views/              # Giao diện Tree, Form, Search, Graph, Pivot
├── security/           # Nhóm quyền và Record Rules bảo mật
├── tests/              # Ca kiểm thử tự động (Unit tests)
├── DEVLOG.md           # Nhật ký tiến độ phát triển
├── __init__.py
└── __manifest__.py