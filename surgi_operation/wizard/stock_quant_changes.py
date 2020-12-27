from odoo import fields, models, api, exceptions


class stock_quant_inherit_wizard(models.Model):
    _inherit = 'stock.quant'

    is_operation_related = fields.Boolean(related="location_id.is_operation_location",
                                          string="Is Operation Location",store=True)

    def open_wizard_stock(self):
        action = self.env.ref('stock_quant.action_wizard_stock_quant')
        result = action.read()[0]
        res = self.env.ref('stock_quant.wizard_line_stock_quant', False)
        result['views'] = [(res and res.id or False, 'form')]
        result['target'] = 'current'
        return result

    def open_wizard_back_to_warehouse(self):
        action = self.env.ref('stock_quant.action_wizard_back_to_warehouse_quant')
        result = action.read()[0]
        res = self.env.ref('stock_quant.wizard_back_to_warehouse', False)
        result['views'] = [(res and res.id or False, 'form')]
        result['target'] = 'new'
        return result

    def open_wizard_move_to_location(self):
        action = self.env.ref('stock_quant.action_wizard_wizard_move_to_location')
        result = action.read()[0]
        res = self.env.ref('stock_quant.wizard_wizard_move_to_location', False)
        result['views'] = [(res and res.id or False, 'form')]
        result['target'] = 'new'
        return result

    def open_wizard_move_to_hanged_warehouse(self):
        action = self.env.ref('stock_quant.action_wizard_wizard_move_to_hanged_warehouse')
        result = action.read()[0]
        res = self.env.ref('stock_quant.wizard_wizard_move_to_hanged_warehouse', False)
        result['views'] = [(res and res.id or False, 'form')]
        result['target'] = 'new'
        return result
