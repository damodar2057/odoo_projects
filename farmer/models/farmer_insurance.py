from odoo import models, fields, _, api
import nepali_datetime

#Produce Insurance Model
class ProduceInsurance(models.Model):
    _name = 'produce.insurance'
    _description = 'Produce Insurance'

    farmer_id = fields.Many2one('farm.farmer', string=_('Farmer'))
    farmer_group_id = fields.Many2one('farmer.group', string=_("Farmer Group"))
    xchg = fields.Many2one('produce.insurance',string=_('Fields For Exchanging'))

    producer_id = fields.Integer("Producer",compute='_get_producer_id',)

    @api.depends('farmer_id','farmer_group_id')
    def _get_producer_id(self):
        for record in self:
            if record.farmer_id:
                record.producer_id = record.farmer_id.producer_id._origin.id
            elif record.farmer_group_id:
                record.producer_id = record.farmer_group_id.producer_id.id

    profile_update_id = fields.Many2one('profile.update.request', string=_("Profile Update Request"))

    # insurance_type_id = ref('farmer_organization_type_insurance')
    insurance_company = fields.Many2one("organization.farmer", "Insurance Company", domain="[('type','=',1)]")
    insured_produce = fields.Many2one('farm.produce','Insured Product')
    insured_amount = fields.Float('Insured Amount')
    insured_date = fields.Date("Insured Date(A.D.)",compute='_obtain_insured_date_ad')
    insured_date_bs = fields.Char("Insured Date(B.S.)")

    @api.depends('insured_date_bs')
    def _obtain_insured_date_ad(self):
        for record in self:
            if record.insured_date_bs:
                record.insured_date = nepali_datetime.datetime.strptime(record.insured_date_bs, '%Y-%m-%d').to_datetime_date()
            else:
                record.insured_date = None

    validity_date = fields.Date("Validity Date(A.D.)",compute='_obtain_validity_date_ad')
    validity_date_bs = fields.Char("Validity Date(B.S.)")

    @api.depends('validity_date_bs')
    def _obtain_validity_date_ad(self):
        for record in self:
            if record.validity_date_bs:
                record.validity_date = nepali_datetime.datetime.strptime(record.validity_date_bs, '%Y-%m-%d').to_datetime_date()
            else:
                record.validity_date = None

    delete_request=fields.Boolean(default=False)
    
    @api.model
    def write(self, vals):
        '''
        normal write for following condition:
        1. if group_user_access
        2. delete_request is not updated 
        '''
        if self.env.user.user_has_groups('farmer.group_user_access') or 'delete_request' not in  vals.keys():
            return super().write(vals)
        if self.farmer_id.id and not self.farmer_id.requesting:
            self.farmer_id.requesting = True
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