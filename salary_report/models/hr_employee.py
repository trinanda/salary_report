# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class HrEmployeePrivate(models.Model):
    _inherit = "hr.employee"

    employee_bank_code = fields.Selection(
        [('ARNB', 'Arab National Bank (ARNB)'), ('AAAL', 'Saudi Hollandi Bank (AAAL)'),
         ('ALBI', 'Bank Albilad (ALBI)')])
    employee_account_number = fields.Char()
