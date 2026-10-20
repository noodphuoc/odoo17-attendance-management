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
    user_id = fields.Many2one('res.users', string='Tài khoản người dùng')
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
    ], string='Trạng thái hồ sơ', default='working', required=True)

    attendance_ids = fields.One2many('attendance.record', 'employee_id', string='Lịch sử chấm công')

    # Trạng thái hiển thị trên Thẻ Chấm công
    attendance_state = fields.Selection([
        ('checked_out', 'Chưa vào làm / Đã tan ca'),
        ('checked_in', 'Đang làm việc')
    ], string='Tình trạng ca làm', compute='_compute_current_attendance', store=False)
    
    current_check_in = fields.Datetime(string='Giờ vào ca hiện tại', compute='_compute_current_attendance')
    today_work_hours = fields.Float(string='Giờ làm hôm nay', compute='_compute_current_attendance')

    _sql_constraints = [
        ('unique_employee_code', 'unique(employee_code)', 'Lỗi: Mã nhân viên phải là duy nhất!')
    ]

    # FIX 1: Chặn đổi trạng thái sang "Đã nghỉ việc" nếu còn ca làm dở dang
    @api.constrains('status')
    def _check_status_resigned(self):
        for emp in self:
            if emp.status == 'resigned':
                open_attendance = self.env['attendance.record'].search([
                    ('employee_id', '=', emp.id),
                    ('check_out', '=', False)
                ], limit=1)
                if open_attendance:
                    raise ValidationError(
                        f"Nhân viên {emp.name} vẫn còn ca chấm công chưa Check-out (từ lúc {open_attendance.check_in.strftime('%d/%m/%Y %H:%M')}). "
                        "Vui lòng hoàn tất Check-out trước khi chuyển trạng thái nghỉ việc!"
                    )

    # FIX 2 & 3: Bổ sung @api.depends và xử lý ca làm việc vắt qua đêm
    @api.depends('attendance_ids.check_in', 'attendance_ids.check_out')
    def _compute_current_attendance(self):
        for emp in self:
            # 1. Tìm ca làm đang mở gần nhất (kể cả check-in từ hôm trước qua đêm)
            open_rec = self.env['attendance.record'].search([
                ('employee_id', '=', emp.id),
                ('check_out', '=', False)
            ], order='check_in desc', limit=1)

            if open_rec:
                emp.attendance_state = 'checked_in'
                emp.current_check_in = open_rec.check_in
                emp.today_work_hours = 0.0
            else:
                emp.attendance_state = 'checked_out'
                # Nếu đã checkout, lấy ca làm gần nhất trong ngày hôm nay để xem số giờ
                today = fields.Date.context_today(self)
                today_closed_rec = self.env['attendance.record'].search([
                    ('employee_id', '=', emp.id),
                    ('date', '=', today),
                    ('check_out', '!=', False)
                ], order='check_out desc', limit=1)
                
                emp.current_check_in = today_closed_rec.check_in if today_closed_rec else False
                emp.today_work_hours = today_closed_rec.work_hours if today_closed_rec else 0.0

    # Chấm công vào
    def action_btn_check_in(self):
        self.ensure_one()
        open_rec = self.env['attendance.record'].search([
            ('employee_id', '=', self.id),
            ('check_out', '=', False)
        ], limit=1)
        if open_rec:
            raise ValidationError(f"Bạn đang trong một ca làm việc (từ {open_rec.check_in.strftime('%H:%M')}), chưa thể Check-in tiếp!")
        
        self.env['attendance.record'].create({
            'employee_id': self.id,
            'date': fields.Date.context_today(self),
            'check_in': fields.Datetime.now(),
        })

    # Chấm công ra
    def action_btn_check_out(self):
        self.ensure_one()
        open_rec = self.env['attendance.record'].search([
            ('employee_id', '=', self.id),
            ('check_out', '=', False)
        ], order='check_in desc', limit=1)
        if not open_rec:
            raise ValidationError("Bạn chưa thực hiện Check-in ca làm nào!")
        
        open_rec.action_check_out()

    # Mở màn hình điểm danh cá nhân
    @api.model
    def action_open_my_attendance(self):
        emp = self.search([('user_id', '=', self.env.uid)], limit=1)
        if not emp:
            raise ValidationError("Tài khoản của bạn chưa được liên kết với hồ sơ Nhân viên nào trong hệ thống! Vui lòng liên hệ HR.")
        
        return {
            'name': 'Chấm công hôm nay',
            'type': 'ir.actions.act_window',
            'res_model': 'attendance.employee',
            'view_mode': 'form',
            'res_id': emp.id,
            'view_id': self.env.ref('attendance_management.view_my_attendance_card').id,
            'target': 'current',
        }