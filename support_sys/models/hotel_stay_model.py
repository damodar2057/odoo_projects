from odoo import models, fields, api
from datetime import datetime

class HotelStayReport(models.Model):
    _name = 'hotel.stay.model'
    _description = 'Employee Stay'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    employee_id = fields.Many2one('hr.employee',"Employee")
    residence = fields.Char('Residence')
    hotel_name = fields.Char('Hotel')
    hotel_detail = fields.Char('Hotel Detail')
    contact_person = fields.Char('Contact Person')
    contact_number = fields.Char('Contact Number')
    client_id = fields.Many2one('client.info','Office')
    estimated_accomodation_expenditure = fields.Float('Stay Expenditure')
    estimated_meals_expenditure = fields.Float('Meals Expenditure')
    supporting_documents = fields.Binary('Bill Image')

class CompanyService(models.Model):
    _name = 'company.services'
    _description = 'Company Service'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    service_name = fields.Char("Company Service")
    url = fields.Char("Url")
    demo_login_id = fields.Char("Demo Login ID")
    demo_login_password = fields.Char("Demo Login Password")

class CompanyBankDetails(models.Model):
    _name = 'company.bank.details'
    _description = 'Company Bank Details'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    account_name = fields.Char("A/C Holder Name")
    account_number = fields.Char("A/C Number")
    bank_name = fields.Char("Bank")
    branch_name = fields.Char("Branch")
