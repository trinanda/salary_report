# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import fields, models, api


class HrEmployeePrivate(models.Model):
    _inherit = "hr.employee"

    employee_bank_code = fields.Selection(
        [('ARNB', 'Arab National Bank (ARNB)'), ('AAAL', 'Saudi Hollandi Bank (AAAL)'),
         ('ALBI', 'Bank Albilad (ALBI)')])
    employee_account_number = fields.Char()
    employee_private_address = fields.Char(compute='_compute_employee_private_address', store=True)

    @api.depends('address_home_id')
    def _compute_employee_private_address(self):
        for rec in self:
            rec.employee_private_address = f"{rec.address_home_id.street}, {rec.address_home_id.street2}, {rec.address_home_id.city}, {rec.address_home_id.state_id.name}, {rec.address_home_id.zip}, {rec.address_home_id.country_id.name}"
