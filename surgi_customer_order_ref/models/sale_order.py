from odoo import models, fields, api

class StockPickingInherit(models.Model):
    _inherit = 'stock.picking'

    customer_order_ref = fields.Char(string="Customer Order Ref.", required=False, )
    area_manager = fields.Many2one(comodel_name='res.users', string="Area Manager")
    hospital = fields.Many2one('res.partner', string="Hospital", )
    sales_person_id = fields.Many2one(comodel_name="res.users", string="Sales Person", required=False, )
    delivery_date = fields.Date(string="Delivery Date", required=False, )



class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    customer_order_ref = fields.Char(string="Customer Order Ref.", required=False, )
    is_ref_order = fields.Boolean(string="", compute='calculate_customer_order_ref')

    @api.depends('customer_order_ref', 'state', 'picking_ids')
    def calculate_customer_order_ref(self):
        self.is_ref_order = False
        for rec in self:
            for line in rec.picking_ids:
                rec.is_ref_order = True
                line.customer_order_ref = rec.customer_order_ref
                line.customer_order_ref = rec.customer_order_ref
                line.area_manager = rec.sales_area_manager.id
                line.hospital = rec.hospital_id.id
                line.sales_person_id = rec.user_id.id
                line.delivery_date = rec.commitment_date

    def action_view_delivery(self):
        '''
        This function returns an action that display existing delivery orders
        of given sales order ids. It can either be a in a list or in a form
        view, if there is only one delivery order to show.
        '''
        action = self.env.ref('stock.action_picking_tree_all').read()[0]

        pickings = self.mapped('picking_ids')
        if len(pickings) > 1:
            action['domain'] = [('id', 'in', pickings.ids)]
        elif pickings:
            form_view = [(self.env.ref('stock.view_picking_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state, view) for state, view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = pickings.id
        # Prepare the context.
        picking_id = pickings.filtered(lambda l: l.picking_type_id.code == 'outgoing')
        picking_id.customer_order_ref = self.customer_order_ref
        picking_id.area_manager = self.sales_area_manager.id
        picking_id.hospital = self.hospital_id.id
        picking_id.sales_person_id = self.user_id.id
        picking_id.delivery_date = self.commitment_date

        if picking_id:
            picking_id = picking_id[0]
        else:
            picking_id = pickings[0]
        action['context'] = dict(self._context, default_partner_id=self.partner_id.id, default_picking_id=picking_id.id,
                                 default_picking_type_id=picking_id.picking_type_id.id, default_origin=self.name,
                                 default_group_id=picking_id.group_id.id,
                                 )
        return action

