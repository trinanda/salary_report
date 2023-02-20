# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging

from datetime import timedelta

import pytz

from odoo import api, fields, models, _
from odoo.osv.expression import AND


class SalaryReport(models.AbstractModel):
    _name = 'report.payroll.salary_report'

    @api.model
    def get_salary_details(self, date_start=False, date_stop=False):

        print('date_start', date_start)
        print('date_stop', date_stop)

        domain = [('state', '=', 'done')]

        if date_start:
            date_start = fields.Datetime.from_string(date_start)
        else:
            # start by default today 00:00:00
            user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz or 'UTC')
            today = user_tz.localize(fields.Datetime.from_string(fields.Date.context_today(self)))
            date_start = today.astimezone(pytz.timezone('UTC'))

        if date_stop:
            date_stop = fields.Datetime.from_string(date_stop)
            # avoid a date_stop smaller than date_start
            if (date_stop < date_start):
                date_stop = date_start + timedelta(days=1, seconds=-1)
        else:
            # stop by default today 23:59:59
            date_stop = date_start + timedelta(days=1, seconds=-1)

        domain = AND([domain,
                      [('date_from  ', '>=', fields.Datetime.to_string(date_start)),
                       ('date_to', '<=', fields.Datetime.to_string(date_stop))]
                      ])



        self.env.cr.execute("""
            SELECT e.identification_id, e.name, e.employee_bank_code, e.employee_account_number,
            SUM(CASE WHEN l.code = 'NET' THEN l.amount END) as net_salary,
            SUM(CASE WHEN l.code = 'BASIC' THEN l.amount END) as basic_salary,
            SUM(CASE WHEN l.code = 'HRA' THEN l.amount END) as house_rent_allowance,
            SUM(CASE WHEN l.code = 'Other' THEN l.amount END) as other_allowance,
            SUM(CASE WHEN l.code = 'PT' THEN l.amount END) as deductions,
            p.name as payslip_reference, e.employee_private_address
            FROM hr_payslip p
            INNER JOIN hr_employee e ON p.employee_id = e.id
            INNER JOIN hr_payslip_line l ON p.id = l.slip_id
            WHERE p.date_from >= %s AND p.date_to <= %s
            GROUP BY p.name, e.identification_id, e.name, e.employee_bank_code, e.employee_account_number, e.employee_private_address
        """, (str(date_start), str(date_stop)))
        result = self.env.cr.dictfetchall()
        print('==========================', result)

        return {
            'date_start': date_start,
            'date_stop': date_stop,
            # 'company_name': self.env.company.name,
            # 'lines': sorted([{
            #     'identification_id': product.id,
            #     'product_name': product.name,
            #     'code': product.default_code,
            #     'quantity': qty,
            #     'price_unit': price_unit,
            #     'discount': discount,
            #     'uom': product.uom_id.name
            # } for (product, price_unit, discount), qty in products_sold.items()], key=lambda l: l['product_name'])
        }

    @api.model
    def _get_report_values(self, data=None):
        data = dict(data or {})
        # initialize data keys with their value if provided, else None
        data.update({
            'date_start': data.get('date_start'),
            'date_stop': data.get('date_stop')
        })
        print('data from _get_report_values',data)
        data.update(self.get_salary_details(data['date_start'], data['date_stop']))
        return data
