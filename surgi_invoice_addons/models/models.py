# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class surgi_invoice_addons(models.Model):
#     _name = 'surgi_invoice_addons.surgi_invoice_addons'
#     _description = 'surgi_invoice_addons.surgi_invoice_addons'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
