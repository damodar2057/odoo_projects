from odoo import models, fields, api
from datetime import datetime,timedelta

class RenewalDocuments(models.Model):
    _name = 'renewal.documents'

    document_id = fields.Many2one('document.list')
    expiry_date = fields.Date("Expiry Date")
    fleet_id = fields.Many2one("fleet.vehicle",string="Fleet")
    driver_id = fields.Many2one("driver.details",string="Driver")
    
    def send_expiry_notifications(self):
        # retrieve renewal alert period from configuration settings
        renewal_alert_period = int(self.env['ir.config_parameter'].sudo().get_param('vehicle_tracking.renewal_alert_period',default=30))
        
        today = fields.Date.today()
        expiration_date = today + timedelta(days=renewal_alert_period)

        # find documents expiring soon
        expiring_documents = self.env['renewal.documents'].sudo().search([
            ('expiry_date','<=',expiration_date),
            
            ])
        for document in expiring_documents:
            print("Hello")
            print(f"Your {document.document_id.name} is expiring in {document.expiry_date}")
            template_ref = self.env.ref('vehicle_tracking.document_renewal_email_template')
            return template_ref.send_mail(self.id, force_send=True)
        
    def action_quotation_send_mail(self):
        print("hello")
        lang = self.env.context.get('lang')
        template_ref = self.env.ref('vehicle_tracking.document_renewal_email_template')
        mail_template = template_ref
        if mail_template and mail_template.lang:
            lang = mail_template._render_lang(self.ids)[self.id]

        ctx = {
            'default_model': 'renewal.documents',
            'default_res_id': self.id,
            'default_use_template': bool(mail_template),
            'default_template_id': mail_template.id if mail_template else None,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'default_email_layout_xmlid': 'mail.mail_notification_layout_with_responsible_signature',
            'proforma': self.env.context.get('proforma', False),
            'force_email': True,

        }
        print(ctx)
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }

class DocumentList(models.Model):
    _name = 'document.list'
    _rec_name = "name"

    name = fields.Char("Document")


