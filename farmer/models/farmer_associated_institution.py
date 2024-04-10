from odoo import models, fields, _, api


class AssociatedInstitue(models.Model):
    _name = 'associated.institute'
    _description = 'Associated Institute'

    xchg = fields.Many2one('associated.institute',string=_('Fields For Exchanging'))
    farmer_id = fields.Many2one('farm.farmer', string=_('Farmer'))
    farmer_group_id = fields.Many2one('farmer.group', string=_("Farmer Group"))
    profile_update_id = fields.Many2one('profile.update.request', string=_("Profile Update Request"))
    institution_type = fields.Many2many('institution.type', string=_('Institution Type'))
    institution_name = fields.Many2many('institution.name', string=_('Institution Name'))

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

    



