from odoo import models, fields, api

class VehicleTracking(models.Model):
    _name = 'vehicle_tracking.vehicle_tracking'
    _description = 'vehicle_tracking.vehicle_tracking'

    name = fields.Char()
    description = fields.Text()


    def action_open_map(self):
        pass
