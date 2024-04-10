from odoo import models,fields,api
from lxml import etree
import requests
from datetime import datetime, timedelta


class VehicleInformation(models.Model):
    _inherit = 'fleet.vehicle'

    vehicle_attached_gps_imei = fields.Char(string="Attached Gps IMEI")
    vehicle_attached_gps_sim_card_no = fields.Integer("Gps Sim No")
    is_gps_activated = fields.Boolean("Is GPS Active",default=False)
    threshold_mileage = fields.Float("Threshold Mileage")
    threshold_engine_hours = fields.Float("Threshold Engine Hours")
    default_maintenance_interval = fields.Integer("Maintenance Interval")
    manufacturer_recommended_interval = fields.Integer("Manufacturer Recommended Interval")
    regulator_recommended_interval = fields.Integer("Regulator Recommended Interval")
    interval = fields.Selection([
        ("Days","Days"),
        ("Week","Week"),
        ("Month","Month"),
    ],string="Interval Period",default="Days")
    # bluebook_validity = fields.Date("Bluebook Validity")
    renewal_documents_ids = fields.One2many('renewal.documents','fleet_id',string="Documents")
    status = fields.Selection(
        [('active', 'Active'), ('inactive', 'Inactive'), ('running', 'Running'), ('out of contact', 'Out of contact')],
        string='Status',
        default='running',
        help='Choose an status of driver'
    )
    latitude = fields.Float(string="Latitude", store=True, digits=(10, 7))
    longitude = fields.Float(string="Longitude", store=True, digits=(10, 7))
    prev_lat = fields.Float(string='PreviousLat', store=True, digits=(10, 7))
    prev_lng = fields.Float(string='PreviousLng', store=True, digits=(10, 7))

    # def notify_owl_component(self):
    #     channel_name = 'vehicle-updated'
    #     self.env['bus.bus'].sudo()._sendone(channel_name, {},None)


    # def check_validity(self):
    #     current_date = datetime.now().current()
        
    #     for rec in self:
    #         if rec.bluebook_validity:
    #             today = datetime.now().date()
    #             expiration_date = fields.Date.from_string(rec.bluebook_validity)
    #             remaining_days = (expiration_date-today).days

    #             # threshold_days
    #             threshold_days = 30
                
    #             if remaining_days <= threshold_days:
    #                 rec.notify_bluebook_expiration(remaining_days)


    # def notify_bluebook_expiration(self):
    #     pass
    # This is for the computation of current location and filter of status accordingly
    # def long_polling_method(self):
    #     return {'type': 'long-polling-response', 'data': 'Hello from server!'}


    def _compute_current_location2(self):
        drivers_details_forUpdate = self.env['fleet.vehicle'].search([])
        print("scheduled called")
        for rec in drivers_details_forUpdate:
            if (rec.vehicle_attached_gps_imei):
                curr_location = self.env['vehicle.location'].search([['vehicle_id','=',rec.vehicle_attached_gps_imei]],order='create_date desc',limit=1)
                if (curr_location):
                    if (curr_location):
                        rec.prev_lat = rec.latitude
                        rec.prev_lng = rec.longitude
                        rec.latitude = curr_location.latitude
                        rec.longitude = curr_location.longitude
                        updatedtime = curr_location.create_date
                        time_diff = datetime.now() - updatedtime
                        time_diff_min = time_diff.total_seconds() / 60
                        if (time_diff_min < 1):
                            if (rec.prev_lat == rec.latitude):
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
                            if (rec.prev_lat == rec.latitude):
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
            # self.notify_owl_component()
            # bus.trigger('vehicle-updated')


    # This is for the maintenance schedular
    def check_for_maintenance(self):
        vehicle_ids = self.env['fleet.vehicle'].search([])
        for record in vehicle_ids:
            
            # fetching data from vehicle.mileage.statistics 
            current_vehicle_mileage_statistics_id = self.env['vehicle.mileage.statistics'].search([('vehicle_id','=',record.id)],order='create_date desc',limit=1)
            current_vehicle_travelled_distance = self.env['vehicle.mileage.statistics'].search([('vehicle_id','=',record.id)],order='create_date desc',limit=1)
            print(f"Current Vehicle travelled distance:: {current_vehicle_mileage_statistics_id.travelled_distance}")
            
            # fetching data from fleet.vehicle.odoometer
            odometer_value_id = self.env['fleet.vehicle.odometer'].search([('vehicle_id','=',record.id)],order='date desc',limit=1)
            odometer_current_vehicle_value=odometer_value_id.value
            print(f"Odoometer Value::{odometer_current_vehicle_value}")
            odometer_current_vehicle_last_service_date=odometer_value_id.date
            print(f"Odoometer last service date:: {odometer_current_vehicle_last_service_date}")

            # Getting required data for checking maintenance needed or not
            threshold_mileage = record.threshold_mileage    
            print(f"Threshold Mileage{threshold_mileage}")                        
            manufacturer_recommend = record.manufacturer_recommended_interval                
            regulator_recommend = record.regulator_recommended_interval
            mean_recommend = int((manufacturer_recommend+regulator_recommend)/2)
            print(f"Mean recommend {mean_recommend}")
            

            if odometer_current_vehicle_last_service_date:
            # Making data for date interval
                today = fields.Date.today()  
                print(today)                        
                servicing_needed_date = odometer_current_vehicle_last_service_date+timedelta(days=mean_recommend)
                print(servicing_needed_date)
                if today >= servicing_needed_date or current_vehicle_travelled_distance >= odometer_current_vehicle_value+threshold_mileage:
                    print("servicing needed")
                    template_ref = self.env.ref('vehicle_tracking.vehicle_maintenance_email_template')
                    template_ref.send_mail(self.id, force_send=True)
                    
                else:
                    print("Service is not Needed")
                
            else:
                print("Odometer last service date not found, unable to calculate servicing needed date.")


    
    # user_id = fields.Many2one('res.users', string='Driver')
    # is_active_driver = fields.Boolean(related='user_id.partner_id.is_driver', string='Is Active Driver', readonly=True, store=False)
    # Override driver_id field
    # driver_id = fields.Many2one(
    #     'res.partner', 'Driver',
    #     tracking=True, help='Driver of the vehicle',
    #     copy=False,domain
    # )
    # driver_id = fields.Many2one('res.users', string='Driver')
    # vehicle_name = fields.Char()
    # vehicle_note = fields.Char()
    # vin_no = fields.Char()
    # vehicle_owner = fields.Char()
    # contact_user = fields.Char()
    # vehicle_plate_number = fields.Char()
    # contract_number = fields.Char()
    # contact_telephone = fields.Char()

    # def create(self, vals_list):
    #     if vals_list


    # This is to register vehicle with gps
    def action_activate_gps(self):
        url = 'https://open.iopgps.com/api/device?accessToken='
        view_id = self.env.ref('vehicle_tracking.fleet_vehicle_form_inherit')
        print(view_id)
        if view_id:
            print(view_id.arch)
            # Parse the XML string into an element tree
            arch_tree = etree.fromstring(view_id.arch)
            print(arch_tree)            # Find the button node using xpath function
            button_node = arch_tree.xpath("//button[@name='action_activate_gps']")
            print(button_node)

            if button_node:
                # Update the 'string' attribute of the button node
                button_node[0].set('string', 'Activated')
                print(button_node)

                # Convert the modified tree back to a string and update the view
                view_id.arch = etree.tostring(arch_tree, encoding='utf-8', pretty_print=True)
                print(view_id.arch)

        return True
        # access_token = ''
        # imei = ''
        # payload = {
        #     "Imei": imei,
        #     "Type": type,
        #     "Vin": "vin_code",
        #     "Account": "demo",
        #     "LicenseNumber": "Ba Kha 1212",
        #     "Mobile": 9392929292,
        #     "DeviceName": "Device Name",
        #     "CarOwner":"Owner's name"
        #
        # }
        # response = requests.post(url, json=payload)
        #
        # #check if the request was successful or not
        # if response.status_code == 200:
        #     self.is_gps_activated = True
        #     print("if response has code 0 in it wa successful")
        #

class FleetWithGps(models.Model):
    _name = 'fleet.with.gps'

    fleet_id = fields.Many2one('fleet.vehicle')
    gps_imei = fields.Char(compute="generate_gps_of_fleet")

    @api.model
    def generate_gps_of_fleet(self):
        self.gps_imei = self.fleet_id.vehicle_attached_gps_imei