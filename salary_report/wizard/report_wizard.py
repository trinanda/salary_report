# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class SalaryReportWizard(models.TransientModel):
    _name = 'salary.report.wizard'

    start_date = fields.Date(required=True)
    end_date = fields.Date(required=True)
    number_of_day = fields.Integer(compute='_compute_number_of_day', store=True)

    @api.depends('start_date', 'end_date')
    def _compute_number_of_day(self):
        for record in self:
            if record.start_date and record.end_date:
                delta = record.end_date - record.start_date
                record.number_of_day = delta.days

    def generate_report_excel(self):
        data = {'date_start': self.start_date, 'date_stop': self.end_date}
        return self.env.ref('salary_report.salary_report_xlsx').report_action([], data=data)
