# -*- coding: utf-8 -*-
# from odoo import http


# class SurgiPurchaseAccess(http.Controller):
#     @http.route('/surgi_purchase_access/surgi_purchase_access/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/surgi_purchase_access/surgi_purchase_access/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('surgi_purchase_access.listing', {
#             'root': '/surgi_purchase_access/surgi_purchase_access',
#             'objects': http.request.env['surgi_purchase_access.surgi_purchase_access'].search([]),
#         })

#     @http.route('/surgi_purchase_access/surgi_purchase_access/objects/<model("surgi_purchase_access.surgi_purchase_access"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('surgi_purchase_access.object', {
#             'object': obj
#         })
