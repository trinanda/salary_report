# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import fields, models


class Company(models.Model):
    _inherit = "res.company"

    employer_id = fields.Char('Employer ID')
