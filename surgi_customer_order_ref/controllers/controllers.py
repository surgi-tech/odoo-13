# -*- coding: utf-8 -*-
# from odoo import http


# class SurgiCustomerOrderRef(http.Controller):
#     @http.route('/surgi_customer_order_ref/surgi_customer_order_ref/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/surgi_customer_order_ref/surgi_customer_order_ref/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('surgi_customer_order_ref.listing', {
#             'root': '/surgi_customer_order_ref/surgi_customer_order_ref',
#             'objects': http.request.env['surgi_customer_order_ref.surgi_customer_order_ref'].search([]),
#         })

#     @http.route('/surgi_customer_order_ref/surgi_customer_order_ref/objects/<model("surgi_customer_order_ref.surgi_customer_order_ref"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('surgi_customer_order_ref.object', {
#             'object': obj
#         })
