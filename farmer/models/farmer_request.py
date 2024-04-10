from odoo import models, fields, _, api
import nepali_datetime
from datetime import date


class RequestMixin(models.AbstractModel):
    _name = 'request.mixin'

    state = fields.Selection([
        ('Pending','Pending'),
        ('Approved','Approved'),
        ('Declined','Declined'),
        ('Canceled','Canceled'),
        ('On Hold','On Hold'),
    ], default='Pending', readonly=True, string="State", tracking=True)
    saved = fields.Boolean()

    template_approved = [
        'farmer.service_request_approved_notification_email_template',
        'farmer.expert_request_approved_notification_email_template',
        'farmer.seedling_request_approved_notification_email_template',
        'farmer.equipment_request_approved_notification_email_template',
        'farmer.fish_larva_request_approved_notification_email_template',
        'farmer.other_request_approved_notification_email_template',
    ]
    template_declined = [
        'farmer.service_request_declined_notification_email_template',
        'farmer.expert_request_declined_notification_email_template',
        'farmer.seedling_request_declined_notification_email_template',
        'farmer.equipment_request_declined_notification_email_template',
        'farmer.fish_larva_request_declined_notification_email_template',
        'farmer.other_request_declined_notification_email_template',
    ]
    template_onhold = [
        'farmer.service_request_onhold_notification_email_template',
        'farmer.expert_request_onhold_notification_email_template',
        'farmer.seedling_request_onhold_notification_email_template',
        'farmer.equipment_request_onhold_notification_email_template',
        'farmer.fish_larva_request_onhold_notification_email_template',
        'farmer.other_request_onhold_notification_email_template',
    ]
    template_for_create = [
        'farmer.service_request_notification_email_template',
        'farmer.expert_request_notification_email_template',
        'farmer.seedling_request_notification_email_template',
        'farmer.equipment_request_notification_email_template',
        'farmer.fish_larva_request_notification_email_template',
        'farmer.other_request_notification_email_template',
    ]

    def action_send_email(self):
        model = self._name
        if model == 'services.request':
            if self.state == 'Approved':
                template_ref = self.template_approved[0]
                template_id = self.env.ref(template_ref)
                if template_id:
                    return template_id.send_mail(self.id, force_send=True)

            elif self.state == 'Declined':
                template_ref = self.template_declined[0]
                template_id = self.env.ref(template_ref)
                if template_id:
                    return template_id.send_mail(self.id, force_send=True)

            elif self.state == 'On Hold':
                template_ref = self.template_onhold[0]
                template_id = self.env.ref(template_ref)
                if template_id:
                    return template_id.send_mail(self.id, force_send=True)

            else:
                template_ref = self.template_for_create[0]
                template_id = self.env.ref(template_ref)
                if template_id:
                    return template_id.send_mail(self.id, force_send=True)

        elif model == 'expert.request':
            if self.state == 'Approved':
                template_ref = self.template_approved[1]
                template_id = self.env.ref(template_ref)
                if template_id:
                    return template_id.send_mail(self.id, force_send=True)

            elif self.state == 'Declined':
                template_ref = self.template_declined[1]
                template_id = self.env.ref(template_ref)
                if template_id:
                    return template_id.send_mail(self.id, force_send=True)

            elif self.state == 'On Hold':
                template_ref = self.template_onhold[1]
                template_id = self.env.ref(template_ref)
                if template_id:
                    return template_id.send_mail(self.id, force_send=True)

            else:
                template_ref = self.template_for_create[1]
                template_id = self.env.ref(template_ref)
                if template_id:
                    return template_id.send_mail(self.id, force_send=True)

        elif model == 'seedling.request':
            if self.state == 'Approved':
                template_ref = self.template_approved[2]
                template_id = self.env.ref(template_ref)
                if template_id:
                    return template_id.send_mail(self.id, force_send=True)

            elif self.state == 'Declined':
                template_ref = self.template_declined[2]
                template_id = self.env.ref(template_ref)
                if template_id:
                    return template_id.send_mail(self.id, force_send=True)

            elif self.state == 'On Hold':
                template_ref = self.template_onhold[2]
                template_id = self.env.ref(template_ref)
                if template_id:
                    return template_id.send_mail(self.id, force_send=True)

            else:
                template_ref = self.template_for_create[2]
                template_id = self.env.ref(template_ref)
                if template_id:
                    return template_id.send_mail(self.id, force_send=True)

        elif model == 'equipment.request':
            if self.state == 'Approved':
                template_ref = self.template_approved[3]
                template_id = self.env.ref(template_ref)
                if template_id:
                    return template_id.send_mail(self.id, force_send=True)

            elif self.state == 'Declined':
                template_ref = self.template_declined[3]
                template_id = self.env.ref(template_ref)
                if template_id:
                    return template_id.send_mail(self.id, force_send=True)

            elif self.state == 'On Hold':
                template_ref = self.template_onhold[3]
                template_id = self.env.ref(template_ref)
                if template_id:
                    return template_id.send_mail(self.id, force_send=True)

            else:
                template_ref = self.template_for_create[3]
                template_id = self.env.ref(template_ref)
                if template_id:
                    return template_id.send_mail(self.id, force_send=True)

        elif model == 'fish.larva.request':
            if self.state == 'Approved':
                template_ref = self.template_approved[4]
                template_id = self.env.ref(template_ref)
                if template_id:
                    return template_id.send_mail(self.id, force_send=True)

            elif self.state == 'Declined':
                template_ref = self.template_declined[4]
                template_id = self.env.ref(template_ref)
                if template_id:
                    return template_id.send_mail(self.id, force_send=True)

            elif self.state == 'On Hold':
                template_ref = self.template_onhold[4]
                template_id = self.env.ref(template_ref)
                if template_id:
                    return template_id.send_mail(self.id, force_send=True)

            else:
                template_ref = self.template_for_create[4]
                template_id = self.env.ref(template_ref)
                if template_id:
                    return template_id.send_mail(self.id, force_send=True)

        elif model == 'other.request':
            if self.state == 'Approved':
                template_ref = self.template_approved[5]
                template_id = self.env.ref(template_ref)
                if template_id:
                    return template_id.send_mail(self.id, force_send=True)

            elif self.state == 'Declined':
                template_ref = self.template_declined[5]
                template_id = self.env.ref(template_ref)
                if template_id:
                    return template_id.send_mail(self.id, force_send=True)

            elif self.state == 'On Hold':
                template_ref = self.template_onhold[5]
                template_id = self.env.ref(template_ref)
                if template_id:
                    return template_id.send_mail(self.id, force_send=True)

            else:
                template_ref = self.template_for_create[5]
                template_id = self.env.ref(template_ref)
                if template_id:
                    return template_id.send_mail(self.id, force_send=True)

    def approve_request(self):
        self.state = 'Approved'
        self.action_send_email()

    def decline_request(self):
        self.state = 'Declined'
        self.action_send_email()

    def hold_request(self):
        self.state = 'On Hold'
        self.action_send_email()

    def cancel_request(self):
        self.state = 'Canceled'


class ServiceRequest(models.Model):
    _name = 'services.request'
    _description = 'Services to request'
    _rec_name = 'ref'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin','request.mixin']
    _order = 'year desc,write_date desc'

    ref = fields.Char(readonly=1, default=lambda self: _('New'), string=_('Service ID'), )
    year = fields.Many2one('programs.year',string=_("Year"),tracking=True)
    program = fields.Many2one('year.program',string=_("Program"))
    project = fields.Many2one('program.project',string=_("Project"))
    service_name = fields.Many2one('services.lists',string=_("Service Name"),required=True)

    def _get_logged_in_producer(self):
        if self.env.user.user_has_groups('farmer.group_user_access'):
            return None
        return self.env["farm.producer"].search([('user_id','=',self.env.user.id)])[0].id

    service_recipient = fields.Many2one('farm.producer',string=_("Service Recipient"),required=True,default=_get_logged_in_producer)
    saved = fields.Boolean(default=False)


    #only show when service recipient is selected
    service_recipient_set = fields.Boolean(store=False,compute="_compute_service_recipient_details")
    service_recipient_name = fields.Char(_("Name"),store=False,compute="_compute_service_recipient_details")
    service_recipient_phone = fields.Char(_("Phone"),store=False,compute="_compute_service_recipient_details")
    service_recipient_mobile = fields.Char(_("Mobile"),store=False,compute="_compute_service_recipient_details")
    service_recipient_vat = fields.Char(_("Tax ID"),store=False,compute="_compute_service_recipient_details")
    service_recipient_farmer_group = fields.Char(_("Farmer Type"),store=True,compute="_compute_service_recipient_details")
    service_recipient_gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], _("Gender"),compute="_compute_service_recipient_details",store=True)
    # service_recipient_gender = fields.Selection('farm.farmer', store=False,compute="_compute_service_recipient_details")
    previous_service_request_inverse = fields.Many2one('services.request')
    previous_service_requests = fields.One2many('services.request','previous_service_request_inverse',compute='_compute_previous_service_requests')
    service_request_dynamic_state = fields.Selection([
        ('false', 'Select State'),
        ('Pending','Pending'),
        ('Approved','Approved'),
        ('Declined','Declined'),
        ('On Hold','On Hold'),
        ('Canceled','Canceled'),
    ],default='false', string="Service Request State",store=False)

    @api.depends('service_request_dynamic_state')
    def _compute_previous_service_requests(self):
        for record in self:
            domain = ['&',
                    ('service_recipient','=',record.service_recipient.id),
                    ('service_name','=',record.service_name.id),
                    ('id','!=',record._origin.id)]
            if self.service_request_dynamic_state != 'false':
                domain += [('state', '=', self.service_request_dynamic_state)]
            temp=[req['id'] for req in self.env['services.request'].search_read(domain,['id'])]
            if temp:
                record.previous_service_requests = temp
            else:
                record.previous_service_requests = None


    @api.onchange('service_recipient')
    def _compute_service_recipient_details(self):
        for record in self:
            if record.service_recipient:
                record.service_recipient_set = True
            record.service_recipient_name = record.service_recipient.name
            record.service_recipient_phone = record.service_recipient.phone
            record.service_recipient_mobile = record.service_recipient.mobile
            record.service_recipient_vat = record.service_recipient.vat
            record.service_recipient_gender = record.service_recipient.gender
            farmer_id = self.env['farm.farmer'].search([('producer_id','=',record.service_recipient.id)])
            if len(farmer_id)>0:
                record.service_recipient_farmer_group = farmer_id[0].farmer_group.type
            else:
                record.service_recipient_farmer_group = None

    @api.model
    def create(self, vals):
        vals['ref'] = self.env['ir.sequence'].next_by_code("farmer.service.request.sequence")
        vals['saved'] = True
        record = super(ServiceRequest, self).create(vals)
        record.action_send_email()
        return record

    @api.onchange('year')
    def _clear_program_project(self):
        self.program=None
        self.project=None

    @api.onchange('program')
    def _clear_project(self):
        self.project=None

    update_date_bs = fields.Char("Updated Date", compute = "_obtain_creation_date_nepali")

    @api.depends('write_date')
    def _obtain_creation_date_nepali(self):
        for record in self:
            record.update_date_bs = nepali_datetime.date.from_datetime_date(record.write_date.date())

class ExpertRequest(models.Model):
    _name = 'expert.request'
    _description = 'Expert Request'
    _rec_name = 'ref'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin', 'request.mixin']
    ref = fields.Char(readonly=1, default=lambda self: _('New'), string=_('Service ID'),)
    year = fields.Many2one('programs.year',string=_("Year"),tracking=True)
    program = fields.Many2one('year.program',string=_("Program"))
    project = fields.Many2one('program.project',string=_("Project"))
    expert_id = fields.Many2one('expert.type', string=_("Type"))
    expert_quantity = fields.Char(string=_('Quantity'),tracking=True)

    def _get_logged_in_producer(self):
        if self.env.user.user_has_groups('farmer.group_user_access'):
            return None
        return self.env["farm.producer"].search([('user_id','=',self.env.user.id)])[0].id

    expert_recipient = fields.Many2one('farm.producer',string=_("Expert Recipient"),required=True,default=_get_logged_in_producer)

    #only show when serive recipient is selected
    expert_recipient_set = fields.Boolean(store=False,compute="_compute_expert_recipient_details")
    expert_recipient_name = fields.Char(_("Name"),store=False,compute="_compute_expert_recipient_details")
    expert_recipient_phone = fields.Char(_("Phone"),store=False,compute="_compute_expert_recipient_details")
    expert_recipient_mobile = fields.Char(_("Mobile"),store=False,compute="_compute_expert_recipient_details")
    expert_recipient_vat = fields.Char(_("Tax ID"),store=False,compute="_compute_expert_recipient_details")
    expert_recipient_farmer_group = fields.Char(_("Farmer Type"),store=True,compute="_compute_expert_recipient_details")
    expert_recipient_gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], _("Gender"),store=True,compute="_compute_expert_recipient_details")

    @api.onchange('expert_recipient')
    def _compute_expert_recipient_details(self):
        for record in self:
            if record.expert_recipient:
                record.expert_recipient_set = True
            record.expert_recipient_name = record.expert_recipient.name
            record.expert_recipient_phone = record.expert_recipient.phone
            record.expert_recipient_mobile = record.expert_recipient.mobile
            record.expert_recipient_vat = record.expert_recipient.vat
            record.expert_recipient_gender = record.expert_recipient.gender
            farmer_id = self.env['farm.farmer'].search([('producer_id','=',record.expert_recipient.id)])
            if len(farmer_id)>0:
                record.expert_recipient_farmer_group = farmer_id[0].farmer_group.type
            else:
                record.expert_recipient_farmer_group = None

    previous_expert_request_inverse = fields.Many2one('expert.request')
    previous_expert_requests = fields.One2many('expert.request','previous_expert_request_inverse',compute='_compute_previous_expert_requests')
    expert_request_dynamic_state = fields.Selection([
        ('false', 'Select State'),
        ('Pending','Pending'),
        ('Approved','Approved'),
        ('Declined','Declined'),
        ('On Hold','On Hold'),
        ('Canceled','Canceled'),
    ],default='false', string="Expert Request State",store=False)

    @api.depends('expert_request_dynamic_state')
    def _compute_previous_expert_requests(self):
        for record in self:
            domain = ['&',
                    ('expert_recipient','=',record.expert_recipient.id),
                    ('expert_id','=',record.expert_id.id),
                    ('id','!=',record._origin.id)]
            if self.expert_request_dynamic_state != 'false':
                domain += [('state', '=', self.expert_request_dynamic_state)]
            temp=[req['id'] for req in self.env['expert.request'].search_read(domain,['id'])]
            if temp:
                record.previous_expert_requests = temp
            else:
                record.previous_expert_requests = None

    @api.model
    def create(self, vals):
        vals['ref'] = self.env['ir.sequence'].next_by_code("farmer.expert.request.sequence")
        vals['saved'] = True
        record = super(ExpertRequest, self).create(vals)
        record.action_send_email()
        return record

    @api.onchange('year')
    def _clear_program_project(self):
        self.program=None
        self.project=None

    @api.onchange('program')
    def _clear_project(self):
        self.project=None

    update_date_bs = fields.Char("Updated Date", compute = "_obtain_creation_date_nepali")

    @api.depends('write_date')
    def _obtain_creation_date_nepali(self):
        for record in self:
            record.update_date_bs = nepali_datetime.date.from_datetime_date(record.write_date.date())


class SeedlingRequest(models.Model):
    _name = 'seedling.request'
    _description = 'Seedling Request'
    _rec_name = 'ref'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin','request.mixin']


    ref = fields.Char(readonly=1, default=lambda self: _('New'), string=_('Service ID'), )
    year = fields.Many2one('programs.year',string=_("Year"),tracking=True)
    program = fields.Many2one('year.program',string=_("Program"))
    project = fields.Many2one('program.project',string=_("Project"))
    seedling_quantity = fields.Char(string=_('Quantity'),required=True)
    unit = fields.Selection([
        ('kg', 'KG'),
        ('unit', 'Unit')
    ], string=_('Unit'),required=True)
    # to reflect
    seedling_list = fields.Many2many('seedling.lists.model', string=_('Type'),required=True )

    def _get_logged_in_producer(self):
        if self.env.user.user_has_groups('farmer.group_user_access'):
            return None
        return self.env["farm.producer"].search([('user_id','=',self.env.user.id)])[0].id

    seedling_recipient = fields.Many2one('farm.producer',string=_("Seedling Recipient"),required=True,default=_get_logged_in_producer)
    saved = fields.Boolean(default=False)

    #only show when serive recipient is selected
    seedling_recipient_set = fields.Boolean(store=False,compute="_compute_seedling_recipient_details")
    seedling_recipient_name = fields.Char(_("Name"),store=False,compute="_compute_seedling_recipient_details")
    seedling_recipient_phone = fields.Char(_("Phone"),store=False,compute="_compute_seedling_recipient_details")
    seedling_recipient_mobile = fields.Char(_("Mobile"),store=False,compute="_compute_seedling_recipient_details")
    seedling_recipient_vat = fields.Char(_("Tax ID"),store=False,compute="_compute_seedling_recipient_details")
    seedling_recipient_farmer_group = fields.Char(_("Farmer Type"),store=True,compute="_compute_seedling_recipient_details")
    seedling_recipient_gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], _("Gender"),store=True,compute="_compute_seedling_recipient_details")


    @api.onchange('seedling_recipient')
    def _compute_seedling_recipient_details(self):
        for record in self:
            if record.seedling_recipient:
                record.seedling_recipient_set = True
            record.seedling_recipient_name = record.seedling_recipient.name
            record.seedling_recipient_phone = record.seedling_recipient.phone
            record.seedling_recipient_mobile = record.seedling_recipient.mobile
            record.seedling_recipient_vat = record.seedling_recipient.vat
            record.seedling_recipient_gender = record.seedling_recipient.gender
            farmer_id = self.env['farm.farmer'].search([('producer_id','=',record.seedling_recipient.id)])
            if len(farmer_id)>0:
                record.seedling_recipient_farmer_group = farmer_id[0].farmer_group.type
            else:
                record.seedling_recipient_farmer_group = None

    previous_seedling_request_inverse = fields.Many2one('seedling.request')
    previous_seedling_requests = fields.One2many('seedling.request','previous_seedling_request_inverse',compute='_compute_previous_seedling_requests')
    seedling_request_dynamic_state = fields.Selection([
        ('false', 'Select State'),
        ('Pending','Pending'),
        ('Approved','Approved'),
        ('Declined','Declined'),
        ('On Hold','On Hold'),
        ('Canceled','Canceled'),
    ],default='false', string="seedling Request State",store=False)

    @api.depends('seedling_request_dynamic_state')
    def _compute_previous_seedling_requests(self):
        for record in self:
            domain = ['&',
                    ('seedling_recipient','=',record.seedling_recipient.id),
                    ('seedling_list','in',[rec.id for rec in record.seedling_list]),
                    ('id','!=',record._origin.id)]
            if self.seedling_request_dynamic_state != 'false':
                domain += [('state', '=', self.seedling_request_dynamic_state)]
            temp=[req['id'] for req in self.env['seedling.request'].search_read(domain,['id'])]
            if temp:
                record.previous_seedling_requests = temp
            else:
                record.previous_seedling_requests = None


    @api.model
    def create(self, vals):
        vals['ref'] = self.env['ir.sequence'].next_by_code("farmer.seedling.request.sequence")
        vals['saved'] = True
        record = super(SeedlingRequest, self).create(vals)
        record.action_send_email()
        return record


    @api.onchange('year')
    def _clear_program_project(self):
        self.program=None
        self.project=None

    @api.onchange('program')
    def _clear_project(self):
        self.project=None

    update_date_bs = fields.Char("Updated Date", compute = "_obtain_creation_date_nepali")

    @api.depends('write_date')
    def _obtain_creation_date_nepali(self):
        for record in self:
            record.update_date_bs = nepali_datetime.date.from_datetime_date(record.write_date.date())



class EquipmentRequest(models.Model):
    _name = 'equipment.request'
    _description = 'Equipment Request'
    _rec_name = 'ref'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin','request.mixin']

    ref = fields.Char(readonly=1, default=lambda self: _('New'), string=_('Service ID'), )
    year = fields.Many2one('programs.year',string=_("Year"),tracking=True)
    program = fields.Many2one('year.program',string=_("Program"))
    project = fields.Many2one('program.project',string=_("Project"))
    equipment_type = fields.Many2one('equipment.lists.model',  string=_('Equipment Type'), required = True)
    equipment_quantity = fields.Char(string=_('Quantity'), required = True)
    unit = fields.Selection([
        ('unit', 'Unit')
    ], string=_('Unit'),required=True)

    def _get_logged_in_producer(self):
        if self.env.user.user_has_groups('farmer.group_user_access'):
            return None

        producer = self.env["farm.producer"].search([('user_id', '=', self.env.user.id)], limit=1)

        if producer:
            return producer[0].id
        else:
            # Handle the case where no producer record is found for the current user.
            return None

    equipment_recipient = fields.Many2one('farm.producer', string=_("Equipment Recipient"), required = True,default=_get_logged_in_producer)
    saved = fields.Boolean(default=False)

    #only show when serive recipient is selected
    equipment_recipient_set = fields.Boolean(store=False,compute="_compute_equipment_recipient_details")
    equipment_recipient_name = fields.Char(_("Name"),store=False,compute="_compute_equipment_recipient_details")
    equipment_recipient_phone = fields.Char(_("Phone"),store=False,compute="_compute_equipment_recipient_details")
    equipment_recipient_mobile = fields.Char(_("Mobile"),store=False,compute="_compute_equipment_recipient_details")
    equipment_recipient_vat = fields.Char(_("Tax ID"),store=False,compute="_compute_equipment_recipient_details")
    equipment_recipient_farmer_group = fields.Char(_("Farmer Type"),store=True,compute="_compute_equipment_recipient_details")
    equipment_recipient_gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], _("Gender"),store=True,compute="_compute_equipment_recipient_details")

    @api.onchange('equipment_recipient')
    def _compute_equipment_recipient_details(self):
        for record in self:
            if record.equipment_recipient:
                record.equipment_recipient_set = True
            record.equipment_recipient_name = record.equipment_recipient.name
            record.equipment_recipient_phone = record.equipment_recipient.phone
            record.equipment_recipient_mobile = record.equipment_recipient.mobile
            record.equipment_recipient_vat = record.equipment_recipient.vat
            record.equipment_recipient_gender = record.equipment_recipient.gender
            farmer_id = self.env['farm.farmer'].search([('producer_id','=',record.equipment_recipient.id)])
            if len(farmer_id)>0:
                record.equipment_recipient_farmer_group = farmer_id[0].farmer_group.type
            else:
                record.equipment_recipient_farmer_group = None

    previous_equipment_request_inverse = fields.Many2one('equipment.request')
    previous_equipment_requests = fields.One2many('equipment.request','previous_equipment_request_inverse',compute='_compute_previous_equipment_requests')
    equipment_request_dynamic_state = fields.Selection([
        ('false', 'Select State'),
        ('Pending','Pending'),
        ('Approved','Approved'),
        ('Declined','Declined'),
        ('On Hold','On Hold'),
        ('Canceled','Canceled'),
    ],default='false', string="equipment Request State",store=False)

    @api.depends('equipment_request_dynamic_state')
    def _compute_previous_equipment_requests(self):
        for record in self:
            domain = ['&',
                    ('equipment_recipient','=',record.equipment_recipient.id),
                    ('equipment_type','=',record.equipment_type.id),
                    ('id','!=',record._origin.id)]
            if self.equipment_request_dynamic_state != 'false':
                domain += [('state', '=', self.equipment_request_dynamic_state)]
            temp=[req['id'] for req in self.env['equipment.request'].search_read(domain,['id'])]
            if temp:
                record.previous_equipment_requests = temp
            else:
                record.previous_equipment_requests = None

    @api.model
    def create(self, vals):
        vals['ref'] = self.env['ir.sequence'].next_by_code("farmer.equipment.request.sequence")
        vals['saved'] = True
        record = super(EquipmentRequest, self).create(vals)
        record.action_send_email()
        return record

    @api.onchange('year')
    def _clear_program_project(self):
        self.program=None
        self.project=None

    @api.onchange('program')
    def _clear_project(self):
        self.project=None

    update_date_bs = fields.Char("Updated Date", compute = "_obtain_creation_date_nepali")

    @api.depends('write_date')
    def _obtain_creation_date_nepali(self):
        for record in self:
            record.update_date_bs = nepali_datetime.date.from_datetime_date(record.write_date.date())



class FishLarvaRequest(models.Model):
    _name = 'fish.larva.request'
    _description = 'Fish Larva Request'
    _rec_name = 'ref'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin','request.mixin']


    ref = fields.Char(readonly=1, default=lambda self: _('New'), string=_('Service ID'),)
    year = fields.Many2one('programs.year',string=_("Year"), tracking=True)
    program = fields.Many2one('year.program',string=_("Program"))
    project = fields.Many2one('program.project',string=_("Project"))
    # to reflect
    fish_larva_list = fields.Many2many('fish_larva.lists.model', string=_('Type'),required=True )
    fish_larva_quantity = fields.Char(string=_('Quantity'))
    unit = fields.Selection([
        ('kg', 'KG'),
        ('unit', 'Unit')
    ], string=_('Unit'),required=True)


    # larva_recipient_gender = fields.Selection([
    #     ('male', 'Male'),
    #     ('female', 'Female'),
    #     ('other', 'Other')
    # ], string=_('Recepient Gender'),required=True)


    
    def _get_logged_in_producer(self):
        if self.env.user.user_has_groups('farmer.group_user_access'):
            return None
        return self.env["farm.producer"].search([('user_id','=',self.env.user.id)])[0].id

    fish_larva_recipient = fields.Many2one('farm.producer',string=_("Fish Larva Recipient"),required=True,default=_get_logged_in_producer)
    saved = fields.Boolean(default=False)

    #only show when fish larva recipient is selected
    fish_larva_recipient_set = fields.Boolean(store=False,compute="_compute_fish_larva_recipient_details")
    fish_larva_recipient_name = fields.Char(_("Name"),store=False,compute="_compute_fish_larva_recipient_details")
    fish_larva_recipient_phone = fields.Char(_("Phone"),store=False,compute="_compute_fish_larva_recipient_details")
    fish_larva_recipient_mobile = fields.Char(_("Mobile"),store=False,compute="_compute_fish_larva_recipient_details")
    fish_larva_recipient_vat = fields.Char(_("Tax ID"),store=False,compute="_compute_fish_larva_recipient_details")
    fish_larva_recipient_farmer_group = fields.Char(_("Farmer Type"),store=True,compute="_compute_fish_larva_recipient_details")
    fish_larva_recipient_gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], _("Recipient Gender"),store=True,compute="_compute_fish_larva_recipient_details")


    @api.onchange('fish_larva_recipient')
    def _compute_fish_larva_recipient_details(self):
        for record in self:
            if record.fish_larva_recipient:
                record.fish_larva_recipient_set = True
            record.fish_larva_recipient_name = record.fish_larva_recipient.name
            record.fish_larva_recipient_phone = record.fish_larva_recipient.phone
            record.fish_larva_recipient_mobile = record.fish_larva_recipient.mobile
            record.fish_larva_recipient_vat = record.fish_larva_recipient.vat
            record.fish_larva_recipient_gender = record.fish_larva_recipient.gender
            farmer_id = self.env['farm.farmer'].search([('producer_id','=',record.fish_larva_recipient.id)])
            if len(farmer_id)>0:
                record.fish_larva_recipient_farmer_group = farmer_id[0].farmer_group.type
            else:
                record.fish_larva_recipient_farmer_group = None

    previous_fish_larva_request_inverse = fields.Many2one('fish.larva.request')
    previous_fish_larva_requests = fields.One2many('fish.larva.request','previous_fish_larva_request_inverse',compute='_compute_previous_fish_larva_requests')
    fish_larva_request_dynamic_state = fields.Selection([
        ('false', 'Select State'),
        ('Pending','Pending'),
        ('Approved','Approved'),
        ('Declined','Declined'),
        ('On Hold','On Hold'),
        ('Canceled','Canceled'),
    ],default='false', string="fish.larva Request State",store=False)

    @api.depends('fish_larva_request_dynamic_state')
    def _compute_previous_fish_larva_requests(self):
        for record in self:
            domain = ['&',
                    ('fish_larva_recipient','=',record.fish_larva_recipient.id),
                    ('fish_larva_list','in',[rec.id for rec in record.fish_larva_list]),
                    ('id','!=',record._origin.id)]
            if self.fish_larva_request_dynamic_state != 'false':
                domain += [('state', '=', self.fish_larva_request_dynamic_state)]
            temp=[req['id'] for req in self.env['fish.larva.request'].search_read(domain,['id'])]
            if temp:
                record.previous_fish_larva_requests = temp
            else:
                record.previous_fish_larva_requests = None

    @api.model
    def create(self, vals):
        vals['ref'] = self.env['ir.sequence'].next_by_code("farmer.fish_larva.request.sequence")
        vals['saved'] = True
        record =  super(FishLarvaRequest, self).create(vals)
        record.action_send_email()
        return record

    @api.onchange('year')
    def _clear_program_project(self):
        self.program=None
        self.project=None

    @api.onchange('program')
    def _clear_project(self):
        self.project=None

    update_date_bs = fields.Char("Updated Date", compute = "_obtain_creation_date_nepali")

    @api.depends('write_date')
    def _obtain_creation_date_nepali(self):
        for record in self:
            record.update_date_bs = nepali_datetime.date.from_datetime_date(record.write_date.date())

class OtherRequest(models.Model):
    _name = 'other.request'
    _description = 'Other Request'
    _rec_name = 'ref'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin','request.mixin']


    ref = fields.Char(readonly=1, default=lambda self: _('New'), string=_('Service ID'),)
    year = fields.Many2one('programs.year',string=_("Year"), tracking=True)
    program = fields.Many2one('year.program',string=_("Program"))
    project = fields.Many2one('program.project',string=_("Project"))
    request_detail = fields.Char( string=_('Request Detail'),required=True )
    
    def _get_logged_in_producer(self):
        if self.env.user.user_has_groups('farmer.group_user_access'):
            return None
        return self.env["farm.producer"].search([('user_id','=',self.env.user.id)])[0].id

    other_recipient = fields.Many2one('farm.producer',string=_("Request Recipient"),required=True,default=_get_logged_in_producer)
    saved = fields.Boolean(default=False)

    #only show when other recipient is selected
    other_recipient_set = fields.Boolean(store=False,compute="_compute_other_recipient_details")
    other_recipient_name = fields.Char(_("Name"),store=False,compute="_compute_other_recipient_details")
    other_recipient_phone = fields.Char(_("Phone"),store=False,compute="_compute_other_recipient_details")
    other_recipient_mobile = fields.Char(_("Mobile"),store=False,compute="_compute_other_recipient_details")
    other_recipient_vat = fields.Char(_("Tax ID"),store=False,compute="_compute_other_recipient_details")
    other_recipient_farmer_group = fields.Char(_("Farmer Type"),store=True,compute="_compute_other_recipient_details")
    other_recipient_gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], _("Recipient Gender"),store=True,compute="_compute_other_recipient_details")


    @api.onchange('other_recipient')
    def _compute_other_recipient_details(self):
        for record in self:
            if record.other_recipient:
                record.other_recipient_set = True
            record.other_recipient_name = record.other_recipient.name
            record.other_recipient_phone = record.other_recipient.phone
            record.other_recipient_mobile = record.other_recipient.mobile
            record.other_recipient_vat = record.other_recipient.vat
            record.other_recipient_gender = record.other_recipient.gender
            farmer_id = self.env['farm.farmer'].search([('producer_id','=',record.other_recipient.id)])
            if len(farmer_id)>0:
                record.other_recipient_farmer_group = farmer_id[0].farmer_group.type
            else:
                record.other_recipient_farmer_group = None

    previous_other_request_inverse = fields.Many2one('other.request')
    previous_other_requests = fields.One2many('other.request','previous_other_request_inverse',compute='_compute_previous_other_requests')
    other_request_dynamic_state = fields.Selection([
        ('false', 'Select State'),
        ('Pending','Pending'),
        ('Approved','Approved'),
        ('Declined','Declined'),
        ('On Hold','On Hold'),
        ('Canceled','Canceled'),
    ],default='false', string="other Request State",store=False)

    @api.depends('other_request_dynamic_state')
    def _compute_previous_other_requests(self):
        for record in self:
            domain = ['&',
                    ('other_recipient','=',record.other_recipient.id),
                    ('id','!=',record._origin.id)]
            if self.other_request_dynamic_state != 'false':
                domain += [('state', '=', self.other_request_dynamic_state)]
            temp=[req['id'] for req in self.env['other.request'].search_read(domain,['id'])]
            if temp:
                record.previous_other_requests = temp
            else:
                record.previous_other_requests = None

    @api.model
    def create(self, vals):
        vals['ref'] = self.env['ir.sequence'].next_by_code("farmer.other.request.sequence")
        vals['saved'] = True
        record =  super(OtherRequest, self).create(vals)
        record.action_send_email()
        return record

    @api.onchange('year')
    def _clear_program_project(self):
        self.program=None
        self.project=None

    @api.onchange('program')
    def _clear_project(self):
        self.project=None

    update_date_bs = fields.Char("Updated Date", compute = "_obtain_creation_date_nepali")

    @api.depends('write_date')
    def _obtain_creation_date_nepali(self):
        for record in self:
            record.update_date_bs = nepali_datetime.date.from_datetime_date(record.write_date.date())