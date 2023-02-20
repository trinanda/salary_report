from odoo import models


class SalaryReportXlsx(models.AbstractModel):
    _name = 'report.salary_report.report_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, objs):
        report_name = 'Salary Report'
        sheet = workbook.add_worksheet(report_name)
        bold = workbook.add_format({'bold': True})
        sheet.set_column('A:A', 25)
        sheet.set_column('B:B', 8)
        sheet.set_column('C:C', 5)
        sheet.set_column('D:D', 12)
        sheet.set_column('E:E', 12)
        sheet.set_column('F:F', 10)
        sheet.set_column('G:G', 12)
        sheet.set_column('H:H', 12)
        sheet.set_column('I:I', 6)
        sheet.set_column('J:J', 7)

        row_information = 0
        col = 0
        row_line = 9

        sheet.write(row_information, col + 0, 'Emp. ID. No.', bold)
        sheet.write(row_information, col + 1, 'Emp. Name', bold)
        sheet.write(row_information, col + 2, 'Emp. Bank Code', bold)
        sheet.write(row_information, col + 3, 'Emp. Acc. No', bold)
        sheet.write(row_information, col + 4, 'Salary Amount', bold)
        sheet.write(row_information, col + 5, 'Basic Salary', bold)
        sheet.write(row_information, col + 6, 'Housing Allowance', bold)
        sheet.write(row_information, col + 7, 'Other Earnings', bold)
        sheet.write(row_information, col + 8, 'Deductions', bold)
        sheet.write(row_information, col + 9, 'Employee Address', bold)

        print('datadatadatadatadata', data)
        data = {'date_start': '2023-01-01 04:29:54',
                'date_stop': '2023-03-30 04:29:54'}

        for obj in objs:
            print("obj._get_report_values(self", obj._get_report_values(self, data=data))

        #     sheet.write(row_information + 1, col + 1, obj._get_report_values(self, data=data)['date_start'])
        #     sheet.write(row_information + 2, col + 1, obj._get_report_values(self, data=data)['date_stop'])
        #
        #     for line in obj._get_report_values(self, data=data)['lines']:
        #         row_line += 1
        #         sheet.write(row_line, col, line['product_name'])
        #         sheet.write(row_line, col + 1, line['quantity'])
        #         sheet.write(row_line, col + 2, line['uom'] if line['uom'] else 'Units')
        #         sheet.write(row_line, col + 3, line['cost'])
        #         sheet.write(row_line, col + 4, line['price_unit'])
        #         sheet.write(row_line, col + 5, line['discount'] if line['discount'] else 0)
        #         sheet.write(row_line, col + 6, line['total_cost'])
        #         sheet.write(row_line, col + 7, line['total_sale'])
        #         sheet.write(row_line, col + 8, line['profit'])
        #         sheet.write(row_line, col + 9, line['percentage'])
