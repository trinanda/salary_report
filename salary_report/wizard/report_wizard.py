# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
import base64


class SalaryReportWizard(models.TransientModel):
    _name = 'salary.report.wizard'

    report_type = fields.Selection(
        [('wage_protection_report', 'Wage Protection Report'), ('salary_report', 'Salary Report')],
        default='wage_protection_report', required=True)
    start_date = fields.Date(required=True)
    end_date = fields.Date(required=True)
    number_of_day = fields.Integer(compute='_compute_number_of_day', store=True)
    file_reference = fields.Char()
    value_date = fields.Date(required=True)
    debit_date = fields.Date()
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

    wage_protection_report_file = fields.Binary("My file")

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

    def generate_data(self):
        data = {}
        self.env.cr.execute("""
                                    SELECT 
                                      e.identification_id, 
                                      e.name as employee_name, 
                                      e.employee_bank_code, 
                                      e.employee_account_number, 
                                      SUM(
                                        CASE WHEN hsrc.name ->> 'en_US' = 'Net' THEN l.amount END
                                      ) as net_salary, 
                                      SUM(
                                        CASE WHEN hsrc.name ->> 'en_US' = 'Basic' THEN l.amount END
                                      ) as basic_salary, 
                                      SUM(
                                        CASE WHEN hsrc.name ->> 'en_US' = 'بدل سكن' THEN l.amount END
                                      ) as house_rent_allowance, 
                                      SUM(
                                        CASE WHEN hsrc.name ->> 'en_US' = 'بدلات أخرى' THEN l.amount END
                                      ) as other_allowance, 
                                      SUM(
                                        CASE WHEN hsrc.name ->> 'en_US' = 'Deduction' THEN l.amount END
                                      ) as deductions, 
                                      p.number as payment_description, 
                                      COALESCE(employee_address, '') as employee_address 
                                    FROM 
                                      hr_payslip p 
                                      INNER JOIN hr_employee e ON p.employee_id = e.id 
                                      INNER JOIN hr_payslip_line l ON p.id = l.slip_id 
                                      INNER JOIN hr_salary_rule hs ON hs.id = l.salary_rule_id 
                                      INNER JOIN hr_salary_rule_category hsrc ON hsrc.id = hs.category_id 
                                      LEFT JOIN (
                                        SELECT 
                                          e.id as employee_id, 
                                          string_agg(
                                            concat_ws(
                                              ', ', 
                                              NULLIF(pa.street, ''), 
                                              NULLIF(pa.street2, ''), 
                                              NULLIF(pa.city, ''), 
                                              NULLIF(state.name, ''), 
                                              NULLIF(pa.zip, ''), 
                                              NULLIF(country.name ->> 'en_US', '')
                                            ), 
                                            ', '
                                          ) as employee_address 
                                        FROM 
                                          hr_employee e 
                                          LEFT JOIN res_partner pa ON e.address_home_id = pa.id 
                                          LEFT JOIN res_country country ON pa.country_id = country.id 
                                          LEFT JOIN res_country_state state ON pa.state_id = state.id 
                                        GROUP BY 
                                          e.id
                                      ) as addresses ON e.id = addresses.employee_id 
                                    WHERE 
                                      p.date_from >= %s
                                      AND p.date_to <= %s
                                      AND p.state = 'done' 
                                    GROUP BY 
                                      p.number, 
                                      e.identification_id, 
                                      e.name, 
                                      e.employee_bank_code, 
                                      e.employee_account_number, 
                                      employee_address;
                                """, (self.start_date, self.end_date))
        result = self.env.cr.dictfetchall()
        data['query'] = result
        company = self.env.company
        data['company_name'] = company.name
        data['company_registry'] = company.company_registry if company.company_registry else None
        data['employer_id'] = company.employer_id if company.employer_id else None
        data['currency'] = company.currency_id.name
        bank_name = None
        acc_number = None
        if company.bank_ids:
            bank_account = company.bank_ids[0]  # Get the first bank account associated with the company
            bank_name = bank_account.bank_name
            acc_number = bank_account.acc_number
        data['bank_name'] = bank_name
        data['acc_number'] = acc_number
        total_amount = 0
        number_of_record = 0

        for dt in result:
            total_amount += dt['net_salary']
            number_of_record += 1
        data['total_amount'] = total_amount
        data['number_of_record'] = number_of_record
        data['value_date'] = self.value_date

        return data

    def generate_report(self):
        if self.report_type == 'salary_report':
            data = {'date_start': self.start_date, 'date_stop': self.end_date, 'data': self.generate_data()}
            return self.env.ref('salary_report.salary_report_xlsx').report_action([], data=data)
        else:
            text = f"{self.generate_data()['bank_name']}\t{self.generate_data()['company_registry']}\t" \
                   f"{self.generate_data()['acc_number']}\t\t\t{self.generate_data()['currency']}\t{self.value_date}\t" \
                   f"{self.generate_data()['total_amount']}\t{self.debit_date}\t{self.file_reference}\t\t\t" \
                   f"{self.generate_data()['employer_id']}"
            for record in self.generate_data()['query']:
                text += f"{record['net_salary']}\t{record['employee_account_number']}\t\t\t\t{record['employee_name']}" \
                        f"\t\t\t\t{record['employee_bank_code']}\t{record['payment_description']}\t{record['net_salary']}" \
                        f"\t{record['basic_salary']}\t{record['house_rent_allowance']}\t{record['other_allowance']}" \
                        f"\t{record['identification_id']}" \
                        f"\n"
            text += '-'
            self.wage_protection_report_file = base64.b64encode(text.encode())
            return {
                'type': 'ir.actions.act_url',
                'url': '/web/content/salary.report.wizard/%s/wage_protection_report_file/%s?download=true' % (
                    self.id, "Wage Protection Report.txt"),
            }
