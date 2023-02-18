# -*- coding: utf-8 -*-
# from odoo import http


# class WageReport(http.Controller):
#     @http.route('/wage_report/wage_report', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/wage_report/wage_report/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('wage_report.listing', {
#             'root': '/wage_report/wage_report',
#             'objects': http.request.env['wage_report.wage_report'].search([]),
#         })

#     @http.route('/wage_report/wage_report/objects/<model("wage_report.wage_report"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('wage_report.object', {
#             'object': obj
#         })
