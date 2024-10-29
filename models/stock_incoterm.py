# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockIncoterms(models.Model):
    _name = 'stock.incoterms'
    _description='Inconterms'

    name=fields.Char("Nom")
    code=fields.Char("Code")