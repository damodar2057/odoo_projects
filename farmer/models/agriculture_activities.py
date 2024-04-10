from odoo import models,fields,_


class AgricultureActivity (models.Model):
    _name= 'farmer.agriculture.activities'
    _description= 'Agriculture activities'

    name = fields.Char(string=_('Agriculture Activity'))


class SeedlingLists (models.Model):
    _name= 'seedling.lists.model'
    _description= 'Seedling Lists'

    name = fields.Char(string=_('Seedling Lists'))



