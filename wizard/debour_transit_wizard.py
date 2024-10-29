# -*- coding: utf-8 -*-
####################################################
#   Author : MOUSSI PEE <moussipeee@gmail.com>
####################################################

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class TransitWizard(models.TransientModel):
    _name = 'stage.transit.wizard'

    stage_id = fields.Many2one(
        'stages.transit',
        string='Etapes',
        required=True
    )

    transit_id = fields.Many2one(
        'folder.transit',
        string='Client',
        # default=_default_transit_id
    )

    stage = fields.Selection([('transit', 'Dedouanement'), ('accone', 'Acconage'), ('ship', 'Shipping')],
                             string="Processus")
    number = fields.Integer(
        string='Numero Etape',
        readonly=True,
    )

    def stage_ok(self):
        record = self.transit_id
        record.update({
            'stage_id': self.stage_id.id
        })
        record.check_stage_follow()

        return {'type': 'ir.actions.act_window_close'}