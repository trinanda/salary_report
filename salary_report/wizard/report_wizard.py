# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _


class SalaryReportWizard(models.TransientModel):
    _name = 'salary.report.wizard'

    report_type = fields.Selection(
        [('wage_protection_report', 'Wage Protection Report'), ('salary_report', 'Salary Report')],
        default='wage_protection_report', required=True)
    start_date = fields.Date(required=True)
    end_date = fields.Date(required=True)
    number_of_day = fields.Integer(compute='_compute_number_of_day', store=True)
    value_date = fields.Date(required=True)
    debit_date = fields.Date(required=True)
    year = fields.Selection([(str(num), str(num)) for num in range(1900, 2101)], string='Year', required=True,
                            default=str(datetime.now().year))

    month = fields.Selection([
        ('01', 'January'),
        ('02', 'February'),
        ('03', 'March'),
        ('04', 'April'),
        ('05', 'May'),
        ('06', 'June'),
        ('07', 'July'),
        ('08', 'August'),
        ('09', 'September'),
        ('10', 'October'),
        ('11', 'November'),
        ('12', 'December'),
    ], string='Month', required=True)

    @api.depends('start_date', 'end_date')
    def _compute_number_of_day(self):
        for record in self:
            if record.start_date and record.end_date:
                delta = record.end_date - record.start_date
                record.number_of_day = delta.days + 1

    @api.onchange('year', 'month')
    def onchange_year_month(self):
        if self.year and self.month:
            # Convert month and year to datetime object
            date_str = self.year + '-' + self.month + '-01'
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()

            # Set start and end date fields
            self.start_date = date_obj.strftime('%Y-%m-%d')
            self.end_date = (date_obj + relativedelta(day=31)).strftime('%Y-%m-%d')

    def generate_report_excel(self):
        data = {'date_start': self.start_date, 'date_stop': self.end_date, 'value_date': self.value_date}
        return self.env.ref('salary_report.salary_report_xlsx').report_action([], data=data)
