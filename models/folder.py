from odoo import models, fields, api, SUPERUSER_ID, _
from odoo.exceptions import UserError
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT

from datetime import datetime, timedelta, date

AVAILABLE_PRIORITIES = [
    ('0', 'Low'),
    ('1', 'Medium'),
    ('2', 'High'),
    ('3', 'Very High'),
]


class TransitFolder(models.Model):
    _name = "folder.transit"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Dossier de Transit"
    _order = "date_open desc"


    @api.depends('task_checklist', 'len_task')
    def _get_checklist_progress(self):
        """:return the value for the check list progress"""
        for rec in self:
            total_len = rec.len_task
            check_list_len = len(rec.task_checklist)
            if total_len != 0:
                rec.checklist_progress = (check_list_len * 100) / total_len

    @api.model
    def _default_currency(self):
        return self.env.user.company_id.currency_id

    @api.model
    def _default_number(self):
        stage_id = self._get_default_stage_id()
        values = self._onchange_stage_id_values(stage_id.id)
        if 'number' in values.keys():
            return values['number']
        return 0

    def _get_default_stage_id(self):
        """ Gives default stage_id """
        stage = self.env.context.get('default_stages')
        return self._stage_find(domain=[('number', '=', 10), ('stages', '=', stage)])[0]

    # @api.depends('debour_ids')
    # def _compute_service_count(self):
    #     if self.debour_ids:
    #         self.service_count = len(self.debour_ids)


    @api.depends('order_ids')
    def get_total_order_ids_amount(self):
        self.amount_purchased = sum(a.chiffr_xaf_take for a in self.order_ids)

    def compute_alerte_date(self):
        for record in self:
            if not record.date_arrival:
                record.alerte = 'open'
            elif record.number < 104 and record.date_arrival:
                date_today = datetime.today()
                eta_date = datetime.strptime(record.date_arrival.strftime("%Y-%m-%d"), "%Y-%m-%d")
                next_date = date_today + timedelta(days=3)

                if eta_date < next_date:
                    record.alerte = 'overdue'
                elif eta_date == next_date:
                    record.alerte = 'danger'
                else:
                    record.alerte = 'open'
            else:
                record.alerte = 'open'

    def compute_deadline_date(self, date, duree):
        if not date:
            return False
        date_today = datetime.strptime(date.strftime("%Y-%m-%d"), "%Y-%m-%d")
        next_date = date_today + timedelta(days=duree)
        return next_date.strftime("%Y-%m-%d")

    name = fields.Char(string='Dossier N°', copy=False, index=True, readonly=True, default=lambda self: _('New'))
    num_ot = fields.Char(string='N° OT')
    number = fields.Integer('code', default=_default_number)
    number_stage = fields.Integer('code residual', default=50)
    date_open = fields.Date("Date de Reception OT")
    date_close = fields.Date("Date de Fermeture")
    date_deadline = fields.Date("Date de Fermeture Estimee")
    # date_departure= fields.Date("ETD")
    transpo_type = fields.Selection([('input', 'Chargement'), ('output', 'Dechargement')],
                                    string="Operation sur le navire", default='')
    date_arrival = fields.Date("ETA", tracking=True)
    date_declaration = fields.Date("Date de declaration", tracking=True)
    date_guce = fields.Date("Date de GUCE", tracking=True)
    date_validate = fields.Date("Ordre de Validation", tracking=True)
    date_RVC = fields.Date("Date AVI", tracking=True)
    date_provisiore = fields.Date("Date Provisoire", tracking=True)
    date_liquidation = fields.Date("Date Liquidation", tracking=True)
    date_depot_pad = fields.Date("Date Depot PAD", tracking=True)
    date_quittance = fields.Date("Date Quittance", tracking=True)
    date_bad = fields.Date("BAD", tracking=True)
    date_bl = fields.Date(" date BL", tracking=True)
    date_sortie = fields.Date("SORTIE", tracking=True)
    alerte = fields.Selection(
        [('open', 'Ouverture'), ('danger', 'Danger'), ('overdue', 'Depasse')],
        "Alerte", compute="compute_alerte_date", default="open")
    customer_id = fields.Many2one(
        'res.partner',
        domain="[('customer_rank', '>', 0)]",
        string='Client',
        tracking=True
    )

    vendor_id = fields.Many2one(
        'res.partner',
        domain="[('supplier_rank', '>', 0)]",
    string='Fournisseur',
    )
    exportator_id = fields.Many2one(
        'exportator.transit',
        string='Exportateur',
    )
    importator_id = fields.Many2one(
        'import.transit',
        string='Importateur',
    )

    consigne_id = fields.Many2one(
        'consignee.transit',
        string='Consignataire',
    )
    len_task = fields.Integer(
        string='empty task',
    )

    destination_id = fields.Many2one(
        'res.country',
        string='Pays de Destination',
    )
    origin_id = fields.Many2one(
        'res.country',
        string="Pays d'origine",
    )

    port_departure = fields.Many2one(
        'port.transit',
        string="Port d'embarquement",
    )
    incoterm = fields.Many2one(
        'stock.incoterms',
        string="Incoterm",
    )
    port_arrival = fields.Many2one(
        'port.transit',
        string="Port de Debarquement",
    )
    num_voy = fields.Char(
        string='N° Voyage',
    )

    num_di = fields.Char(
        string='N° DI',
    )
    code_camsi = fields.Char(
        string='Code CAMSI',
    )
    goods = fields.Char(
        string='MARCHANDISE',
    )
    num_avi = fields.Char(
        string='N° Guce',
    )
    num_besc = fields.Char(
        string='BESC'
    )
    num_pr = fields.Char(
        string='PR'
    )
    num_rvc = fields.Char(
        string='RVC'
    )
    num_rvc_1 = fields.Char(
        string='2eme RVC'
    )
    num_rvc_2 = fields.Char(
        string='3eme RVC'
    )
    num_rvc_3 = fields.Char(
        string='4eme RVC'
    )
    num_rvc_4 = fields.Char(
        string='5eme RVC'
    )
    num_rvc_5 = fields.Char(
        string='6eme RVC'
    )

    num_quittance = fields.Char(
        string='N° Quittance',
    )
    num_manifeste = fields.Char(
        string='MANIFESTE',
    )
    num_pad = fields.Char(
        string='PAD',
    )
    num_depot_pad = fields.Char(
        string='DEPOT PAD',
    )
    num_liquidation = fields.Char(
        string='N° Declaration',
    )
    vessel = fields.Many2one(
        'vessel.transit',
        string='Navire',
    )
    circuit = fields.Boolean(
        string='Circuit',
    )
    scan = fields.Boolean(
        string='Scanneur',
    )
    visit = fields.Selection([('yes', 'OUI'), ('no', 'NON')], string="Visite")
    type_op = fields.Selection([('in', 'Import'), ('out', 'Export')], string="Type d'operation", default='in')
    transp_op = fields.Selection([('air', 'Air'), ('land', 'Land'), ('sea', 'Ocean')], string="Transport",
                                 default='air')
    type_circuit = fields.Selection([('blue', 'BLEU'), ('yellow', 'JAUNE'), ('green', 'VERT'), ('red', 'ROUGE')],
                                    string="Type Circuit", default='blue')
    type_validated = fields.Selection([('open', ''), ('close', 'Valide')], string="Valide", default='open')
    amount_purchased = fields.Float("Valeur imposable en CFA", tracking=True)
    amount_douane = fields.Float("Droit de douane")
    num_brd = fields.Char("Numero de B/L", track_visibility='onchange')
    debour_ids = fields.One2many('debour.transit', 'transit_id', string="services")

    order_ids = fields.One2many('invoice.transit', 'folder_id', string="Marchandises")
    # order_ids=fields.Many2many('invoice.transit',string="Marchandises")
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  required=True, readonly=True,
                                  default=_default_currency)
    company_id = fields.Many2one('res.company', string='Company', change_default=True,
                                 required=True, readonly=True, default=lambda self: self.env.user.company_id)
    user_id = fields.Many2one('res.users', string='Traite Par', track_visibility='onchange',
                              readonly=True,
                              default=lambda self: self.env.user)
    stages = fields.Selection([('transit', 'Dedouanement'), ('accone', 'Acconage'), ('ship', 'Shipping')],
                              string="Processus", default='transit')

    task_checklist = fields.One2many('task.checklist', 'folder_id', string='Check List')
    checklist_progress = fields.Float(compute='_get_checklist_progress', string='Progress', store=True,
                                      default=0.0)
    max_rate = fields.Integer(string='Maximum rate', default=100)
    stage_id = fields.Many2one('stages.transit', string='Stage', ondelete='restrict', track_visibility='onchange',
                               index=True,
                               default=_get_default_stage_id, group_expand='_read_group_stage_ids', copy=False)
    active = fields.Boolean(
        string="Archived",
        default=True,
        help="If a Transit is set to archived, it is not displayed, but still exists.")
    color = fields.Integer('Color Index')
    # time_quittance = fields.Integer('Duree Moyenne Obtention Quittance', compute="_compute_time_quittance_obtention")
    priority = fields.Selection(AVAILABLE_PRIORITIES, string='Priority', index=True, default=AVAILABLE_PRIORITIES[0][0])
    kanban_state = fields.Selection(
        [('grey', 'No next activity planned'), ('red', 'Next activity late'), ('green', 'Next activity is planned')],
        string='Kanban State', compute='_compute_kanban_state')
    service_count = fields.Integer(string='Service Count', compute='_compute_service_count', readonly=True)
    attachment_files = fields.Many2many(
        'ir.attachment', 'folder_ir_attachments_rel',
        'folder_id', 'attachment_id', 'Attachments')

    total_weighty = fields.Float("Poids Total")
    total_fcl20 = fields.Integer("20'")
    total_fcl40 = fields.Integer("40'")
    total_colis = fields.Integer("Colis")
    uom_total_id = fields.Many2one(
        'uom.uom',
        string='Unite de Mesure',
    )
    regime = fields.Char(string="Regime")
    package_ids = fields.One2many('package.folders', 'transit_id', string="Conteneurs")

    @api.model
    def create(self, values):
        res = []
        if values['stages'] == 'transit':
            if values.get('name', _('New')) == _('New'):
                values['name'] = self.env['ir.sequence'].next_by_code('transit.invoice') or _('New')
            # channel = self.env.ref('transit_invoice.channel_transit_lmc')
            ot_id = self.env.ref('transit_invoice.mail_act_rh_courrier_order').id
            new_id = self.env.ref('transit_invoice.mail_act_rh_courrier_folder').id
            res = [ot_id, new_id]
        if values['stages'] == 'accone':
            if values.get('name', _('New')) == _('New'):
                values['name'] = self.env['ir.sequence'].next_by_code('transit.acconage') or _('New')
            # channel = self.env.ref('transit_invoice.channel_acconage')
        if values['stages'] == 'ship':
            if values.get('name', _('New')) == _('New'):
                values['name'] = self.env['ir.sequence'].next_by_code('transit.shipping') or _('New')
            # channel = self.env.ref('transit_invoice.channel_shipping')
        result = super(TransitFolder, self).create(values)
        # result.message_subscribe(channel_ids=channel.ids)
        for task in res:
            create_vals = {
                'activity_type_id': task,
                'summary': self.env['mail.activity.type'].browse([task]).name,
                'automated': True,
                'note': '',
                'date_deadline': result.compute_deadline_date(result.date_open, 0),
                'res_model_id': self.env['ir.model']._get(result._name).id,
                'res_id': result.id,
                'stages': result.stages
            }
            activity = self.env['mail.activity'].create(create_vals)
            activity.action_feedback()
        result.write({
            'len_task': len(res),
        })
        return result


    def activity_scheduler(self):
        res = []
        ot_id = self.env.ref('transit_invoice.mail_act_rh_courrier_order').id
        new_id = self.env.ref('transit_invoice.mail_act_rh_courrier_folder').id
        res = [ot_id, new_id]
        for rec in self:

            if rec.name == _('New'):
                raise UserError("Veuillez saisir Le Numero du dossier avant de planifier!!!!")
            if not rec.date_arrival:
                raise UserError("Ce Dossier n'a pas d'ETA inserée, Veuillez La Saisir avant de planifier!!!!")
            if rec.len_task == 2:
                activity_types = self.env['mail.activity.type'].search([('stages', '=', rec.stages)])
                duree = 3
                for activity in activity_types.filtered(lambda x: x.id not in res):
                    create_vals = {
                        'activity_type_id': activity.id,
                        'summary': activity.name,
                        'automated': True,
                        'note': '',
                        'user_id': activity.responsible_id.id if activity.responsible_id else self.env.user.id,
                        'date_deadline': rec.compute_deadline_date(rec.date_arrival, duree),
                        'res_model_id': self.env['ir.model']._get(rec._name).id,
                        'res_id': rec.id,
                        'stages': rec.stages
                    }
                    duree += 1
                    self.env['mail.activity'].create(create_vals)
                rec.write({
                    'date_deadline': rec.compute_deadline_date(rec.date_arrival, len(activity_types)),
                    'len_task': self.len_task + len(activity_types)
                })
            elif not rec.len_task:
                activity_types = self.env['mail.activity.type'].search([('stages', '=', rec.stages)])
                duree = 3
                for activity in activity_types:
                    create_vals = {
                        'activity_type_id': activity.id,
                        'summary': activity.name,
                        'automated': True,
                        'note': '',
                        'user_id': activity.responsible_id.id if activity.responsible_id else self.env.user.id,
                        'date_deadline': rec.compute_deadline_date(rec.date_arrival, duree),
                        'res_model_id': self.env['ir.model']._get(rec._name).id,
                        'res_id': rec.id,
                        'stages': rec.stages
                    }
                    duree += 1
                    self.env['mail.activity'].create(create_vals)
                rec.write({
                    'date_deadline': rec.compute_deadline_date(rec.date_arrival, len(activity_types)),
                    'len_task': self.len_task + len(activity_types)
                })
            else:
                raise UserError('Ce Dossier a déjà été Planifié....')


    # @api.onchange('date_arrival')
    # def on_change_date_arrival(self):
    #     self.ensure_one()
    #     for follow in self.message_follower_ids:
    #         channel = follow.channel_id
    #         channel.message_post_with_view('transit_invoice.message_channel_folder_link',
    #                                        values={'self': self, 'origin': self},
    #                                        subtype_id=self.env.ref('mail.mt_comment').id)

    # @api.depends('')

    def _stage_find(self, domain=[]):
        return self.env['stages.transit'].search(domain)

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        search_domain = []
        stage_ids = stages._search(search_domain, order=order, access_rights_uid=SUPERUSER_ID)
        return stages.browse(stage_ids)

    def action_view_services(self):
        action = self.env.ref('transit_invoice.act_res_partner_2_transit_invoice').read()[0]
        action['domain'] = [('transit_id', '=', self.id)]
        action['context'] = {
            'default_courier_id': self.id,
            'search_default_courier_id': [self.id]}
        return action

    @api.model
    def _onchange_stage_id_values(self, stage_id):
        """ returns the new values when stage_id has changed """

        if not stage_id:
            return {}
        stage = self.env['stages.transit'].browse(stage_id)
        if stage and stage.number == 0:
            stage.number = self.number_stage + 1
            self.update({
                'number_stage': stage.number
            })
            return {'number': stage.number}
        else:
            return {'number': stage.number}

    @api.onchange('stage_id')
    def _onchange_stage_id(self):
        self.check_stage_follow()


    def check_stage_follow(self):
        self.ensure_one()
        for record in self:
            if len(record.activity_ids) and record.stage_id.number in [105, 106]:
                raise UserError(_('Veuillez Terminer toutes les taches'))
            if record.checklist_progress == 0 and record.stage_id.number in [105, 106]:
                raise UserError(_('Veuiller Planifier avant de passer a cette Etape.'))
            values = record._onchange_stage_id_values(record.stage_id.id)
            record.update(values)


    def _compute_kanban_state(self):
        today = date.today()
        for lead in self:
            kanban_state = 'grey'
            if lead.activity_date_deadline:
                lead_date = fields.Date.from_string(lead.activity_date_deadline)
                if lead_date >= today:
                    kanban_state = 'green'
                else:
                    kanban_state = 'red'
            lead.kanban_state = kanban_state


    def action_validate_folder(self):
        self.ensure_one()
        for record in self:
            if record.number == 104 and not record.date_arrival:
                raise UserError(_('Vous ne pouvez pas Valider ce Dossier sans inserer l"ETA. '))
            if record.number == 104 and not record.num_besc:
                message_id = self.env['message.wizard.gec'].create(
                    {'message': _("Voulez-vous valider le Dossier %s sans BESC ? ") % (record.name)})
                return {
                    'name': _('Warning'),
                    'type': 'ir.actions.act_window',
                    'view_mode': 'form',
                    'res_model': 'message.wizard.gec',
                    'res_id': message_id.id,
                    'context': {
                        'default_folder_id': record.id,
                    },
                    'target': 'new',
                }
            if record.number == 104 and not record.num_rvc:
                message_id = self.env['message.wizard.gec'].create(
                    {'message': _("Voulez-vous valider le Dossier %s sans BESC ? ") % (record.name)})
                return {
                    'name': _('Warning'),
                    'type': 'ir.actions.act_window',
                    'view_mode': 'form',
                    'res_model': 'message.wizard.gec',
                    'res_id': message_id.id,
                    'context': {
                        'default_folder_id': record.id,
                    },
                    'target': 'new',
                }
            return {
                'name': _('Etape Suivante'),
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'stage.transit.wizard',
                'view_id': self.env.ref('transit_invoice.wizard_debour_transit_form').id,
                'context': {
                    'default_transit_id': record.id,
                    'default_number': record.number,
                    'default_stage': record.stages,
                },
                'target': 'new',
            }

    # @api.multi
    # def action_archive_button(self):
    #     self.ensure_one()
    #     # if not self.activity_ids:
    #     #    raise UserError('Veuillez termine toutes vos taches!!!!!!!')
    #     document_obj = self.env['muk_dms.directory']
    #     for record in self:
    #         piece_no_archive = self.mapped('attachment_files')
    #         parent_obj = document_obj.search([('name', '=', record.customer_id.name)])
    #         if not parent_obj:
    #             if record.stages == 'transit':
    #                 dms_vals = {
    #                     'name': record.customer_id.name,
    #                     'parent_directory': self.env.ref('transit_invoice.lmc_directory_01').id,
    #                     'transit_id': record.id,
    #                 }
    #                 parent_obj = document_obj.create(dms_vals)
    #             if record.stages == 'ship':
    #                 dms_vals = {
    #                     'name': record.name,
    #                     'parent_directory': self.env.ref('transit_invoice.lmc_directory_03').id,
    #                     'transit_id': record.id,
    #                 }
    #                 parent_obj = document_obj.create(dms_vals)
    #             if record.stages == 'accone':
    #                 dms_vals = {
    #                     'name': record.name,
    #                     'parent_directory': self.env.ref('transit_invoice.lmc_directory_02').id,
    #                     'transit_id': record.id,
    #                 }
    #                 parent_obj = document_obj.create(dms_vals)
    #         if record.customer_id:
    #             parent_obj_directory = document_obj.search(
    #                 [('name', '=', record.name), ('parent_directory', '=', parent_obj.id)])
    #             if not parent_obj_directory:
    #                 dms_vals = {
    #                     'name': record.name,
    #                     'parent_directory': parent_obj.id,
    #                     'transit_id': record.id,
    #                 }
    #                 parent_obj_directory = document_obj.create(dms_vals)
    #         if piece_no_archive:
    #             for attachment in piece_no_archive:
    #                 dms_file_vals = {
    #                     'name': attachment.name,
    #                     'content': attachment.datas,
    #                     'directory': parent_obj.id
    #                 }
    #                 self.env['muk_dms.file'].create(dms_file_vals)
    #         search_domain = [('number', '=', record.number), ('stages', '=', record.stages)]
    #         nws_stage = record._stage_find(search_domain)[0]
    #         values = record._onchange_stage_id_values(nws_stage.id)
    #         record.write({'stage_id': nws_stage.id, 'active': False})
    #         record.update(values)


    def action_create_invoice(self):
        self.ensure_one()
        invoice_obj = self.env['account.move']
        invoice_id = invoice_obj.create({
            'partner_id': self.customer_id.id,
            'transit_id': self.id,
            'service_ids': [(6, 0, self.debour_ids.ids)],
            'origin': self.name,
        })
        action = self.env.ref('account.action_invoice_tree1').read()[0]
        action['views'] = [(self.env.ref('account.move_form').id, 'form')]
        action['res_id'] = invoice_id.id
        invoice_id.message_post_with_view('mail.message_origin_link',
                                          values={'self': invoice_id, 'origin': self},
                                          subtype_id=self.env.ref('mail.mt_note').id)
        return action


    def invoice_line_debour(self, invoice):
        self.ensure_one()
        product = self.env.ref('transit_invoice.product_product_debours')
        account = product.property_account_income_id or product.categ_id.property_account_income_categ_id
        if not account:
            raise UserError(
                _('Please define income account for this product: "%s" (id:%d) - or for its category: "%s".') %
                (product.name, product.id, product.categ_id.name))

        fpos = self.regime or self.customer_id.property_account_position_id
        if fpos:
            account = fpos.map_account(account)

        taxes = product.taxes_id
        invoice.update({
            'invoice_line_ids': [(0, 0, {
                'name': product.name,
                'sequence': 10,
                'origin': self.name,
                'account_id': account.id,
                'price_unit': 1.0,
                'quantity': self.amount_transit_debours,
                'uom_id': product.uom_id.id,
                'product_id': product.id or False,
                'invoice_line_tax_ids': [(6, 0, taxes.ids)],
            })]
        })


class EtapesTransitFolder(models.Model):
    _name = 'stages.transit'
    _inherit = ['mail.thread']
    _description = 'Etapes de Transit'
    _order = "number asc"

    name = fields.Char("Etapes")
    number = fields.Integer("Numero Etape")
    stages = fields.Selection([('transit', 'Dedouanement'), ('accone', 'Acconage'), ('ship', 'Shipping')],
                              string="Processus")


class PortTransit(models.Model):
    _name = 'port.transit'
    _description = 'Port de Transit'

    name = fields.Char("Nom")


class ExportPortTransit(models.Model):
    _name = 'exportator.transit'
    _description = 'ExPort de Transit'

    name = fields.Char("Nom")


class ImportPortTransit(models.Model):
    _name = 'import.transit'
    _description = 'ImPort de Transit'

    name = fields.Char("Nom")


class ConsignatioTransit(models.Model):
    _name = 'consignee.transit'
    _description = 'Consignataire'

    name = fields.Char("Nom")


class PackageTransit(models.Model):
    _name = 'package.transit'
    _description = 'Package Transit'

    name = fields.Char(string='Name')

class NavireTransit(models.Model):
    _name = 'vessel.transit'
    _description = 'Description du Navire'

    name = fields.Char("Navire")
    active = fields.Boolean(default=True)


# class TransitMuksDms(models.Model):
#     _inherit = 'muk_dms.directory'
#
#     transit_id = fields.Many2one(
#         "folder.transit",
#         "Dossier"
#     )


class PackageFolder(models.Model):
    _name = 'package.folders'

    name = fields.Char("Numero du Conteneur", size=11, )
    package_type_id = fields.Many2one(
        'package.transit',
        string='Type de Conteneur',
    )
    date_receipt = fields.Date("Date Ticket de Livraison")
    date_output = fields.Date("Date de Sortie")
    date_delivered = fields.Date("Date Livraison Client")
    date_remove = fields.Date("Date retrait")
    date_return = fields.Date("Date Retour")
    transit_id = fields.Many2one(
        "folder.transit",
        "Dossier"
    )
