from odoo import models, fields, api
import requests
from ..models.iopgps_client import IOPGPSClient


class VehicleMileageStatistics(models.Model):
    _name = 'vehicle.mileage.statistics'

    vehicle_id = fields.Many2one('fleet.vehicle',"Vehicle")
    attached_gps_device = fields.Char("Attached GPS IMEI")
    travelled_distance = fields.Float("Mileage")
    related_driver = fields.Many2one('driver.details', string="Associated Driver")
    run_time = fields.Float("Runtime")
    vehicle_engine_hours = fields.Float(string="Engine Hours")
    unit = fields.Selection([
        ('km', "K.M"),
        ('miles', "Miles")
    ], string="Unit", default="km", readonly=True)

    def create_maintenance_activity(self):
        vehicle_ref = self.env.ref['fleet.vehicle']
        for record in vehicle_ref:
            threshold_mileage = record['threshold_mileage']
            if self.travelled_distance >= threshold_mileage:
                return "Your time for maintenace is near"

    def get_iopgps_access_token(self):
        # Create an instance of IOPGPSClient
        iopgps_client = IOPGPSClient()

        # Call the get_access_token method on the instance
        access_token = iopgps_client.get_access_token()

        return access_token


    def update_mileage_statistics(self,imei,**kwargs):
        print(imei)
        print("update_mileage_statistics is called")
        url = "https://open.iopgps.com/api/device/miles"
        access_token = self.get_iopgps_access_token()
        # imei = "861449050466603"  # Make sure to use a string, not a tuple
        start_linux_time = "1699594607"
        end_linux_time = ''
        vehicle_name = self.env['fleet.vehicle'].search([['vehicle_attached_gps_imei','=',imei]])
        print(vehicle_name.id)
        response = requests.get(url, params={
            'accessToken': access_token,
            'imei': imei,
            'startTime': start_linux_time,
        })
        print(response)

        if response.status_code == 200:
            # print(vehicle_name)
            mileage_data = response.json()
            print(mileage_data)
            self.create({
                'vehicle_id': vehicle_name.id,
                'attached_gps_device': imei,
                'travelled_distance': mileage_data.get('miles', 0),  # Use get() to handle potential missing key
                'run_time': mileage_data.get('runTime', 0)
            })
        else:
            print(f"Error: {response.text}")

        pass
    



class GpsDeviceStatistics(models.Model):
    _name = 'gps.device.statistics'

    gps_device_id = fields.Char()
    attached_device_id = fields.Char()
    static_count = fields.Integer()
    movement_count = fields.Integer()
    offline_count = fields.Integer()
    unused_count = fields.Integer()

