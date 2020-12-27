# -*- coding: utf-8 -*-
# from odoo import http


# class SurgiInvoiceAddons(http.Controller):
#     @http.route('/surgi_invoice_addons/surgi_invoice_addons/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/surgi_invoice_addons/surgi_invoice_addons/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('surgi_invoice_addons.listing', {
#             'root': '/surgi_invoice_addons/surgi_invoice_addons',
#             'objects': http.request.env['surgi_invoice_addons.surgi_invoice_addons'].search([]),
#         })

#     @http.route('/surgi_invoice_addons/surgi_invoice_addons/objects/<model("surgi_invoice_addons.surgi_invoice_addons"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('surgi_invoice_addons.object', {
#             'object': obj
#         })
