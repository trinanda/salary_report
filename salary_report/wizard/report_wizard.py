# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class SalaryReportWizard(models.TransientModel):
    _name = 'salary.report.wizard'

    start_date = fields.Datetime(required=True)
    end_date = fields.Datetime(required=True, default=fields.Datetime.now)
    number_of_day = fields.Integer()
    month = fields.Char()

    def generate_report_excel(self):
        data = {'date_start': self.start_date, 'date_stop': self.end_date}
        return self.env.ref('salary_report.salary_report_xlsx').report_action([], data=data)
