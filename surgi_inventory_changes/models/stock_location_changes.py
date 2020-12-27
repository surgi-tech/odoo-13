from odoo import fields,models,api

class stock_location_inherit(models.Model):
    _inherit = 'stock.location'

    is_operation_location = fields.Boolean(string="Is Operation Location" )
    warehouse_id = fields.Many2one('stock.warehouse',string="Warehouse")
    required_approval = fields.Boolean(string="Required Approval?" )
    partner_id = fields.Many2one('res.partner',string='Owner')