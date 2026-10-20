# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase, tagged
from odoo.exceptions import ValidationError
from datetime import datetime

@tagged('at_install', 'post_install')
class TestAttendanceManagement(TransactionCase):

    def setUp(self):
        super(TestAttendanceManagement, self).setUp()
        self.Employee = self.env['attendance.employee']
        self.Attendance = self.env['attendance.record']

        self.employee_test = self.Employee.create({
            'employee_code': 'TEST01',
            'name': 'Nhân Viên Kiểm Thử',
            'department': 'it',
            'status': 'working',
        })

    def test_01_create_employee(self):
        """Test Case 1: Kiểm tra tạo hồ sơ nhân viên thành công"""
        self.assertEqual(self.employee_test.employee_code, 'TEST01')
        self.assertEqual(self.employee_test.status, 'working')

    def test_02_work_hours_computation(self):
        """Test Case 2: Kiểm tra thuật toán tự động tính tổng giờ làm"""
        time_in = datetime(2026, 10, 20, 8, 0, 0)
        time_out = datetime(2026, 10, 20, 17, 0, 0)

        record = self.Attendance.create({
            'employee_id': self.employee_test.id,
            'check_in': time_in,
            'check_out': time_out,
        })
        self.assertEqual(record.work_hours, 9.0, "Tổng giờ làm phải bằng chính xác 9.0!")

    def test_03_prevent_resigned_with_open_checkin(self):
        """Test Case 3: Kiểm tra ràng buộc chặn nhân viên nghỉ việc khi chưa check-out"""
        self.Attendance.create({
            'employee_id': self.employee_test.id,
            'check_in': datetime.now(),
            'check_out': False,
        })
        with self.assertRaises(ValidationError):
            self.employee_test.write({'status': 'resigned'})
