# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models


class SalaryReportXlsx(models.AbstractModel):
    _name = 'report.salary_report.report_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, objs):
        report_name = 'Salary Report'
        sheet = workbook.add_worksheet(report_name)
        bold = workbook.add_format({'bold': True})
        col = 0

        """sheet.set_column('column', space number)"""
        sheet.set_column('A:A', 22)
        sheet.set_column('B:B', 35)
        sheet.set_column('C:C', 15)
        sheet.set_column('D:D', 15)
        sheet.set_column('E:E', 15)
        sheet.set_column('F:F', 15)
        sheet.set_column('G:G', 18)
        sheet.set_column('H:H', 15)
        sheet.set_column('I:I', 15)
        sheet.set_column('J:J', 15)
        sheet.set_column('K:K', 50)

        """sheet.write(row index, column index, 'Field Name', format)"""
        sheet.write(0, col, 'Company Name', bold)
        sheet.write(1, col, 'Company Registry', bold)
        sheet.write(2, col, 'Company BANK Name', bold)
        sheet.write(3, col, 'Company BANK Code', bold)
        sheet.write(4, col, 'Currency Code', bold)
        sheet.write(5, col, 'Company MOL Number', bold)
        sheet.write(6, col, 'Value Date', bold)
        sheet.write(7, col, 'Total Amount', bold)
        sheet.write(8, col, 'Number of Record', bold)

        sheet.write(10, col, 'Emp. ID. No.', bold)
        sheet.write(10, col + 1, 'Emp. Name', bold)
        sheet.write(10, col + 2, 'Emp. Bank Code', bold)
        sheet.write(10, col + 3, 'Emp. Acc. No', bold)
        sheet.write(10, col + 4, 'Salary Amount', bold)
        sheet.write(10, col + 5, 'Basic Salary', bold)
        sheet.write(10, col + 6, 'Housing Allowance', bold)
        sheet.write(10, col + 7, 'Other Earnings', bold)
        sheet.write(10, col + 8, 'Deductions', bold)
        sheet.write(10, col + 9, 'Payment Description', bold)
        sheet.write(10, col + 10, 'Employee Address', bold)

        row_line = 10
        for dt in data['data']['query']:
            row_line += 1
            sheet.write(row_line, col, dt['identification_id'])
            sheet.write(row_line, col + 1, dt['employee_name'])
            sheet.write(row_line, col + 2, dt['employee_bank_code'])
            sheet.write(row_line, col + 3, dt['employee_account_number'])
            sheet.write(row_line, col + 4, dt['net_salary'])
            sheet.write(row_line, col + 5, dt['basic_salary'])
            sheet.write(row_line, col + 6, dt['house_rent_allowance'])
            sheet.write(row_line, col + 7, dt['other_allowance'])
            sheet.write(row_line, col + 8, dt['deductions'])
            sheet.write(row_line, col + 9, dt['payment_description'])
            sheet.write(row_line, col + 10, dt['employee_address'])

        sheet.write(0, 1, data['data']['company_name'])
        sheet.write(1, 1, data['data']['company_registry'])
        sheet.write(2, 1, data['data']['bank_name'])
        sheet.write(3, 1, data['data']['acc_number'])
        sheet.write(4, 1, data['data']['currency'])
        sheet.write(5, 1, data['data']['employer_id'])
        sheet.write(6, 1, data['data']['value_date'])
        sheet.write(7, 1, data['data']['total_amount'])
        sheet.write(8, 1, data['data']['number_of_record'])
