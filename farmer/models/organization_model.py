from odoo import models, fields,api, _
import nepali_datetime
from odoo.exceptions import ValidationError

class FiscalYear(models.Model):
    _name = 'fiscal.year'
    _rec_name = 'fiscal_year'

    fiscal_year = fields.Char(string=_('Fiscal Year'))



class OrganizationType(models.Model):
    _name = 'organization.type'
    _rec_name = 'type'

    type = fields.Char(string=_('Type'))


class OrganizationNature(models.Model):
    _name = 'organization.nature'
    _rec_name = 'nature'

    nature = fields.Char(string=_('Nature'))


class OrgClosingReason(models.Model):
    _name = 'organization.closing.reason'
    _rec_name = 'reason'

    reason = fields.Char(string=_('Reason'))


class Organization(models.Model):
    _name = "organization.farmer"
    _description = "Organization Farmer"
    _inherits = {'res.partner': 'partner_id'}


    # Relational Fields
    partner_id = fields.Many2one('res.partner', required=True, ondelete='restrict', auto_join=True, index=True,
                                 string='Related Partner', help='Partner-related data of the user',)

    type = fields.Many2one('organization.type',string=_('Organization Type'))
    nature = fields.Many2one('organization.nature',string=_('Organization Nature'))
    registration_number = fields.Char(string=_('Registration Number'))
    registration_date = fields.Date(string=_('Registration Date'),compute="_obtain_registration_date_ad")
    registration_date_bs = fields.Char(string=_('Registration Date(B.S.)'),required=False)
    registration_district = fields.Many2one('location.district',string=_('Registration District'))

    #organization functional details
    start_date = fields.Date(string=_('Start Date'),compute="_obtain_start_date_ad")
    start_date_bs = fields.Char(string=_('Start Date(B.S.)'),required=False)

    close_date = fields.Date(string=_('Close Date'),compute="_obtain_close_date_ad")
    close_date_bs = fields.Char(string=_('Close Date(B.S.)'),required=False)

    recent_paid_tax_year = fields.Many2one('fiscal.year',string=_('Recent Tax Paid Year'))
    yearly_transaction = fields.Float(string=_('Yearly Transaction'))


    #local regsitration details
    local_reg_number = fields.Char(string=_('VDC/Municipality Registration Number'))
    local_reg_date_bs = fields.Char(string=_("Registation Date(B.S.)"))
    local_reg_date = fields.Date(string=_("Registation Date"),compute="_obtain_local_registration_date_ad")


    @api.depends('local_reg_date_bs')
    def _obtain_local_registration_date_ad(self):
        for record in self:
            if record.local_reg_date_bs:
                record.local_reg_date = nepali_datetime.datetime.strptime(record.local_reg_date_bs, '%Y-%m-%d').to_datetime_date()
            else:
                record.local_reg_date=None

    @api.depends('start_date_bs')
    def _obtain_start_date_ad(self):
        for record in self:
            if record.start_date_bs:
                record.start_date = nepali_datetime.datetime.strptime(record.start_date_bs, '%Y-%m-%d').to_datetime_date()
            else:
                record.start_date=None

    @api.depends('close_date_bs')
    def _obtain_close_date_ad(self):
        for record in self:
            if record.close_date_bs:
                record.close_date = nepali_datetime.datetime.strptime(record.close_date_bs, '%Y-%m-%d').to_datetime_date()
            else:
                record.close_date=None

    @api.depends('registration_date_bs')
    def _obtain_registration_date_ad(self):
        for record in self:
            record.registration_date = nepali_datetime.datetime.strptime(record.registration_date_bs, '%Y-%m-%d').to_datetime_date()

    pan_number = fields.Char(string=_('Pan Number'))
    #location fields Many2one
    province = fields.Many2one('location.province',string=_('Province'))
    district = fields.Many2one('location.district',string=_('District'))
    palika = fields.Many2one('location.palika',string=_('Palika'))
    ward_no = fields.Integer(string=_('Ward No'),required=False)
    tole = fields.Many2one('location.tole',string=_('Tole'))

    # photo = fields.Binary(string=_('Photo'))

    #organization registation related fields
    
    @api.constrains('number')
    def action_save(self):
        # self.ensure_one()
        self.write({})
        return True

    def action_cancel(self):
        self.ensure_one()
        return {'type': 'ir.actions.act_window_close'}





