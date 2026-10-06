# -*- coding: utf-8 -*-
{
    'name': "Quản lý Chấm công (Attendance Management)",
    'summary': "Module quản lý nhân viên và chấm công theo thời gian thực",
    'description': """
        Đồ án Lập trình 2:
        - Quản lý hồ sơ nhân viên
        - Ghi nhận Check-in / Check-out tự động
        - Tự động tính toán tổng giờ làm và trạng thái đi muộn
        - Phân quyền người dùng (Admin, HR, Nhân viên)
        - Biểu đồ thống kê và Dashboard phân tích
    """,
    'author': "Lê Hồng Phước",
    'category': 'Human Resources',
    'version': '17.0.1.0.0',
    'depends': ['base', 'web'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/employee_views.xml',
        'views/attendance_views.xml',
        'views/menu_views.xml',
        'views/attendance_report.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}