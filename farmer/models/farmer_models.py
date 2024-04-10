from odoo import models, fields,api,_
import qrcode
import nepali_datetime
import base64
from io import BytesIO
from odoo.exceptions import ValidationError
from . import organization_model


class Producer(models.Model):
    _name = 'farm.producer'
    _inherits = {'res.users': 'user_id'}

    # Relational Fields
    user_id = fields.Many2one('res.users', required=True, ondelete='restrict', auto_join=True, index=True,
                              string=_('Related User'))
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string=_('Gender'),required=False)
    allowed_warehouses = fields.Many2many("stock.warehouse")

    @api.model
    def create(self, vals_list):
        if 'mobile' not in vals_list or not vals_list['mobile']:
            raise ValidationError('Mobile Number is required')

        vals_list['login'] = vals_list['mobile']
        vals_list['password'] = vals_list['mobile']
        user = super(Producer, self).create(vals_list)
        # Define the names of the access groups you want to assign by default
        default_access_groups = ['FIS/ User Producer Farmer Access']

        # Find the access groups by name
        access_groups = self.env['res.groups'].search([('name', 'in', default_access_groups)])

        # Assign the user to the found access groups
        user.write({'groups_id': [(4, group.id) for group in access_groups]})

        return user


class Household(models.Model):
    _name = 'farm.household'
    _description = 'Household Producer'
    _inherits = {'farm.producer': 'producer_id'}

    producer_id = fields.Many2one('farm.producer',store=True, required=True, ondelete='restrict', auto_join=True, index=True, string=_('Related Partner'), help='Partner-related data of the user',)
    ref = fields.Char(readonly=1,default=lambda self: _('New'), string=_('Household Producer Sequence ID'), )
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string=_('Gender'),required=False)
    # contact_no = fields.Char(string=_('Contact Number'),required=False)
    date_of_birth = fields.Date(string=_('Date of Birth(A.D)'),required=False,compute='_obtain_dob_in_ad')
    date_of_birth_bs = fields.Char(string=_('Date of Birth(B.S.)'),required=False)

    @api.depends('date_of_birth_bs')
    def _obtain_dob_in_ad(self):
        for record in self:
            record.date_of_birth = nepali_datetime.datetime.strptime(record.date_of_birth_bs, '%Y-%m-%d').to_datetime_date()

    # Tax Information
    pan_no = fields.Char(string=_('PAN Number'),required=False)

    local_production_ids = fields.One2many("local.production","household_id",string="Local Productions")
    # Identity Documents
    citizenship_number = fields.Char(string=_('Citizenship Number'),required=False)
    citizenship_issue_district = fields.Many2one('location.district',string=_('District'))
    citizenship_issue_date = fields.Date(string=_('Issue Date(A.D.)'),required=False,compute='_obtain_citzenship_issue_date_ad')
    citizenship_issue_date_bs = fields.Char(string=_('Issue Date(B.S.)'),required=False)

    @api.depends('citizenship_issue_date_bs')
    def _obtain_citzenship_issue_date_ad(self):
        for record in self:
            record.citizenship_issue_date = nepali_datetime.datetime.strptime(record.citizenship_issue_date_bs, '%Y-%m-%d').to_datetime_date()

    # Location Information
    province = fields.Many2one('location.province',string=_('Province'))
    district = fields.Many2one('location.district',string=_('District'))
    palika = fields.Many2one('location.palika',string=_('Palika'))
    ward_no = fields.Integer(string=_('Ward No'),required=False)
    tole = fields.Many2one('location.tole',string=_('Tole'))

    dynamic_state = fields.Selection([
        ('false', 'Select State'),
        ('Pending','Pending'),
        ('Approved','Approved'),
        ('Declined','Declined'),
        ('Canceled','Canceled'),
    ],default='false', string="State",store=False) 

    requesting = fields.Boolean("Requesting Profile Update",default = False)


    @api.model
    def create(self, vals):
        vals['ref'] = self.env['ir.sequence'].next_by_code("household.sequence")
        return super(Household, self).create(vals)
    
    @api.onchange('dynamic_state')
    def calc_domain(self):
        for record in self:
            domain = [('household_id','=',self._origin.id)]
            if self.dynamic_state == 'Pending':
                domain += [('state', '=', 'Pending')]
            elif self.dynamic_state == 'Approved':
                domain += [('state', '=', 'Approved')]
            elif self.dynamic_state == 'Declined':
                domain += [('state', '=', 'Declined')]
            elif self.dynamic_state == 'Canceled':
                domain += [('state', '=', 'Canceled')]
            record.profile_update_request_ids = self.env["profile.update.request"].search(domain)

    profile_update_request_ids = fields.One2many("profile.update.request","farmer_id", string="Profile Update Requests",compute=calc_domain)

    def return_associated_model(self,key):
        if key=='crop_ids':
            return 'farmer.crop'
        if key=='land_ids':
            return 'farmer.land'
        if key=='fish_ids':
            return 'farmer.fish'
        if key=='animal_ids':
            return 'farmer.animal'
        if key=='loan_ids':
            return 'farmer.loan'
        if key=='associated_ids':
            return 'associated.institute'
        if key=='document_ids':
            return 'farmer.documents'
        if key=='family_ids':
            return 'farmer.family'
        if key=='local_production_ids':
            return 'local.production'
        if key=='farmer_group_membership_ids':
            return 'farmer.group.member'

    @api.model
    def write(self, *args, **kwargs):
        if len(args)>1:
            household = self.env['farm.household'].search([('id','in',args[0])])[0]
        else:
            household = self
        values = args[-1]
        '''
        execute normal write in two cases
        1. if the logged in user has group_user_access.
        2. if the only value to change is of field requesting.
        '''
        if self.env.user.user_has_groups('farmer.group_user_access') or (len(values)==1 and "requesting" in values.keys()):
            super(Household, household).write(values)
            return
            
        requesting_values = {
            'local_production_ids':values.pop("local_production_ids") if "local_production_ids" in values  else None,
            'household_id':household.id
        }

        model_obj = {}

        for key,value in requesting_values.items():
            if value is not None:
                model_name=self.return_associated_model(key)

                if model_name:
                    model_orm=self.env[model_name]
                    if type(value)==list:

                        for [_,ref_id,req_value] in value:
                            if req_value:
                                if type(ref_id) == str:
                                    continue
                                curr_model = model_orm.search([['id','=',ref_id]])

                                if curr_model:
                                    curr_model.xchg = curr_model.copy()
                                    curr_model.household_id=None
                                    model_obj[key] = curr_model

        super(Household, household).write(values)

        '''
        farmer.requesting is True when a one2many data is deleted
        in which case a profile.update.request is already created 
        so for this case the most recently created profile.update.request 
        for this farmer.id is referenced.
        '''
        if household.requesting:
            res = self.env['profile.update.request'].search([('household_id','=',household.id)],order = 'ref desc',limit = 1)[0]
            res.write(requesting_values)
            household.requesting = False
        elif sum([0 if requesting_values[i]==None else 1 for i in requesting_values])>1:
            res = self.env['profile.update.request'].create(requesting_values)
            household.requesting = False

        for [field_name,record] in model_obj.items():
            res[field_name] += record


    @api.constrains('requesting')
    def _send_request(self):
        if not self.requesting:
            return
        requesting_values = {
            'local_production_ids':self["local_production_ids"],
            'household_id':self.id
        }
        if sum([0 if requesting_values[i]==None else 1 for i in requesting_values])>1:
            res = self.env['profile.update.request'].create(requesting_values)

    def goto_website(self):
        return {
            'type': 'ir.actions.act_url',
            'target': 'self',
            'url': '',
        }
        # return self.env.ref('website.website_preview').read()[0]

class Farmer(models.Model):
    _name = 'farm.farmer'
    _description = 'Farm Farmer'
    _inherits = {'farm.producer': 'producer_id'}

    producer_id = fields.Many2one('farm.producer',store=True, required=True, ondelete='restrict', auto_join=True, index=True, string=_('Related Partner'), help='Partner-related data of the user',)
    ref = fields.Char(readonly=1,default=lambda self: _('New'), string=_('Farmer Sequence ID'), )

    # contact_no = fields.Char(string=_('Contact Number'),required=False)
    date_of_birth = fields.Date(string=_('Date of Birth(A.D)'),required=False,compute='_obtain_dob_in_ad')
    date_of_birth_bs = fields.Char(string=_('Date of Birth(B.S.)'),required=False)

    @api.depends('date_of_birth_bs')
    def _obtain_dob_in_ad(self):
        for record in self:
            if record.date_of_birth_bs:
                record.date_of_birth = nepali_datetime.datetime.strptime(record.date_of_birth_bs, '%Y-%m-%d').to_datetime_date()
            else:
                record.date_of_birth = None

    agriculture_activites = fields.Many2many('farmer.agriculture.activities', string=_('Agriculture Activity'))

    # Farmer Annual Income
    business_name = fields.Char(string=_('Business Name'))
    agriculture_income = fields.Float(string=_('Agriculture Income'))
    other_income = fields.Float(string=_('Other Income'))

    # Tax Information
    pan_no = fields.Char(string=_('PAN Number'),required=False)

    # Identity Documents
    citizenship_number = fields.Char(string=_('Citizenship Number'),required=False)
    citizenship_issue_district = fields.Many2one('location.district',string=_('District'))
    citizenship_issue_date = fields.Date(string=_('Issue Date(A.D.)'),required=False,compute='_obtain_citzenship_issue_date_ad')
    citizenship_issue_date_bs = fields.Char(string=_('Issue Date(B.S.)'),required=False)


    yearly_investment=fields.Integer(_("Yearly Investment"))
    yearly_transaction=fields.Integer(_("Yearly Transaction"))
    min_monthly_income=fields.Integer(_("Min Income/Month"))
    family_contribution=fields.Integer(_("Family Contribution"))
    num_employees=fields.Integer(_("No. of Employees"))
    num_experience=fields.Integer(_("No. Experiences"))
    ability_and_technology=fields.Selection(selection=[
        ('trained_and_advanced_tech','Trained and Advanced Tech'),
        ('trained_and_mid_tech','Trained and Mid Tech'),
        ('mid_tech','Mid Tech'),
        ('mixed','Mixed')],string="Ability and Technology")
    
    
    @api.depends('citizenship_issue_date_bs')
    def _obtain_citzenship_issue_date_ad(self):
        for record in self:
            if record.citizenship_issue_date_bs:
                record.citizenship_issue_date = nepali_datetime.datetime.strptime(record.citizenship_issue_date_bs, '%Y-%m-%d').to_datetime_date()
            else:
                record.citizenship_issue_date = None

    @api.constrains('create_uid', 'citizenship_number', 'citizenship_issue_district', 'citizenship_issue_date')
    def check_unique_citizenship_id(self):
        for record in self:
            same_record = self.search([('create_uid', '=', record.create_uid.id)])

            for other_record in same_record:
                if (
                    other_record != record and
                    (
                        other_record.citizenship_number == record.citizenship_number and
                        other_record.citizenship_issue_district == record.citizenship_issue_district and
                        other_record.citizenship_issue_date == record.citizenship_issue_date
                    )
                ):
                    raise ValidationError("Citizenship Card Already In Use")

    # one2many pages fields
    crop_ids = fields.One2many('farmer.crop', 'farmer_id', string=_('Crops'))
    land_ids = fields.One2many('farmer.land', 'farmer_id', string=_('Lands'))
    fish_ids = fields.One2many('farmer.fish', 'farmer_id', string=_('Fish'))
    animal_ids = fields.One2many('farmer.animal', 'farmer_id', string=_('Animal'))
    loan_ids = fields.One2many('farmer.loan', 'farmer_id', string=_('Loan'))
    associated_ids = fields.One2many('associated.institute', 'farmer_id', string=_('Associated Instutite'))
    document_ids = fields.One2many('farmer.documents', 'farmer_id', string=_('Farmer Documents'))
    service_lists = fields.Many2many('services.lists', string=_('Service Lists'))
    family_ids = fields.One2many('farmer.family', 'farmer_id', string=_('Family'))
    local_production_ids = fields.One2many("local.production","farmer_id",string="Local Productions")
    insurance_ids = fields.One2many("produce.insurance","farmer_id",string="Produce Insurance")
    #associated farmer group
    farmer_group_membership_ids = fields.One2many('farmer.group.member','farmer_id',string="Farmer Group")
    # Location Information
    province = fields.Many2one('location.province',string=_('Province'))
    district = fields.Many2one('location.district',string=_('District'))
    palika = fields.Many2one('location.palika',string=_('Palika'))
    ward_no = fields.Integer(string=_('Ward No'),required=False)
    tole = fields.Many2one('location.tole',string=_('Tole'))
    full_address = fields.Char("Address",compute="_compute_full_address")

    def _compute_full_address(self):
        for record in self:
            temp=""
            if record.palika:
                temp+=record.palika.palika_name
            if record.ward_no:
                temp+=' - '+record.ward_no+', '
            if record.district:
                temp+=record.district.district_name+', '
            if record.province:
                temp+=record.province.name
            
            record.full_address = temp


    latitude = fields.Char(string=_('Latitude'))
    longitude = fields.Char(string=_('Longitude'))
    qr_code = fields.Binary(compute='_generate_qr_code',string="QR Code")
    farmer_group=fields.Many2one("farmer.type",string=_("Farmer Group"))
    dynamic_state = fields.Selection([
        ('false', 'Select State'),
        ('Pending','Pending'),
        ('Approved','Approved'),
        ('Declined','Declined'),
        ('Canceled','Canceled'),
    ],default='false', string=_("State"),store=False)  
    
    def action_open_farmer_group_wizard(self):
        return {
        'name': 'Farmer Group Data',
        'type': 'ir.actions.act_window',
        'view_type': 'form',
        'view_mode': 'form',
        'res_model': 'farmer.group.metadata',
        'target': 'new',
    }


    @api.onchange('dynamic_state')
    def calc_domain(self):
        for record in self:
            domain = [('farmer_id','=',self._origin.id)]
            if self.dynamic_state == 'Pending':
                domain += [('state', '=', 'Pending')]
            elif self.dynamic_state == 'Approved':
                domain += [('state', '=', 'Approved')]
            elif self.dynamic_state == 'Declined':
                domain += [('state', '=', 'Declined')]
            elif self.dynamic_state == 'Canceled':
                domain += [('state', '=', 'Canceled')]
            record.profile_update_request_ids = self.env["profile.update.request"].search(domain)

    profile_update_request_ids = fields.One2many("profile.update.request","farmer_id", string="Profile Update Requests",compute=calc_domain)
    requesting = fields.Boolean("Requesting Profile Update",default = False)

    def open_farmer_group_metadata(self):
        pass

    # @api.depends()
    def _generate_qr_code(self):
        vals = self.env["farm.farmer"].search_read([('id','=',self.id)])[0]
        val_list = [
            'id', 'producer_id', 'ref', 'gender', 'agriculture_activites', 
            'business_name', 'agriculture_income', 'other_income', 'pan_no', 'citizenship_number', 
            'citizenship_issue_district', 'crop_ids', 'land_ids', 'fish_ids', 
            'animal_ids', 'loan_ids', 'associated_ids', 'document_ids', 'service_lists', 'family_ids', 
            'local_production_ids', 'province', 'district', 'palika', 'ward_no', 'tole', 'latitude', 'longitude', 
            'name', 'lang','vat','email',  'phone', 'mobile', 
        ]
        new_vals={}
        for key in vals:
            if key in val_list:
                new_vals[key]=self[key]

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=3,
            border=4,
        )
        qr.add_data('http://localhost:8069/report/html/%s/%s?enable_editor' % ('farmer.action_farmer_id_report_preview', self.id))
        qr.make(fit=True)
        img = qr.make_image()
        temp = BytesIO()
        img.save(temp, format="PNG")
        qr_image = base64.b64encode(temp.getvalue())
        self.qr_code = qr_image
        
        
    # def assign_farmer_group(self,vals):
    #     farmer_group_orm=self.env["farmer.type"]
    #     farmer_groups=farmer_group_orm.search([])
        
    #     ability_and_technology=vals.get('ability_and_technology')
    #     num_experience=vals.get('num_experience')
    #     num_employees=vals.get('num_employees')
    #     family_contribution=vals.get('family_contribution')
    #     min_monthly_income=vals.get('min_monthly_income')
    #     yearly_transaction=vals.get('yearly_transaction')
    #     yearly_investment=vals.get('yearly_investment')
    #     match_group=None
    #     match_value_counts=0
        
    #     for group in farmer_groups:
    #         check_num_experience=group._check_range('num_experience',num_experience,id=group.id,is_gte=True)
    #         check_num_employees=group._check_range('num_employees',num_employees,is_gte=False,id=group.id)
    #         check_family_contribution=group._check_range('family_contribution',family_contribution,id=group.id,is_gte=False)
    #         check_min_monthly_income=group._check_range('min_monthly_income',min_monthly_income,id=group.id,is_gte=True)
    #         check_yearly_transaction=group._check_range('yearly_transaction',yearly_transaction,is_gte=False,id=group.id)
    #         check_yearly_investment=group._check_range('yearly_investment',yearly_investment,is_gte=False,id=group.id)
    #         check_ability_and_technology_truth=ability_and_technology==group.ability_and_technology
    #         group_truth_values=[check_num_experience,check_num_employees,check_family_contribution,check_min_monthly_income,check_yearly_transaction,check_yearly_investment,check_ability_and_technology_truth]
    #         print(group_truth_values)
    #         curr_match_value_counts=sum(group_truth_values)
    #         print(group_truth_values,curr_match_value_counts,group.id)
    #         if curr_match_value_counts > match_value_counts:
    #             match_group=group
    #             match_value_counts=curr_match_value_counts
    #     print(match_group)
        
    #     return match_group

            
    def goto_website(self):
        return {
            'type': 'ir.actions.act_url',
            'target': 'self',
            'url': '',
        }
        # return self.env.ref('website.website_preview').read()[0]

    def print_farmer_id(self):
        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': '/report/html/%s/%s?enable_editor' % ('farmer.action_farmer_id_report_preview', self.id),
        }

    @api.model
    def create(self, vals):
        vals['ref'] = self.env['ir.sequence'].next_by_code("farmer.sequence")
        return super(Farmer, self).create(vals)
    

    def return_associated_model(self,key):
        if key=='crop_ids':
            return 'farmer.crop'
        if key=='land_ids':
            return 'farmer.land'
        if key=='fish_ids':
            return 'farmer.fish'
        if key=='animal_ids':
            return 'farmer.animal'
        if key=='loan_ids':
            return 'farmer.loan'
        if key=='associated_ids':
            return 'associated.institute'
        if key=='document_ids':
            return 'farmer.documents'
        if key=='family_ids':
            return 'farmer.family'
        if key=='local_production_ids':
            return 'local.production'
        if key=='farmer_group_membership_ids':
            return 'farmer.group.member'

    @api.model
    def write(self, *args, **kwargs):
        if len(args)>1:
            farmer = self.env['farm.farmer'].search([('id','in',args[0])])[0]
        else:
            farmer = self
        values = args[-1]
        '''
        execute normal write in two cases
        1. if the logged in user has group_user_access.
        2. if the only value to change is of field requesting.
        '''

        if self.env.user.user_has_groups('farmer.group_user_access') or (len(values)==1 and "requesting" in values.keys()):
            super(Farmer, farmer).write(values)
            return
        requesting_values = {
            'crop_ids':values.pop("crop_ids") if "crop_ids" in values  else None,
            'land_ids':values.pop("land_ids") if "land_ids" in values  else None,
            'fish_ids':values.pop("fish_ids") if "fish_ids" in values  else None,
            'animal_ids':values.pop("animal_ids") if "animal_ids" in values  else None,
            'loan_ids':values.pop("loan_ids") if "loan_ids" in values  else None,
            'associated_ids':values.pop("associated_ids") if "associated_ids" in values  else None,
            'document_ids':values.pop("document_ids") if "document_ids" in values  else None,
            'family_ids':values.pop("family_ids") if "family_ids" in values  else None,
            'local_production_ids':values.pop("local_production_ids") if "local_production_ids" in values  else None,
            'insurance_ids':values.pop("insurance_ids") if "insurance_ids" in values  else None,
            'farmer_group_membership_ids':values.pop("farmer_group_membership_ids") if "farmer_group_membership_ids" in values  else None,
            'farmer_id':farmer.id
        }
        print('values: ',values)
        print('requesting values: ',requesting_values)

        model_obj = {}

        for key,value in requesting_values.items():
            if value is not None:
                model_name=self.return_associated_model(key)

                if model_name:
                    model_orm=self.env[model_name]
                    if type(value)==list:

                        for [_,crop_id,req_value] in value:
                            if req_value:
                                if type(crop_id) == str:
                                    continue
                                curr_model = model_orm.search([['id','=',crop_id]])
                                curr_model.xchg = curr_model.copy()
                                curr_model.farmer_id=None

                                model_obj[key] = curr_model

        super(Farmer, farmer).write(values)
        '''
        farmer.requesting is True when a one2many data is deleted
        in which case a profile.update.request is already created 
        so for this case the most recently created profile.update.request 
        for this farmer.id is referenced.
        '''
        if farmer.requesting:
            res = self.env['profile.update.request'].search([('farmer_id','=',farmer.id)],order = 'ref desc',limit = 1)[0]
            res.write(requesting_values)
            farmer.requesting = False
        elif sum([0 if requesting_values[i]==None else 1 for i in requesting_values])>1:
            res = self.env['profile.update.request'].create(requesting_values)
            farmer.requesting = False

        for [field_name,record] in model_obj.items():
            res[field_name] += record

    @api.constrains('requesting')
    def _send_request(self):
        if not self.requesting:
            return
        requesting_values = {
            'crop_ids':self["crop_ids"],
            'land_ids':self["land_ids"],
            'fish_ids':self["fish_ids"],
            'animal_ids':self["animal_ids"],
            'loan_ids':self["loan_ids"],
            'associated_ids':self["associated_ids"],
            'document_ids':self["document_ids"],
            'family_ids':self["family_ids"],
            'local_production_ids':self["local_production_ids"],
            'insurance_ids':self["insurance_ids"],
            'farmer_group_membership_ids':self["farmer_group_membership_ids"],
            'farmer_id':self.id
        }
        if sum([0 if requesting_values[i]==None else 1 for i in requesting_values])>1:
            res = self.env['profile.update.request'].create(requesting_values)

    @api.onchange('province')
    def _clear_province_name(self):
        self.district=None
        self.palika=None

    @api.onchange('district')
    def _clear_district_name(self):
        self.palika=None

class FarmerGroupPOC(models.Model):
    _name = 'farmer.group.poc'
    _inherits = {'res.users': 'user_id'}

    ref = fields.Char(readonly=1, default=lambda self: _('New'), string=_('Farmer Group ID'), )
    user_id = fields.Many2one('res.users',store=True, required=True, ondelete='cascade', auto_join=True, index=True, string=_('Related User'), help=' Data of the user',)

    @api.model
    def create(self, vals):
        group_id = self.env.context.get('active_id', '0')
        group_obj = self.env['farmer.group'].search([('id', '=', group_id)])
        vals['login'] = 'djdmd'
        vals['parent_id'] = group_obj.user_id.id
        poc = super(FarmerGroupPOC, self).create(vals)
        group_obj.write({'poc_id': poc.id})
        return poc


class FarmerGroupMember(models.Model):
    _name = 'farmer.group.member'
    
    farmer_group_id = fields.Many2one('farmer.group')
    farmer_id = fields.Many2one('farm.farmer')
    profile_update_id = fields.Many2one('profile.update.request', string=_("Profile Update Request"))

    xchg = fields.Many2one('farmer.group.member',string=_('Fields For Exchanging'))
    position = fields.Selection([
        ('Member','Member'),
        ('Chairman/Coordinator','Chairman/Coordinator'),
        ('Secretary','Secretary'),
        ('Treasurer','Treasurer'),
    ])
        
    delete_request=fields.Boolean(default=False)
    
    # @api.constrains('farmer_id','farmer_group_id','position')
    # def membership_constraint(self):
    #     for record in self:
    #         other_records = self.env['farmer.group.member'].search([])
    #         for other_record in other_records:
                # if (other_record.id != record.id and other_record.farmer_group_id.id == record.farmer_group_id.id and other_record.farmer_id.id == record.farmer_id.id  ):
                #     raise ValidationError(_("Duplicate Member in this group."))
                # if (other_record.id != record.id and other_record.farmer_group_id.id == record.farmer_group_id.id and other_record.position == record.position and record.position != 'Member' ):
                #     raise ValidationError(_(record.position+" is already filled for this group."))

    @api.model
    def write(self, *args, **kwargs):
        vals=args[-1]
        '''
        normal write for following condition:
        1. if group_user_access
        2. delete_request is not updated 
        '''
        if self.env.user.user_has_groups('farmer.group_user_access') or 'delete_request' not in  vals.keys():
            return super().write(vals)
        if self.farmer_id.id and not self.farmer_id.requesting:
            self.farmer_id.requesting = True
        if self.farmer_group_id.id and not self.farmer_group_id.requesting:
            self.farmer_group_id.requesting = True
        return super().write(vals)

    def delete(self):
        self.delete_request = True
                
        if self.env.user.user_has_groups('farmer.group_user_access'):
            self.unlink()   
            return {
                'type': 'ir.actions.client',
                'tag': 'reload',
            }

    def undo_delete(self):
        self.delete_request = False   
    

class FarmerGroup(models.Model):
    _name = 'farmer.group'
    _description = 'Farmer Group'
    _inherits = {'farm.producer': 'producer_id'}

    ref = fields.Char(readonly=1, default=lambda self: _('New'), string=_('Farmer Group ID'), )
    producer_id = fields.Many2one('farm.producer',store=True, required=True, ondelete='restrict', auto_join=True, index=True, string=_('Related Partner'), help='Partner-related data of the user',)
    agriculture_activites = fields.Many2many('farmer.agriculture.activities', string=_('Agriculture Activity'))
    
    registration_number = fields.Char(string=_('Registration Number'))
    registration_date = fields.Date(string=_('Registration Date'),compute="_obtain_registration_date_ad")
    registration_date_bs = fields.Char(string=_('Registration Date(B.S.)'),required=False)
    pan_number = fields.Char(string=_('Pan Number'))
    #location fields Many2one
    province = fields.Many2one('location.province',string=_('Province'))
    district = fields.Many2one('location.district',string=_('District'))
    palika = fields.Many2one('location.palika',string=_('Palika'))
    ward_no = fields.Integer(string=_('Ward No'),required=False)
    tole = fields.Many2one('location.tole',string=_('Tole'))
    
    
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

    # one2many pages fields
    crop_ids = fields.One2many('farmer.crop', 'farmer_group_id', string=_('Crops'))
    land_ids = fields.One2many('farmer.land', 'farmer_group_id', string=_('Lands'))
    fish_ids = fields.One2many('farmer.fish', 'farmer_group_id', string=_('Fish'))
    animal_ids = fields.One2many('farmer.animal', 'farmer_group_id', string=_('Animal'))
    loan_ids = fields.One2many('farmer.loan', 'farmer_group_id', string=_('Loan'))
    associated_ids = fields.One2many('associated.institute', 'farmer_group_id', string=_('Associated Instutite'))
    document_ids = fields.One2many('farmer.documents', 'farmer_group_id', string=_('Farmer Documents'))
    service_lists = fields.Many2many('services.lists', string=_('Service Lists'))
    local_production_ids = fields.One2many("local.production","farmer_group_id",string="Local Productions")
    farmer_group_membership_ids = fields.One2many("farmer.group.member","farmer_group_id",string="Members")
    insurance_ids = fields.One2many("produce.insurance","farmer_group_id",string="Produce Insurance")

    poc_id = fields.Many2one('farmer.group.poc', string='POC')
    poc_name = fields.Char(related='poc_id.name', string='POC Name', store=False)
    poc_mobile = fields.Char(related='poc_id.mobile', string='POC Mobile', store=False)
    poc_email = fields.Char(related='poc_id.email', string='POC Email', store=False)

    latitude = fields.Char(string=_('Latitude'))
    longitude = fields.Char(string=_('Longitude'))

    chairman = fields.Many2one('farm.farmer', string=_('Chairman/Coordinator'),compute='populate_positions')
    secretary = fields.Many2one('farm.farmer', string=_('Secretary'),compute='populate_positions')
    treasurer = fields.Many2one('farm.farmer', string=_('Treasurer'),compute='populate_positions')
    
    profile_update_request_ids = fields.One2many("profile.update.request","farmer_group_id", string="Profile Update Requests")
    requesting = fields.Boolean("Requesting Profile Update",default = False)

    def return_associated_model(self,key):
        if key=='crop_ids':
            return 'farmer.crop'
        if key=='land_ids':
            return 'farmer.land'
        if key=='fish_ids':
            return 'farmer.fish'
        if key=='animal_ids':
            return 'farmer.animal'
        if key=='loan_ids':
            return 'farmer.loan'
        if key=='associated_ids':
            return 'associated.institute'
        if key=='document_ids':
            return 'farmer.documents'
        if key=='family_ids':
            return 'farmer.family'
        if key=='local_production_ids':
            return 'local.production'
        if key=='farmer_group_membership_ids':
            return 'farmer.group.member'

    @api.model
    def write(self, *args, **kwargs):
        if len(args)>1:
            farmer_group = self.env['farmer.group'].search([('id','in',args[0])])[0]
        else:
            farmer_group = self
        values = args[-1]
        '''
        execute normal write in two cases
        1. if the logged in user has group_user_access.
        2. if the only value to change is of field requesting.
        '''

        if self.env.user.user_has_groups('farmer.group_user_access') or (len(values)==1 and "requesting" in values.keys()):
            super(FarmerGroup, farmer_group).write(values)
            return
        requesting_values = {
            'crop_ids':values.pop("crop_ids") if "crop_ids" in values  else None,
            'land_ids':values.pop("land_ids") if "land_ids" in values  else None,
            'fish_ids':values.pop("fish_ids") if "fish_ids" in values  else None,
            'animal_ids':values.pop("animal_ids") if "animal_ids" in values  else None,
            'loan_ids':values.pop("loan_ids") if "loan_ids" in values  else None,
            'associated_ids':values.pop("associated_ids") if "associated_ids" in values  else None,
            'document_ids':values.pop("document_ids") if "document_ids" in values  else None,
            'local_production_ids':values.pop("local_production_ids") if "local_production_ids" in values  else None,
            'insurance_ids':values.pop("insurance_ids") if "insurance_ids" in values  else None,
            'farmer_group_membership_ids':values.pop("farmer_group_membership_ids") if "farmer_group_membership_ids" in values  else None,
            'farmer_group_id':farmer_group.id
        }

        model_obj = {}

        for key,value in requesting_values.items():
            if value is not None:
                model_name=self.return_associated_model(key)

                if model_name:
                    model_orm=self.env[model_name]
                    if type(value)==list:

                        for [_,ref_id,req_value] in value:
                            if req_value:
                                if type(ref_id) == str:
                                    continue
                                curr_model = model_orm.search([['id','=',ref_id]])

                                if curr_model:
                                    curr_model.xchg = curr_model.copy()
                                    curr_model.farmer_group_id=None
                                    model_obj[key] = curr_model
        print(farmer_group)
        super(FarmerGroup, farmer_group).write(values)
        '''
        farmer.requesting is True when a one2many data is deleted
        in which case a profile.update.request is already created 
        so for this case the most recently created profile.update.request 
        for this farmer.id is referenced.
        '''
        if farmer_group.requesting:
            res = self.env['profile.update.request'].search([('farmer_group_id','=',farmer_group.id)],order = 'ref desc',limit = 1)[0]
            res.write(requesting_values)
            farmer_group.requesting = False
        elif sum([0 if requesting_values[i]==None else 1 for i in requesting_values])>1:
            res = self.env['profile.update.request'].create(requesting_values)
            farmer_group.requesting = False

        for [field_name,record] in model_obj.items():
            res[field_name] += record

    @api.constrains('requesting')
    def _send_request(self):
        if not self.requesting:
            return
        requesting_values = {
            'crop_ids':self["crop_ids"],
            'land_ids':self["land_ids"],
            'fish_ids':self["fish_ids"],
            'animal_ids':self["animal_ids"],
            'loan_ids':self["loan_ids"],
            'associated_ids':self["associated_ids"],
            'document_ids':self["document_ids"],
            'local_production_ids':self["local_production_ids"],
            'farmer_group_membership_ids':self["farmer_group_membership_ids"],
            'farmer_group_id':self.id
        }
        if sum([0 if requesting_values[i]==None else 1 for i in requesting_values])>1:
            res = self.env['profile.update.request'].create(requesting_values)

    @api.onchange('farmer_group_membership_ids')
    def populate_positions(self):
        for record in self:
            record.chairman = None
            record.secretary = None
            record.treasurer = None
            for members in record.farmer_group_membership_ids:
                if members.position == 'Chairman/Coordinator':
                    record.chairman = members.farmer_id
                if members.position == 'Secretary':
                    record.secretary = members.farmer_id
                if members.position == 'Treasurer':
                    record.treasurer = members.farmer_id

    @api.model
    def create(self, vals):
        vals['is_company'] = True
        vals['ref'] = self.env['ir.sequence'].next_by_code("farmer.group.sequence")
        return super(FarmerGroup, self).create(vals)

    def action_edit_poc(self):
        # res_id is used to get that particular id object filled in the form.
        # self.id is the alternative to self.env.context.get('active_id', 0)
        group_obj = self.env['farmer.group'].search([('id', '=', self.id)])
        return {
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'farmer.group.poc',
                'target': 'new',
                'res_id': group_obj.poc_id.id,
            }






