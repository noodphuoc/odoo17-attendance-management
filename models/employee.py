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

    # Các trường hiển thị trên Thẻ Chấm công hôm nay
    attendance_state = fields.Selection([
        ('checked_out', 'Chưa vào làm / Đã tan ca'),
        ('checked_in', 'Đang làm việc')
    ], string='Tình trạng ca làm', compute='_compute_today_attendance')
    
    today_check_in = fields.Datetime(string='Giờ vào hôm nay', compute='_compute_today_attendance')
    today_check_out = fields.Datetime(string='Giờ ra hôm nay', compute='_compute_today_attendance')
    today_work_hours = fields.Float(string='Giờ làm hôm nay', compute='_compute_today_attendance')

    _sql_constraints = [
        ('unique_employee_code', 'unique(employee_code)', 'Lỗi: Mã nhân viên phải là duy nhất!')
    ]

    # Tính toán thông tin ca làm hôm nay
    def _compute_today_attendance(self):
        today = fields.Date.context_today(self)
        for emp in self:
            rec = self.env['attendance.record'].search([
                ('employee_id', '=', emp.id),
                ('date', '=', today)
            ], order='check_in desc', limit=1)
            
            if rec:
                emp.today_check_in = rec.check_in
                emp.today_check_out = rec.check_out
                emp.today_work_hours = rec.work_hours
                emp.attendance_state = 'checked_in' if not rec.check_out else 'checked_out'
            else:
                emp.today_check_in = False
                emp.today_check_out = False
                emp.today_work_hours = 0.0
                emp.attendance_state = 'checked_out'

    # Hành động khi bấm nút [ CHẤM CÔNG VÀO ]
    def action_btn_check_in(self):
        self.ensure_one()
        # Kiểm tra xem có ca nào chưa checkout không
        open_rec = self.env['attendance.record'].search([
            ('employee_id', '=', self.id),
            ('check_out', '=', False)
        ], limit=1)
        if open_rec:
            raise ValidationError("Bạn đang trong ca làm việc rồi, chưa Check-out!")
        
        self.env['attendance.record'].create({
            'employee_id': self.id,
            'date': fields.Date.context_today(self),
            'check_in': fields.Datetime.now(),
        })

    # Hành động khi bấm nút [ CHẤM CÔNG RA ]
    def action_btn_check_out(self):
        self.ensure_one()
        open_rec = self.env['attendance.record'].search([
            ('employee_id', '=', self.id),
            ('check_out', '=', False)
        ], limit=1)
        if not open_rec:
            raise ValidationError("Bạn chưa Check-in nên không thể Check-out!")
        
        open_rec.action_check_out()

    # Mở màn hình chấm công của tài khoản đang đăng nhập
    @api.model
    def action_open_my_attendance(self):
        emp = self.search([('user_id', '=', self.env.uid)], limit=1)
        if not emp:
            raise ValidationError("Tài khoản này là Quản trị viên hệ thống (Admin), không áp dụng chấm công ca làm cá nhân!")
        
        return {
            'name': 'Chấm công hôm nay',
            'type': 'ir.actions.act_window',
            'res_model': 'attendance.employee',
            'view_mode': 'form',
            'res_id': emp.id,
            'view_id': self.env.ref('attendance_management.view_my_attendance_card').id,
            'target': 'current',
        }