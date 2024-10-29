# -*- coding: utf-8 -*-
# from odoo import http


# class TransitInvoice(http.Controller):
#     @http.route('/transit_invoice/transit_invoice', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/transit_invoice/transit_invoice/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('transit_invoice.listing', {
#             'root': '/transit_invoice/transit_invoice',
#             'objects': http.request.env['transit_invoice.transit_invoice'].search([]),
#         })

#     @http.route('/transit_invoice/transit_invoice/objects/<model("transit_invoice.transit_invoice"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('transit_invoice.object', {
#             'object': obj
#         })

