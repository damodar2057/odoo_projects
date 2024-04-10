from odoo import models, fields, _, api


class Qualification (models.Model):
    _name = 'farmer.qualification'
    _description = 'Qualifications'

    name = fields.Char(string=_('Qualification'))

class Occupation(models.Model):
    _name = 'farmer.occupation'
    _description = 'Occupation'

    name = fields.Char(string=_('Occupation'))


class FarmerFamily(models.Model):
    _name = 'farmer.family'
    _description = 'Farmer Family Members'
    _inherits = {'res.partner': 'partner_id'}

    xchg = fields.Many2one('farmer.family',string=_('Fields For Exchanging'))

    # member_name = fields.Char(string=_('Name'), required=False)
    member_dob = fields.Date(string=_('Date of Birth'), required=False)
    member_gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string=_('Gender'),required=False)
    member_qualification = fields.Many2many('farmer.qualification',string=_('Qualification'),required=False)
    member_occupation = fields.Many2one('farmer.occupation', string=_('Occupation'))
    # member_photo = fields.Binary(string=_(' Photo'))
    member_citizenship_photo = fields.Binary(string=_('Citizenship Photo'))
    member_involved_in_agri = fields.Boolean(string=_('Involved In Agriculture'))
    farmer_id = fields.Many2one(
        'farm.farmer',
        string=_("Farmer"))
    partner_id = fields.Many2one('res.partner', required=True, ondelete='restrict', auto_join=True, index=True,
                                 string='Related Partner', help='Partner-related data of the user',)
    profile_update_id = fields.Many2one('profile.update.request', string=_("Profile Update Request"))
    
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





