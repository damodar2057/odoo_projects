from odoo import models, fields,api,_

class ProgramsYear(models.Model):
    _name = 'programs.year'
    _description = 'Programs Year'

    name = fields.Char(string=_('Year'))   
    
class YearProgram(models.Model):
    _name = 'year.program'
    _rec_name = 'program_name'
    _description = 'Year Program'

    year = fields.Many2one('programs.year',string=_('Year'))
    program_name = fields.Char(string=_('Program'))
    
class ProgramProject(models.Model):
    _name = 'program.project'
    _rec_name = 'project_name'
    _description = 'Program Project'

    program_name = fields.Many2one('year.program',string=_('Program'))
    project_name = fields.Char(string=_('Project'))