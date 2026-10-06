# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class AttendanceKioskWizard(models.TransientModel):
    _name = 'attendance.kiosk.wizard'
    _description = 'Wizard Chấm công nhanh Kiosk'

    employee_id = fields.Many2one(
        'attendance.employee', 
        string='Chọn nhân viên', 
        domain=[('status', '=', 'working')],
        help='Chọn tên nhân viên đang làm việc tại công ty'
    )
    employee_code = fields.Char(
        string='Hoặc nhập Mã nhân viên', 
        placeholder='Ví dụ: NV01'
    )

    def action_confirm_attendance(self):
        self.ensure_one()
        employee = False

        # 1. Tìm nhân viên theo Mã NV nhập vào hoặc theo ô Chọn nhân viên
        if self.employee_code:
            employee = self.env['attendance.employee'].search([
                ('employee_code', '=ilike', self.employee_code.strip()),
                ('status', '=', 'working')
            ], limit=1)
            if not employee:
                raise ValidationError(f"Không tìm thấy nhân viên đang làm việc có mã '{self.employee_code}'!")
        elif self.employee_id:
            employee = self.employee_id
        else:
            raise ValidationError("Vui lòng chọn nhân viên hoặc nhập mã nhân viên để chấm công!")

        # 2. Kiểm tra xem nhân viên này có ca làm dở dang (chưa Check-out) hay không
        Attendance = self.env['attendance.record']
        open_record = Attendance.search([
            ('employee_id', '=', employee.id),
            ('check_out', '=', False)
        ], limit=1)

        # 3. Phân luồng tự động Check-in / Check-out
        if open_record:
            # Thực hiện Check-out
            open_record.action_check_out()
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Tạm biệt & Hẹn gặp lại!',
                    'message': f"Nhân viên {employee.name} đã Check-out thành công. Tổng thời gian hôm nay: {open_record.work_hours} giờ.",
                    'type': 'warning',
                    'sticky': False,
                    'next': {'type': 'ir.actions.act_window_close'}
                }
            }
        else:
            # Thực hiện Check-in mới
            new_record = Attendance.create({
                'employee_id': employee.id,
                'date': fields.Date.context_today(self),
                'check_in': fields.Datetime.now(),
            })
            status_text = "Đúng giờ" if new_record.status == 'on_time' else "Đi muộn"
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Xin chào buổi sáng!',
                    'message': f"Nhân viên {employee.name} đã Check-in thành công ({status_text}). Chúc bạn một ngày làm việc hiệu quả!",
                    'type': 'success',
                    'sticky': False,
                    'next': {'type': 'ir.actions.act_window_close'}
                }
            }