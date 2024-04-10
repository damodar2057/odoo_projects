from odoo import models,fields,api
from datetime import datetime, timedelta

class DriverStateAndCurrentLocation(models.Model):
    _name = 'driver.current.state.location'
    _rec_name = 'vehicle_id'

    vehicle_id = fields.Many2one('fleet.vehicle',ondelete='cascade')
    status = fields.Boolean("Current State",default=False)
    current_latitude = fields.Char(name="latitude",digits=(10,7))
    current_longitude = fields.Char(name='longitude',digits=(10,7))
    license_plate_no = fields.Char(string='License Plate', related='vehicle_id.license_plate', readonly=True)

    @api.model_create_multi
    def create(self,vals):
        # vals['status']=True
        record=super(DriverStateAndCurrentLocation,self).create(vals)

        record.update_location()
        return record

        # return record

    def update_location(self):
        drivers_details_forUpdate = self.env['fleet.vehicle'].search([])
        print("scheduled called")
        for rec in drivers_details_forUpdate:
            if (rec.vehicle_attached_gps_imei):
                curr_location = self.env['vehicle.location'].search([['vehicle_id','=',rec.vehicle_attached_gps_imei]],order='create_date desc',limit=1)
                if (curr_location):
                    if (curr_location):
                        updatedtime = curr_location.create_date
                        time_diff = datetime.now() - updatedtime
                        time_diff_min = time_diff.total_seconds() / 60
                        if (time_diff_min < 1):
                            if (rec.prev_lat == rec.latitude and rec.prev_lng==rec.longitude):
                                rec.status = 'active'
                            else:
                                rec.status = 'running'
                        else:
                            time_diff_days = time_diff_min / (60 * 24)
                            if (time_diff_days > 7):
                                rec.status = 'out of contact'
                            else:
                                rec.status = 'inactive'

                    else:
                        print("current_location not found")
            else:
                current_location = self.env['driver.current.state.location'].search([['license_plate_no', '=', rec.license_plate]],
                                                                  order='create_date desc', limit=1)
                if (current_location):
                    if (current_location):
                        rec.prev_lat = rec.latitude
                        rec.prev_lng = rec.longitude
                        rec.latitude = current_location.current_latitude
                        rec.longitude = current_location.current_longitude
                        updatedtime = current_location.create_date
                        time_diff = datetime.now() - updatedtime
                        time_diff_min = time_diff.total_seconds() / 60
                        if (time_diff_min < 1):
                            if (rec.prev_lat == rec.latitude and rec.prev_lng==rec.longitude):
                                rec.status = 'active'
                            else:
                                rec.status = 'running'
                        else:
                            time_diff_days = time_diff_min / (60 * 24)
                            if (time_diff_days > 7):
                                rec.status = 'out of contact'
                            else:
                                rec.status = 'inactive'

                    else:
                        print("current_location not found")
        pass