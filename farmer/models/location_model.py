from odoo import models, fields,api,_

class LocationProvince(models.Model):
    _name = 'location.province'
    _description = 'Province Name'

    name = fields.Char(string=_('Province Name'))   
    name_np = fields.Char(string=_('Province Name NEP'))   
    reference_id = fields.Char("Reference ID")
    reference_code = fields.Char("Reference Code")
    
    def name_get(self):
        result = []
        if self._context["lang"]=='ne_NP':
            for rec in self:
                result.append((rec.id, rec.name_np))
        else:
            for rec in self:
                result.append((rec.id, rec.name))
        return result

class LocationDistrict(models.Model):
    _name = 'location.district'
    _description = 'Location District Information'

    province_name = fields.Many2one('location.province',string=_('Province'))
    district_name = fields.Char(string=_('District'))
    district_name_np = fields.Char(string=_('District(NEP)'))
    reference_id = fields.Char("Reference ID")
    reference_code = fields.Char("Reference Code")
    
    def name_get(self):
        result = []
        if self._context["lang"]=='ne_NP':
            for rec in self:
                result.append((rec.id, rec.district_name_np))
        else:
            for rec in self:
                result.append((rec.id, rec.district_name))
        return result
    
class LocationPalika(models.Model):
    _name = 'location.palika'
    _description = 'Location Palika Information'

    district_name = fields.Many2one('location.district',string=_('District'))
    palika_name = fields.Char(string=_('Palika'))
    palika_name_np = fields.Char(string=_('Palika(NEP)'))
    reference_id = fields.Char("Reference ID")
    reference_code = fields.Char("Reference Code")
        
    def name_get(self):
        result = []
        if self._context["lang"]=='ne_NP':
            for rec in self:
                result.append((rec.id, rec.palika_name_np))
        else:
            for rec in self:
                result.append((rec.id, rec.palika_name))
        return result


class PalikaTole(models.Model):
    _name = 'location.tole'
    _description = 'Location Tole Information'

    palika_name = fields.Many2one('location.palika',string=_('Palika'))
    tole_name = fields.Char(string=_('Tole'))
    tole_name_np = fields.Char(string=_('Tole(NEP)'))
    ward_number = fields.Integer(string=_('Ward Number'))
    reference_id = fields.Char("Reference ID")
    reference_code = fields.Char("Reference Code")
    
    def name_get(self):
        result = []
        if self._context["lang"]=='ne_NP':
            for rec in self:
                result.append((rec.id, rec.tole_name_np))
        else:
            for rec in self:
                result.append((rec.id, rec.tole_name))
        return result

