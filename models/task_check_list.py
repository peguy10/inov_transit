# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import html2plaintext, clean_context


class TaskChecklist(models.Model):
    _inherit = 'mail.activity.type'

    stages = fields.Selection([('transit', 'Dedouanement'), ('accone', 'Acconage'), ('ship', 'Shipping')],
                              string="Processus")
    responsible_id = fields.Many2one(
        'res.users',
        string='Poste',
    )


class TaskActivityTransit(models.Model):
    _inherit = 'mail.activity'

    model_transit_id = fields.Many2one(
        'folder.transit',
        string='Dossier',
        compute='compute_folder_transit_field',
    )

    stages = fields.Selection([('transit', 'Dedouanement'), ('accone', 'Acconage'), ('ship', 'Shipping')],
                              string="Processus")


    @api.depends('res_id')
    def compute_folder_transit_field(self):
        for record in self:
            if record.res_id:
                record.model_transit_id = self.env['folder.transit'].browse(record.res_id).id

    
    
    def action_feedback(self, feedback=False, attachment_ids=None):
        for activity in self:
            vals = {
                    'name': activity.activity_type_id.name,
                    'responsible_id': activity.user_id.name,
                    'date_start': activity.date_deadline,
                    'date_dealine': fields.Date.today(),
                    'folder_id': activity.res_id,
                }
            self.env['task.checklist'].create(vals)
        messages, _next_activities = self.with_context(
            clean_context(self.env.context)
        )._action_done(feedback=feedback, attachment_ids=attachment_ids)
        return messages[0].id if messages else False
       
      
    # def action_feedback(self, feedback=False):
    #     message = self.env['mail.message']
    #     if feedback:
    #         self.write(dict(feedback=feedback))
    #     for activity in self:
    #         if activity.user_id != self.env.user:
    #             raise ValidationError(
    #                 _("L'utilisateur %s n'a pas le droit de confirmer cette Tache, seul %s Doit la validée, Merci!") % (
    #                 self.env.user.name, activity.user_id.name))
    #         record = self.env[activity.res_model].browse(activity.res_id)
    #         record.message_post(
    #             'mail.message_activity_done',
    #             values={'activity': activity},
    #             subtype_id=self.env['ir.model.data']._xmlid_to_res_id('mail.mt_activities'),
    #             mail_activity_type_id=activity.activity_type_id.id,
    #         )
    #         message |= record.message_ids[0]
    #         vals = {
    #             'name': activity.activity_type_id.name,
    #             'responsible_id': activity.user_id.name,
    #             'date_start': activity.date_deadline,
    #             'date_dealine': fields.Date.today(),
    #             'folder_id': activity.res_id,
    #         }
    #         self.env['task.checklist'].create(vals)
    #         self.unlink()
    #     return message.ids and message.ids[0] or False
    # def action_feedback(self, feedback=False):
    #     message = self.env['mail.message']
    #     if feedback:
    #         self.write(dict(feedback=feedback))
    #     for activity in self:
    #         if activity.user_id != self.env.user:
    #             raise ValidationError(
    #                 _("L'utilisateur %s n'a pas le droit de confirmer cette Tache, seul %s Doit la validée, Merci!") % (
    #                 self.env.user.name, activity.user_id.name))
    #         record = self.env[activity.res_model].browse(activity.res_id)
    #         record.message_post_with_view(
    #             'mail.message_activity_done',
    #             values={'activity': activity},
    #             subtype_id=self.env['ir.model.data'].xmlid_to_res_id('mail.mt_activities'),
    #             mail_activity_type_id=activity.activity_type_id.id,
    #         )
    #         message |= record.message_ids[0]
    #         vals = {
    #             'name': activity.activity_type_id.name,
    #             'responsible_id': activity.user_id.name,
    #             'date_start': activity.date_deadline,
    #             'date_dealine': fields.Date.today(),
    #             'folder_id': activity.res_id,
    #         }
    #         self.env['task.checklist'].create(vals)
    #         self.unlink()
    #     return message.ids and message.ids[0] or False
class TaskTransitChecklist(models.Model):
    _name = 'task.checklist'
    _description = 'Checklist for the task'

    name = fields.Char(string='Name', required=True)
    responsible_id = fields.Char(
        string='Poste',
    )
    description = fields.Char("Observation")
    date_dealine = fields.Date("Date Validation", required=True)
    date_start = fields.Date("Date Creation de la tache", required=True)
    folder_id = fields.Many2one("folder.transit", string="Dossier")


