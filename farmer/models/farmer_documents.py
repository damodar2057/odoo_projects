from odoo import models,fields, _, api


class DocumentType(models.Model):
    _name = 'documents.type'
    _description = 'Document Types'

    name = fields.Char(string=_('Document Type'))


class Document (models.Model):
    _name = 'farmer.documents'
    _description = 'Farmer Documents'

    xchg = fields.Many2one('farmer.documents',string=_('Fields For Exchanging'))
    farmer_id = fields.Many2one('farm.farmer', string=_('Farmer'))
    farmer_group_id = fields.Many2one('farmer.group', string=_("Farmer Group"))
    profile_update_id = fields.Many2one('profile.update.request', string=_("Profile Update Request"))

    documents_types = fields.Many2one('documents.type', string=_('Documents Type'))
    file = fields.Binary(string=_("Upload"))
    
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


