from odoo import models, fields, _, api
from odoo.exceptions import ValidationError

class LandType(models.Model):
    _name = 'land.type'
    _description = 'Land Types'

    name = fields.Char(string=_('Land Type'))


class IrrigationType(models.Model):
    _name = 'irrigation.type'
    _description = 'Irrigation Types'

    name = fields.Char(string=_('Irrigation Type'))


class RoadType(models.Model):
    _name = 'road.type'
    _description = 'Road Types'

    name = fields.Char(string=_('Road Type'))


class Land(models.Model):
    _name = 'farmer.land'
    _description = 'Land Information'

    farmer_id = fields.Many2one('farm.farmer', string=_('Farmer'))
    farmer_group_id = fields.Many2one('farmer.group', string=_("Farmer Group"))
    profile_update_id = fields.Many2one('profile.update.request', string=_("Profile Update Request"))
    xchg = fields.Many2one('farmer.land',string=_('Fields For Exchanging'))
    land_types = fields.Many2many('land.type', string=_('Land Types'))
    is_leased = fields.Boolean(string=_('Is leased'), required=True)
    has_irrigation = fields.Boolean(string=_('Has Irrigation'), required=True)
    irrigation_area = fields.Float(string=_("Irrigation Area"))
    irrigation_types = fields.Many2many('irrigation.type', string=_('Irrigation Types'))
    has_road_access = fields.Boolean(string=_('Has Road Access'), required=True)
    road_types = fields.Many2many('road.type', string=_('Road Types'))
    has_tunnel_agriculture = fields.Boolean(string=_('Has Tunnel Irrigation'), required=True)
    tunnel_count = fields.Integer(string=_("Tunnel Count"))
    tunnel_size = fields.Float(String=_('Tunnel Size'))
    tunnel_area = fields.Float(string=_('Tunnel Area'))

    land_area = fields.Float(string=_('Land Area(Sq. ft)'))
    unit_of_measurement = fields.Many2one('uom.uom',string=_('Unit'),domain="[('category_id','=',5)]")
    land_area_m2 = fields.Float(string=_("Land Area (meter sq.)"),compute='_compute_land_area_m2')

    @api.onchange('land_area','unit_of_measurement')
    def _compute_land_area_m2(self):
        for record in self:
            if record.land_area and record.unit_of_measurement:
                if record.unit_of_measurement.uom_type == 'bigger':
                    record.land_area_m2 = record.land_area * record.unit_of_measurement.ratio
                elif record.unit_of_measurement.uom_type == 'smaller':
                    record.land_area_m2 = record.land_area/record.unit_of_measurement.ratio
                elif record.unit_of_measurement.uom_type == 'reference':
                    record.land_area_m2 = record.land_area
            # else:
            #     raise ValidationError(_("Please Enter Land Area and Unit"))

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




