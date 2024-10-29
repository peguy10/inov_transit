# -*- coding: utf-8 -*-

from odoo import models, fields, api


class TransitDebour(models.Model):
    _name = 'debour.transit'
    _rec_name = 'product_id'


    @api.depends('product_id', 'product_qty', 'tax_id', 'transit_id')
    def _compute_taxe_line(self):
        for line in self:
            taxes = line.tax_id.compute_all(line.product_id.lst_price, line.transit_id.currency_id, line.product_qty,
                                            product=line.product_id, partner=line.transit_id.customer_id)
            line.update({
                'price_taxed': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'amount_debour': taxes['total_included'],
            })
            # line.price_taxed= round(sum((line.product_qty*t.amount)/100 for t in line.product_id.taxes_id))
            # line.amount_debour= line.price_taxed + line.product_qty

    product_id = fields.Many2one(
        'product.product',
        string='Designation',
        required=True,
        domain="[('sale_ok', '=', True),('type','=','service')]")
    ref_deb = fields.Char("Reference Facture")
    amount_debour = fields.Float("Montant", compute='_compute_taxe_line', readonly=True)
    transit_id = fields.Many2one(
        'folder.transit',
        string='Dossier',
    )
    price_taxed = fields.Float(
        compute='_compute_taxe_line',
        string='TVA', store=True, )

    product_qty = fields.Float(
        string='Base',
        default=0.0)
    user_id = fields.Many2one('res.users', string='Traite Par',
                              readonly=True,
                              default=lambda self: self.env.user)
    tax_id = fields.Many2many('account.tax', string='Taxes',
                              domain=['|', ('active', '=', False), ('active', '=', True)])
    attach_files_ids = fields.Many2many('ir.attachment', string="Pieces Jointes")


