# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models


class SalaryReportXlsx(models.AbstractModel):
    _name = 'report.salary_report.report_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, objs):
        self.env.cr.execute("""
                            SELECT 
                              e.identification_id, 
                              e.name, 
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
                              p.number as payslip_reference, 
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
                        """, (data['date_start'], data['date_stop']))
        result = self.env.cr.dictfetchall()
        # print('result',result)
        print("data['date_start']", data['date_start'])
        company = self.env.company
        bank_name = None
        bank_code = None
        if company.bank_ids:
            bank_account = company.bank_ids[0]  # Get the first bank account associated with the company
            bank_name = bank_account.bank_name
            bank_code = bank_account.bank_bic
        total_amount = 0
        number_of_record = 0

        report_name = 'Salary Report'
        sheet = workbook.add_worksheet(report_name)
        bold = workbook.add_format({'bold': True})

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

        col = 0

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
        for dt in result:
            total_amount += dt['net_salary']
            row_line += 1
            number_of_record += 1
            sheet.write(row_line, col, dt['identification_id'])
            sheet.write(row_line, col + 1, dt['name'])
            sheet.write(row_line, col + 2, dt['employee_bank_code'])
            sheet.write(row_line, col + 3, dt['employee_account_number'])
            sheet.write(row_line, col + 4, dt['net_salary'])
            sheet.write(row_line, col + 5, dt['basic_salary'])
            sheet.write(row_line, col + 6, dt['house_rent_allowance'])
            sheet.write(row_line, col + 7, dt['other_allowance'])
            sheet.write(row_line, col + 8, dt['deductions'])
            sheet.write(row_line, col + 9, dt['payslip_reference'])
            sheet.write(row_line, col + 10, dt['employee_address'])

        sheet.write(0, 1, company.name)
        sheet.write(1, 1, company.company_registry if company.company_registry else None)
        sheet.write(2, 1, bank_name)
        sheet.write(3, 1, bank_code)
        sheet.write(4, 1, company.currency_id.name)
        sheet.write(5, 1, company.employer_id if company.employer_id else None)
        sheet.write(6, 1, data['value_date'])
        sheet.write(7, 1, total_amount)
        sheet.write(8, 1, number_of_record)
