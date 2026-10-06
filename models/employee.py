# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class AttendanceEmployee(models.Model):
    _name = 'attendance.employee'
    _description = 'Thông tin nhân viên'
    _order = 'employee_code asc'
    _rec_name = 'name'

    employee_code = fields.Char(string='Mã nhân viên', required=True, copy=False, index=True)
    name = fields.Char(string='Họ và tên', required=True)
    user_id = fields.Many2one('res.users', string='Tài khoản người dùng', help='Liên kết tài khoản Odoo để nhân viên tự đăng nhập chấm công')
    email = fields.Char(string='Email')
    phone = fields.Char(string='Số điện thoại')
    department = fields.Selection([
        ('it', 'Công nghệ thông tin'),
        ('hr', 'Hành chính nhân sự'),
        ('sales', 'Kinh doanh'),
        ('accounting', 'Kế toán'),
    ], string='Phòng ban', default='it', required=True)
    position = fields.Char(string='Chức vụ')
    hire_date = fields.Date(string='Ngày vào làm', default=fields.Date.context_today)
    status = fields.Selection([
        ('working', 'Đang làm việc'),
        ('resigned', 'Đã nghỉ việc')
    ], string='Trạng thái', default='working', required=True)

    attendance_ids = fields.One2many('attendance.record', 'employee_id', string='Lịch sử chấm công')

    _sql_constraints = [
        ('unique_employee_code', 'unique(employee_code)', 'Lỗi: Mã nhân viên phải là duy nhất!')
    ]

    # Kiểm tra ràng buộc Python (OOP Constraints)
    @api.constrains('status')
    def _check_status(self):
        for rec in self:
            if rec.status == 'resigned':
                # Nếu nghỉ việc thì kiểm tra xem còn ca làm dở dang chưa checkout không
                open_attendance = self.env['attendance.record'].search([
                    ('employee_id', '=', rec.id),
                    ('check_out', '=', False)
                ])
                if open_attendance:
                    raise ValidationError(f'Nhân viên {rec.name} vẫn còn lượt chấm công chưa Check-out. Hãy xử lý trước khi chuyển trạng thái nghỉ việc!')