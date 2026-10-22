# DEVLOG - NHẬT KÝ TIẾN ĐỘ PHÁT TRIỂN DỰ ÁN ĐỒ ÁN 2

* **Tên đề tài:** Nghiên cứu Framework Odoo và phát triển Module quản lý chấm công
* **Mã đề tài:** Workforce Operations & Attendance Management System
* **Sinh viên thực hiện:** Lê Hồng Phước
* **Mã số sinh viên:** 2374801030058
* **Giảng viên hướng dẫn:** Bộ môn Công nghệ Phần mềm
* **Nền tảng:** Odoo 17.0 Community Edition (Python 3.11, PostgreSQL 16, Ubuntu 22.04 LTS / WSL 2)
* **Kho lưu trữ mã nguồn:** [GitHub Repository](https://github.com/noodphuoc/odoo17-attendance-management)

---

## [TUẦN 1] (08/09/2026 – 14/09/2026): Khảo Sát Nghiệp Vụ & Đề Cương Dự Án
- **Mục tiêu:** Xác định bài toán, khảo sát thực tế và lập đề cương đồ án.
- **Công việc thực hiện:**
  - Khảo sát các quy trình chấm công thực tế tại doanh nghiệp (ghi nhận vào/ra, tính công, đi muộn, nghỉ phép).
  - Tìm hiểu tổng quan về hệ thống hoạch định nguồn lực doanh nghiệp (ERP) và nền tảng mã nguồn mở Odoo.
  - Soạn thảo và thông qua đề cương chi tiết: *"Mô tả đề án – Đồ án Lập trình 2"* với 18 mục tiêu và phạm vi cụ thể.
- **Kết quả bàn giao:** Bản đề cương mô tả đề án chi tiết (file `.docx`).

---

## [TUẦN 2] (15/09/2026 – 21/09/2026): Phân Tích Yêu Cầu & Kịch Bản Nghiệp Vụ
- **Mục tiêu:** Đặc tả chức năng hệ thống theo chuẩn công nghệ phần mềm.
- **Công việc thực hiện:**
  - Xác định 3 nhóm tác nhân chính:
    1. **Nhân viên:** Chấm công cá nhân, theo dõi lịch sử làm việc của bản thân.
    2. **Quản lý / HR:** Quản lý hồ sơ nhân sự, giám sát ca làm việc, xem xét ngoại lệ.
    3. **Quản trị viên (Admin):** Toàn quyền cấu hình, giám sát 24/7 và trích xuất báo cáo.
  - Xây dựng các kịch bản nghiệp vụ chấm công cốt lõi: Đúng giờ (trước 08:00), Đi muộn (sau 08:00), Đang làm việc (chưa check-out), Hoàn thành ca làm.
- **Kết quả bàn giao:** Tài liệu đặc tả yêu cầu chức năng (SRS) và biểu đồ Use Case.

---

## [TUẦN 3] (22/09/2026 – 28/09/2026): Thiết Kế Kiến Trúc & Cơ Sở Dữ Liệu
- **Mục tiêu:** Thiết kế mô hình dữ liệu quan hệ và kiến trúc module Odoo.
- **Công việc thực hiện:**
  - Thiết kế sơ đồ quan hệ thực thể (ERD) quan hệ 1 – N:
    - Model `attendance.employee` (1): Lưu thông tin hồ sơ nhân sự.
    - Model `attendance.record` (N): Lưu lịch sử giao dịch chấm công từng ngày.
  - Thiết kế cấu trúc thư mục module Odoo chuẩn: `models/`, `views/`, `security/`, `reports/`, `tests/`.
  - Hoạch định các ràng buộc dữ liệu:
    - *SQL Constraints:* Đảm bảo mã nhân viên (`employee_code`) là duy nhất trên toàn hệ thống.
    - *Python Constraints:* Ràng buộc logic thời gian (giờ ra phải sau giờ vào).
- **Kết quả bàn giao:** Sơ đồ CSDL (ERD) và bản thiết kế cấu trúc module.

---

## [TUẦN 4] (29/09/2026 – 05/10/2026): Thiết Lập Môi Trường Phát Triển (Dev Environment)
- **Mục tiêu:** Cài đặt toàn bộ môi trường lập trình và chạy thử Odoo server.
- **Công việc thực hiện:**
  - Kích hoạt nền tảng ảo hóa và cài đặt môi trường **WSL 2 (Ubuntu Linux)** trên Windows.
  - Cài đặt hệ quản trị cơ sở dữ liệu **PostgreSQL 16**, tạo tài khoản quản trị `odoo`.
  - Khởi tạo môi trường ảo Python 3.11 (`odoo-env`), cài đặt toàn bộ gói phụ thuộc (`psycopg2`, `lxml`, `openblas`,...).
  - Cài đặt công cụ biên dịch báo cáo **wkhtmltopdf 0.12.6.1**.
  - Thiết lập file cấu hình `odoo.conf`, kết nối database `attendance_db` và chạy Odoo 17 Community trên cổng `8069`.
  - Cấu hình IDE Visual Studio Code với các extension chuyên dụng (Python, Odoo Snippets, XML Tools).
- **Kết quả bàn giao:** Môi trường Odoo 17 chạy ổn định tại `http://localhost:8069`.

---

## [TUẦN 5] (06/10/2026 – 12/10/2026): Khởi Tạo Module & Xây Dựng Backend Core (Python)
- **Mục tiêu:** Lập trình các Model dữ liệu và thuật toán xử lý thời gian.
- **Công việc thực hiện:**
  - Sử dụng lệnh `odoo-bin scaffold` khởi tạo module `attendance_management`.
  - Lập trình file `models/employee.py`: Khai báo các trường thông tin nhân viên, phòng ban, chức vụ, trạng thái và liên kết tài khoản người dùng (`user_id`).
  - Lập trình file `models/attendance.py`:
    - Xử lý thuật toán tính tổng giờ làm việc tự động (`_compute_work_hours`).
    - Xử lý bài toán múi giờ: Chuyển đổi giờ UTC lưu trong DB sang giờ địa phương Việt Nam (UTC+7 / `Asia/Ho_Chi_Minh`) để kiểm tra chính xác đi muộn sau 08:00 sáng.
  - Khởi tạo kho lưu trữ Git cục bộ, cấu hình `.gitignore` và kết nối thành công lên GitHub.
- **Kết quả bàn giao:** Mã nguồn backend cơ bản đã được đẩy lên GitHub.

---

## [TUẦN 6] (13/10/2026 – 19/10/2026): Xây Dựng Giao Diện Người Dùng (XML Views)
- **Mục tiêu:** Thiết kế giao diện trực quan cho cả nhân viên và quản lý.
- **Công việc thực hiện:**
  - Xây dựng `employee_views.xml`: Giao diện Form và Tree view quản lý hồ sơ nhân viên.
  - Xây dựng `attendance_views.xml`:
    - Danh sách chấm công với hệ thống huy hiệu trạng thái màu sắc (`widget="badge"`: Xanh = Đúng giờ, Đỏ = Đi muộn, Vàng = Đang làm việc).
    - Tích hợp biểu đồ cột (**Graph View**) và bảng ma trận (**Pivot View**) phân tích tổng số giờ làm theo phòng ban.
  - Xây dựng `menu_views.xml`: Hệ thống thanh điều hướng phân cấp chức năng rõ ràng.
- **Kết quả bàn giao:** Giao diện người dùng đầy đủ các chế độ xem Tree, Form, Graph, Pivot.

---

## [TUẦN 7] (20/10/2026 – 22/10/2026) [HIỆN TẠI]: Tái Cấu Trúc Vận Hành, Dashboard KPI, Báo Cáo PDF & Unit Test
- **Mục tiêu:** Tái định vị sản phẩm thành "Bảng điều khiển vận hành nhân sự", chuẩn hóa nghiệp vụ doanh nghiệp và hoàn thiện kiểm thử.
- **Công việc thực hiện:**
  1. **Bảo mật & Phân quyền đa cấp (Security):**
     - Thiết lập 3 nhóm bảo mật: *Nhân viên*, *Quản lý / HR*, *Quản trị viên (Admin)*.
     - Cấu hình **Record Rules**: Nhân viên chỉ đọc/sửa dữ liệu chấm công và hồ sơ của chính mình (bảo mật tuyệt đối SĐT, email đồng nghiệp).
     - Tách quyền Admin: Admin là vai trò giám sát vận hành 24/7, không bị ép phải thực hiện Check-in/Check-out.
  2. **Báo cáo PDF QWeb chuyên nghiệp:**
     - Xây dựng template in Bảng chấm công chi tiết ra file **PDF (QWeb Report)** chuẩn hành chính có chữ ký Người lập biểu và Trưởng phòng nhân sự.
  3. **Refactor nghiệp vụ & Bắt lỗi hệ thống:**
     - Bổ sung `@api.constrains`: Chặn tuyệt đối việc đổi trạng thái nhân viên sang "Đã nghỉ việc" khi đang còn ca làm dở dang chưa checkout.
     - Xử lý triệt để bài toán ca làm việc vắt qua nửa đêm (Midnight shift) và khai báo đầy đủ `@api.depends`.
  4. **Workforce Operations Dashboard (Giao diện vận hành thời gian thực):**
     - Xây dựng model `attendance.dashboard` và giao diện `dashboard_views.xml`.
     - Tích hợp **4 thẻ chỉ số KPI tương tác**: *Tổng nhân sự*, *Đang có mặt*, *Đi muộn hôm nay*, *Chưa đến / Vắng mặt*.
     - Thuật toán tự động tìm ra danh sách những nhân viên chưa hề quẹt thẻ trong ngày (giải quyết bài toán đếm người vắng mặt).
     - Tích hợp nút in nhanh PDF trực tiếp trên đầu Dashboard.
  5. **Kiểm thử tự động (Automated Unit Testing):**
     - Xây dựng bộ ca kiểm thử trong thư mục `tests/test_attendance.py`:
       - `test_01_create_employee`: Kiểm tra tính toàn vẹn khi tạo hồ sơ.
       - `test_02_work_hours_computation`: Kiểm tra độ chính xác thuật toán tính 9.0 giờ làm.
       - `test_03_prevent_resigned_with_open_checkin`: Kiểm tra ràng buộc chặn nghỉ việc khi ca đang mở.
     - Kết quả chạy Odoo Test Runner: **3 post-tests ran, 0 failed, 0 error(s) -> Đạt 100%**.
  6. **Nhập liệu & Giả lập quy mô lớn (Batch Seeding):**
     - Nạp thành công **143 nhân sự** từ file `danh_sach_nhan_vien_150.csv` theo 4 phòng ban.
     - Giả lập hơn **500 bản ghi chấm công thực tế** trong tuần phục vụ phân tích biểu đồ và ma trận.
  7. **Tài liệu hóa dự án:**
     - Soạn thảo trang `README.md` và nhật ký `DEVLOG.md` chuẩn kỹ thuật.
- **Đánh giá tiến độ Tuần 7:** **HOÀN THÀNH 100% MỤC TIÊU VÀ VƯỢT TIẾN ĐỘ ĐỀ RA.**

---

## KẾ HOẠCH DỰ KIẾN (TUẦN 8 – TUẦN 15)

* **Tuần 8:** Bắt đầu soạn thảo Chương 1 (Tổng quan đề tài & Odoo) và Chương 2 (Phân tích thiết kế hệ thống) trong file Báo cáo Word.
* **Tuần 9:** Hoàn thiện bảng phân tích hiệu suất và xuất dữ liệu chấm công phục vụ tính lương.
* **Tuần 10:** Lập bảng ma trận Test Case kiểm thử thủ công và chụp ảnh kết quả đưa vào báo cáo.
* **Tuần 11 – 12:** Soạn thảo Chương 3 (Hiện thực hóa hệ thống & Thuật toán) và Chương 4 (Kiểm thử & Đánh giá kết quả).
* **Tuần 13:** Viết Chương 5 (Kết luận & Hướng phát triển), rà soát định dạng, mục lục, tài liệu tham khảo theo quy chuẩn đồ án của trường.
* **Tuần 14:** Thiết kế Slide thuyết trình PowerPoint (15 – 20 slide) và kịch bản demo trước hội đồng.
* **Tuần 15:** Tổng duyệt, chuẩn bị câu hỏi phản biện và bảo vệ đồ án tốt nghiệp.