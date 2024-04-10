from odoo import models, fields, _, api
import nepali_datetime
from datetime import date

class ExpertType(models.Model):
    _name = 'expert.type'
    _description = 'Expert Type'

    name = fields.Char(string=_('Expert Type'))

class TechnicianType(models.Model):
    _name = 'technician.type'
    _description = 'Technician Type'

    name = fields.Char(string=_('Technician Type'))

class Expert (models.Model):
    _name = 'expert.experts'
    _description = 'experts'
    _inherits = {'res.partner': 'partner_id'}

    branch = fields.Selection([
        ('ag_branch', 'Agriculture Branch'),
        ('animal_branch', 'Animal Branch'),
    ], string=_('Branch'))
    province = fields.Many2one('location.province',string=_('Province'))
    district = fields.Many2one('location.district',string=_('District'))
    palika = fields.Many2one('location.palika',string=_('Palika'))
    ward_no = fields.Integer(string=_('Ward No'),required=False)
    tole = fields.Many2one('location.tole',string=_('Tole'))
    expert_type = fields.Many2one('expert.type', string=_('Expert Type'))
    # Relational Fields
    partner_id = fields.Many2one('res.partner', required=True, ondelete='restrict', auto_join=True, index=True,
                                 string='Related Partner', help='Partner-related data of the user',)


class Technician (models.Model):
    _name = 'technician.technicians'
    _description = 'technicians'
    _inherits = {'res.partner': 'partner_id'}

    branch = fields.Selection([
        ('ag_branch', 'Agriculture Branch'),
        ('animal_branch', 'Animal Branch'),
    ], string=_('Branch'))
    province = fields.Many2one('location.province',string=_('Province'))
    district = fields.Many2one('location.district',string=_('District'))
    palika = fields.Many2one('location.palika',string=_('Palika'))
    ward_no = fields.Integer(string=_('Ward No'),required=False)
    tole = fields.Many2one('location.tole',string=_('Tole'))

    technician_type = fields.Many2one('technician.type', string=_('Technician Type'))

    # Relational Fields
    partner_id = fields.Many2one('res.partner', required=True, ondelete='restrict', auto_join=True, index=True,
                                 string='Related Partner', help='Partner-related data of the user',)
