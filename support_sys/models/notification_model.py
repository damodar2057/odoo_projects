# notification_model.py
from odoo import fields, models


class NotificationModel(models.Model):
    _name = "notification.model"

    message_seen_status = fields.Boolean("Status", default=False)
    emp_id = fields.Many2one('hr.employee',string="Employee")
    message = fields.Char("Message")
    sent_to = fields.Many2one("res.users")
    sent_at = fields.Datetime("Sent at",default=fields.Datetime.now())