# -*- coding: utf-8 -*-
# from odoo import http


# class AttendanceManagement(http.Controller):
#     @http.route('/attendance_management/attendance_management', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/attendance_management/attendance_management/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('attendance_management.listing', {
#             'root': '/attendance_management/attendance_management',
#             'objects': http.request.env['attendance_management.attendance_management'].search([]),
#         })

#     @http.route('/attendance_management/attendance_management/objects/<model("attendance_management.attendance_management"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('attendance_management.object', {
#             'object': obj
#         })

