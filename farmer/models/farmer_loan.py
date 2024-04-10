from odoo import models, fields, _, api


class InstitutionType(models.Model):
    _name = 'institution.type'
    _description = 'Institution Type'

    name = fields.Char(string=_('Institution Type'))


class InstitutionName(models.Model):
    _name = 'institution.name'
    _description = 'Institution Name'
    _inherits = {'res.partner': 'partner_id'}
    partner_id = fields.Many2one('res.partner', required=True, ondelete='restrict', auto_join=True, index=True,
                                 string='Related Partner', help='Partner-related data of the user',)

    institution_type = fields.Many2one("institution.type",string=_('Institution Type'))





class Loan(models.Model):
    _name = 'farmer.loan'
    _description = 'Farmer Loan Information'

    farmer_id = fields.Many2one('farm.farmer', string=_('Farmer'))
    farmer_group_id = fields.Many2one('farmer.group', string=_("Farmer Group"))
    profile_update_id = fields.Many2one('profile.update.request', string=_("Profile Update Request"))
    xchg = fields.Many2one('farmer.loan',string=_('Fields For Exchanging'))
    institution_type = fields.Many2one('institution.type', string=_('Institution Type'), compute='_get_instutition_type_from_name')
    institution_name = fields.Many2one('institution.name', string=_('Institution Name'))
    loan_amount = fields.Float(string=_('Loan Amount'))


    @api.onchange('institution_name')
    def _get_instutition_type_from_name(self):
        self.institution_type = self.institution_name.institution_type
        
    
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

