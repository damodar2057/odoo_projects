from odoo import models,fields,api


class VehicleRequestByOfficeEmployee(models.Model):
    _name="vehicle.request.office.employee"

    vehicle_id = fields.Many2one('fleet.vehicle',"Requested Vehicle",ondelete='cascade')
    requested_by = fields.Many2one('res.users',string="Requested By",ondelete='cascade')
    purpose = fields.Char("Purpose")
    requested_duration = fields.Integer("Requested Duration")
    use_date = fields.Datetime("Requested Date")
    start_point = fields.Char("Start Point")
    destination_point = fields.Char("Destination Point")
    state = fields.Selection([
        ('New Request', 'New Request'),
        ('Accept', 'Accepted'),
        ('Reject', 'Rejected'),
        ('Done', 'Done'),
    ], default='New Request', readonly=True, string="State", tracking=True)
            
    def accept_request(self):
        self.state = 'Accept'
        return self.action_quotation_send_mail()
    
    def reject_request(self):
        self.state = 'Reject'
    
    def mark_as_done(self):
        self.state = 'Done'
    
    def mark_as_undo(self):
        self.state = 'Accept'
        
    
    def action_quotation_send_mail(self):
        print("hello")
        self.ensure_one()
        lang = self.env.context.get('lang')
        template_ref = self.env.ref('vehicle_tracking.document_renewal_email_template')
        mail_template = template_ref
        if mail_template and mail_template.lang:
            lang = mail_template._render_lang(self.ids)[self.id]

        ctx = {
            'default_model': 'vehicle.request.office.employee',
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