# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import pytz

class AttendanceRecord(models.Model):
    _name = 'attendance.record'
    _description = 'Bản ghi chấm công'
    _order = 'check_in desc'

    employee_id = fields.Many2one('attendance.employee', string='Nhân viên', required=True, ondelete='cascade')
    department = fields.Selection(related='employee_id.department', string='Phòng ban', store=True)
    date = fields.Date(string='Ngày', default=fields.Date.context_today, required=True)
    check_in = fields.Datetime(string='Giờ vào', default=fields.Datetime.now, required=True)
    check_out = fields.Datetime(string='Giờ ra')
    work_hours = fields.Float(string='Tổng giờ làm', compute='_compute_work_hours', store=True)
    status = fields.Selection([
        ('on_time', 'Đúng giờ'),
        ('late', 'Đi muộn'),
        ('working', 'Đang làm việc'),
        ('completed', 'Đã hoàn thành')
    ], string='Trạng thái', compute='_compute_status', store=True)

    # 1. Tính tổng thời gian làm việc
    @api.depends('check_in', 'check_out')
    def _compute_work_hours(self):
        for rec in self:
            if rec.check_in and rec.check_out:
                delta = rec.check_out - rec.check_in
                rec.work_hours = round(delta.total_seconds() / 3600.0, 2)
            else:
                rec.work_hours = 0.0

    # 2. Xử lý quy tắc nghiệp vụ chấm công theo múi giờ
    @api.depends('check_in', 'check_out')
    def _compute_status(self):
        for rec in self:
            if not rec.check_in:
                rec.status = 'working'
                continue

            # Quy đổi giờ UTC của Odoo sang múi giờ người dùng (hoặc mặc định GMT+7)
            user_tz = self.env.user.tz or 'Asia/Ho_Chi_Minh'
            tz = pytz.timezone(user_tz)
            local_check_in = pytz.utc.localize(rec.check_in).astimezone(tz)

            # Quy ước giờ bắt đầu làm việc buổi sáng là 08:00
            is_late = (local_check_in.hour > 8) or (local_check_in.hour == 8 and local_check_in.minute > 5)

            if not rec.check_out:
                rec.status = 'working'
            else:
                rec.status = 'late' if is_late else 'on_time'

    # 3. Ràng buộc toàn vẹn dữ liệu (Bắt lỗi nghiệp vụ)
    @api.constrains('check_in', 'check_out', 'employee_id')
    def _check_attendance_validity(self):
        for rec in self:
            # Ràng buộc: Giờ ra phải sau giờ vào
            if rec.check_in and rec.check_out and rec.check_out <= rec.check_in:
                raise ValidationError('Thời gian Check-out phải diễn ra sau thời gian Check-in!')

            # Ràng buộc: Một nhân viên không thể có 2 ca làm dở dang cùng lúc
            if not rec.check_out:
                open_records = self.search([
                    ('employee_id', '=', rec.employee_id.id),
                    ('check_out', '=', False),
                    ('id', '!=', rec.id)
                ])
                if open_records:
                    raise ValidationError(f'Nhân viên {rec.employee_id.name} đang có một lượt chấm công chưa Check-out. Vui lòng Check-out trước khi chấm công mới!')

    # 4. Action nút bấm Chấm công ra (Check-out)
    def action_check_out(self):
        for rec in self:
            if not rec.check_out:
                rec.check_out = fields.Datetime.now()