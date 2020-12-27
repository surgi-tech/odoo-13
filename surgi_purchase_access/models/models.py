# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class surgi_purchase_access(models.Model):
#     _name = 'surgi_purchase_access.surgi_purchase_access'
#     _description = 'surgi_purchase_access.surgi_purchase_access'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
