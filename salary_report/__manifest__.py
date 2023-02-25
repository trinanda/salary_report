# -*- coding: utf-8 -*-
{
    'name': "salary_report",

    'summary': """
        Generate Wage Protection Report and Salary Report""",

    'description': """
        Generate Wage Protection Report and Salary Report for Saudi Arabia Government
    """,

    'author': "Tri Nanda",
    'website': "https://www.github.com/trinanda",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Generic Modules/Human Resources',
    'version': '16.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['hr_payroll_community', 'report_xlsx'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/salary_report.xml',
        'views/res_company_views.xml',
        'views/hr_employee_views.xml',
        'wizard/report_wizard.xml',
    ],
}
