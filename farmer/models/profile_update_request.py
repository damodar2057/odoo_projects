from odoo import models, fields,api,_
from odoo.exceptions import ValidationError
import nepali_datetime

class ProfileUpdateRequest(models.Model):
    _name = 'profile.update.request'
    _description = 'Profile Update Request'
    _rec_name = 'ref'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']

    producer_type = fields.Selection([
        ('farmer','Farmer'),
        ('farmer_group','Farmer Group'),
        ('household','Household'),
        ('other','other')
    ],string='Producer Type', compute='_compute_producer_type')


    creation_date_bs = fields.Char("Creation Date", compute = "_obtain_creation_date_nepali")

    @api.depends('create_date')
    def _obtain_creation_date_nepali(self):
        for record in self:
            record.creation_date_bs = nepali_datetime.date.from_datetime_date(record.create_date.date())

    ref = fields.Char(readonly=1, default=lambda self: _('New'), string=_('Service ID'), )
    crop_ids = fields.One2many('farmer.crop', 'profile_update_id', string=_('Crops'))
    crop_ids_exists = fields.Boolean(compute="_compute_crop_ids_exists")

    def _compute_crop_ids_exists(self):
        for record in self:
            exists = False
            for val in  record.crop_ids:
                record.crop_ids_exists = True
                exists = True
                break
            if not exists:
                record.crop_ids_exists = False

    land_ids = fields.One2many('farmer.land', 'profile_update_id', string=_('Lands'))
    land_ids_exists = fields.Boolean(compute="_compute_land_ids_exists")

    def _compute_land_ids_exists(self):
        for record in self:
            exists = False
            for val in  record.land_ids:
                record.land_ids_exists = True
                exists = True
                break
            if not exists:
                record.land_ids_exists = False

    fish_ids = fields.One2many('farmer.fish', 'profile_update_id', string=_('Fish'))
    fish_ids_exists = fields.Boolean(compute="_compute_fish_ids_exists")

    def _compute_fish_ids_exists(self):
        for record in self:
            exists = False
            for val in  record.fish_ids:
                record.fish_ids_exists = True
                exists = True
                break
            if not exists:
                record.fish_ids_exists = False

    animal_ids = fields.One2many('farmer.animal', 'profile_update_id', string=_('Animal'))
    animal_ids_exists = fields.Boolean(compute="_compute_animal_ids_exists")

    def _compute_animal_ids_exists(self):
        for record in self:
            exists = False
            for val in  record.animal_ids:
                record.animal_ids_exists = True
                exists = True
                break
            if not exists:
                record.animal_ids_exists = False

    loan_ids = fields.One2many('farmer.loan', 'profile_update_id', string=_('Loan'))
    loan_ids_exists = fields.Boolean(compute="_compute_loan_ids_exists")

    def _compute_loan_ids_exists(self):
        for record in self:
            exists = False
            for val in  record.loan_ids:
                record.loan_ids_exists = True
                exists = True
                break
            if not exists:
                record.loan_ids_exists = False

    associated_ids = fields.One2many('associated.institute', 'profile_update_id', string=_('Associated Instutite'))
    associated_ids_exists = fields.Boolean(compute="_compute_associated_ids_exists")

    def _compute_associated_ids_exists(self):
        for record in self:
            exists = False
            for val in  record.associated_ids:
                record.associated_ids_exists = True
                exists = True
                break
            if not exists:
                record.associated_ids_exists = False

    document_ids = fields.One2many('farmer.documents', 'profile_update_id', string=_('Farmer Documents'))
    document_ids_exists = fields.Boolean(compute="_compute_document_ids_exists")

    def _compute_document_ids_exists(self):
        for record in self:
            exists = False
            for val in  record.document_ids:
                record.document_ids_exists = True
                exists = True
                break
            if not exists:
                record.document_ids_exists = False

    family_ids = fields.One2many('farmer.family', 'profile_update_id', string=_('Family'))
    family_ids_exists = fields.Boolean(compute="_compute_family_ids_exists")

    def _compute_family_ids_exists(self):
        for record in self:
            exists = False
            for val in  record.family_ids:
                record.family_ids_exists = True
                exists = True
                break
            if not exists:
                record.family_ids_exists = False

    local_production_ids = fields.One2many("local.production","profile_update_id",string="Local Productions")
    local_production_ids_exists = fields.Boolean(compute="_compute_local_production_ids_exists")

    def _compute_local_production_ids_exists(self):
        for record in self:
            exists = False
            for val in  record.local_production_ids:
                record.local_production_ids_exists = True
                exists = True
                break
            if not exists:
                record.local_production_ids_exists = False

    insurance_ids = fields.One2many("produce.insurance","profile_update_id",string="Local Productions")
    insurance_ids_exists = fields.Boolean(compute="_compute_insurance_ids_exists")

    def _compute_insurance_ids_exists(self):
        for record in self:
            exists = False
            for val in  record.insurance_ids:
                record.insurance_ids_exists = True
                exists = True
                break
            if not exists:
                record.insurance_ids_exists = False

    farmer_group_membership_ids = fields.One2many("farmer.group.member","profile_update_id",string="Local Productions")
    farmer_group_membership_ids_exists = fields.Boolean(compute="_compute_farmer_group_membership_ids_exists")

    def _compute_farmer_group_membership_ids_exists(self):
        for record in self:
            exists = False
            for val in  record.farmer_group_membership_ids:
                record.farmer_group_membership_ids_exists = True
                exists = True
                break
            if not exists:
                record.farmer_group_membership_ids_exists = False

    decline_reason = fields.Char("Reason for Request Decline")
    state = fields.Selection([
        ('Pending','Pending'),
        ('Approved','Approved'),
        ('Declined','Declined'),
        ('Canceled','Canceled'),
    ],default='Pending',readonly= True, string="State")

    farmer_id = fields.Many2one("farm.farmer",string="Farmer")
    farmer_group_id = fields.Many2one("farmer.group",string="Farmer Group")
    household_id = fields.Many2one('farm.household',string="Household")

    def _compute_producer_type(self):
        for record in self:
            if record.farmer_id:
                record.producer_type = 'farmer'
            elif record.household_id:
                record.producer_type= 'household'
            elif record.farmer_group_id:
                record.producer_type= 'farmer_group'
            else:
                record.producer_type = 'other'

    def approve_profile(self):
        if self.state not in ['Pending']:
            return
        self.state = 'Approved'
        if self.farmer_id:
            if self.crop_ids:
                self._update_user_data(self.farmer_id,"crop_ids")
            if self.land_ids:
                self._update_user_data(self.farmer_id,"land_ids")
            if self.fish_ids:
                self._update_user_data(self.farmer_id,"fish_ids")
            if self.animal_ids:
                self._update_user_data(self.farmer_id,"animal_ids")
            if self.loan_ids:
                self._update_user_data(self.farmer_id,"loan_ids")
            if self.associated_ids:
                self._update_user_data(self.farmer_id,"associated_ids")
            if self.document_ids:
                self._update_user_data(self.farmer_id,"document_ids")
            if self.family_ids:
                self._update_user_data(self.farmer_id,"family_ids")
            if self.local_production_ids:
                self._update_user_data(self.farmer_id,"local_production_ids")
            if self.farmer_group_membership_ids:
                self._update_user_data(self.farmer_id,"farmer_group_membership_ids")
            if self.insurance_ids:
                self._update_user_data(self.farmer_id,"insurance_ids")
            self.farmer_id.requesting = False
        if self.farmer_group_id:
            if self.crop_ids:
                self._update_user_data(self.farmer_group_id,"crop_ids")
            if self.land_ids:
                self._update_user_data(self.farmer_group_id,"land_ids")
            if self.fish_ids:
                self._update_user_data(self.farmer_group_id,"fish_ids")
            if self.animal_ids:
                self._update_user_data(self.farmer_group_id,"animal_ids")
            if self.loan_ids:
                self._update_user_data(self.farmer_group_id,"loan_ids")
            if self.associated_ids:
                self._update_user_data(self.farmer_group_id,"associated_ids")
            if self.document_ids:
                self._update_user_data(self.farmer_group_id,"document_ids")
            if self.local_production_ids:
                self._update_user_data(self.farmer_group_id,"local_production_ids")
            if self.farmer_group_membership_ids:
                self._update_user_data(self.farmer_group_id,"farmer_group_membership_ids")
            self.farmer_group_id.requesting = False
        elif self.household_id:
            if self.local_production_ids:
                self._update_user_data(self.household_id,"local_production_ids")
            self.household_id.requesting = False
        else:
            pass
          
    def _update_user_data(self,user_id,one2many_ids_key):
        for each in self[one2many_ids_key]:
            if each.xchg:
                each.farmer_id = self.farmer_id
                each.xchg.unlink()
            if each.delete_request:
                each.unlink()
        user_id[one2many_ids_key]=self[one2many_ids_key]
    
    def decline_profile(self):
        if self.state not in ['Pending']:
            return
        self.state='Declined'
        if self.farmer_id:
            if self.crop_ids:
                self._update_user_data_on_decline(self.farmer_id,"crop_ids")
            if self.land_ids:
                self._update_user_data_on_decline(self.farmer_id,"land_ids")
            if self.fish_ids:
                self._update_user_data_on_decline(self.farmer_id,"fish_ids")
            if self.animal_ids:
                self._update_user_data_on_decline(self.farmer_id,"animal_ids")
            if self.loan_ids:
                self._update_user_data_on_decline(self.farmer_id,"loan_ids")
            if self.associated_ids:
                self._update_user_data_on_decline(self.farmer_id,"associated_ids")
            if self.document_ids:
                self._update_user_data_on_decline(self.farmer_id,"document_ids")
            if self.family_ids:
                self._update_user_data_on_decline(self.farmer_id,"family_ids")
            if self.local_production_ids:
                self._update_user_data_on_decline(self.farmer_id,"local_production_ids")
            if self.insurance_ids:
                self._update_user_data_on_decline(self.farmer_id,"insurance_ids")
            if self.farmer_group_membership_ids:
                self._update_user_data_on_decline(self.farmer_id,"farmer_group_membership_ids")
            self.farmer_id.requesting = False
        if self.farmer_group_id:
            if self.crop_ids:
                self._update_user_data_on_decline(self.farmer_group_id,"crop_ids")
            if self.land_ids:
                self._update_user_data_on_decline(self.farmer_group_id,"land_ids")
            if self.fish_ids:
                self._update_user_data_on_decline(self.farmer_group_id,"fish_ids")
            if self.animal_ids:
                self._update_user_data_on_decline(self.farmer_group_id,"animal_ids")
            if self.loan_ids:
                self._update_user_data_on_decline(self.farmer_group_id,"loan_ids")
            if self.associated_ids:
                self._update_user_data_on_decline(self.farmer_group_id,"associated_ids")
            if self.document_ids:
                self._update_user_data_on_decline(self.farmer_group_id,"document_ids")
            if self.family_ids:
                self._update_user_data_on_decline(self.farmer_group_id,"family_ids")
            if self.local_production_ids:
                self._update_user_data_on_decline(self.farmer_group_id,"local_production_ids")
            if self.insurance_ids:
                self._update_user_data_on_decline(self.farmer_group_id,"insurance_ids")
            if self.farmer_group_membership_ids:
                self._update_user_data_on_decline(self.farmer_group_id,"farmer_group_membership_ids")
            self.farmer_group_id.requesting = False
        elif self.household_id:
            if self.local_production_ids:
                self._update_user_data_on_decline(self.household_id,"local_production_ids")
        else:
            pass
        if self.decline_reason == False:
            raise ValidationError(_("Enter a Reason for Declining the request"))
          
    def _update_user_data_on_decline(self,user_id,one2many_ids_key):
        for each in self[one2many_ids_key]:
            if each.delete_request:
                each.delete_request=False
        # user_id[one2many_ids_key]=self[one2many_ids_key]

    def cancel_profile(self):
        if self.state not in ['Pending']:
            return
        self.state = 'Canceled'
        
    @api.model
    def create(self, vals):
        vals['ref'] = self.env['ir.sequence'].next_by_code("farmer.profile.update.request.sequence")
        return super(ProfileUpdateRequest, self).create(vals)