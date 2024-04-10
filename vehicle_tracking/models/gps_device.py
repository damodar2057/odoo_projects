from odoo import models,fields,api
import requests
from ..models.iopgps_client import IOPGPSClient


class GpsDevice(models.Model):
    _name = 'gps.device.info'
    _description = 'GPS Tracking Device'

    name = fields.Char(string='Device Name',required=True)
    imei_no = fields.Char(string='IMEI', required=True)
    vin_no = fields.Char(required=True)
    mobile_no = fields.Char(required=True)
    account = fields.Char()
    license_number = fields.Char()
    vehicle_owner = fields.Char()
    device_type = fields.Selection([('vehicle', 'Vehicle Tracker'), ('personal', 'Personal Tracker')], string='Device Type')
    battery_status = fields.Char(string='Battery Status')
    last_communication_time = fields.Datetime(string='Last Communication Time')
    firmware_version = fields.Char(string='Firmware Version')
    # installed_apps = fields.Many2many('gps.app', string='Installed Apps')
    sim_card_info = fields.Char(string='SIM Card Information')
    vendor_id=fields.Many2one('res.partner',string="Vendor")
    vendor_type=fields.Many2one('res.partner',string="Vendor Type")

    def get_iopgps_access_token(self):
        # Create an instance of IOPGPSClient
        iopgps_client = IOPGPSClient()

        # Call the get_access_token method on the instance
        access_token = iopgps_client.get_access_token()

        return access_token

    @api.model
    def create(self, vals):
        access_token = self.get_iopgps_access_token()
        payload = {
            'imei': vals.get('imei_no'),
            'vin': vals.get('vin_no'),
            'mobile': vals.get('mobile_no'),
            'deviceName': vals.get('name'),
            'account': vals.get('account'),
            'license_number': vals.get('license_number'),
            'type': vals.get('device_type'),
            'carOwner': vals.get('vehicle_owner')
        }

        response = requests.post("https://open.iopgps.com/api/device", params={
            'accessToken': access_token
        }, json=payload)

        response_data = response.json()
        print(response_data)

        if response.status_code == 200:
            # Status code 200 indicates a successful request
            created_record = super(GpsDevice, self).create({
                'name': vals.get('name'),
                'imei_no': vals.get('imei_no'),
                'vin_no': response_data.get('vin') or vals.get('vin_no'),
                'mobile_no': response_data.get('mobile') or vals.get('mobile_no'),
                'account': response_data.get('account') or vals.get('account'),
                'license_number': response_data.get('license_number') or vals.get('license_number'),
                'vehicle_owner': response_data.get('carOwner') or vals.get('vehicle_owner'),
                'device_type': response_data.get('type') or vals.get('device_type'),
                'battery_status': response_data.get('battery_status'),
                'last_communication_time': response_data.get('last_communication_time'),
                'firmware_version': response_data.get('firmware_version'),
                'sim_card_info': response_data.get('sim_card_info'),
            })

            return created_record
        else:
            error_message = response_data.get('message', 'Unknown error')
            raise Exception(f"Error: {error_message}")

    def update_active_gps_devices_list(self):
        # request.get()
        pass

    # Add other relevant fields as needed

class GpsDeviceCurrentStatus(models.Model):
    _name = 'gps.device.current.status'

    imei = fields.Char()
    device_status = fields.Char() # // Status clarification: Static, Moving, Sleep, Inactive,Offline
    longitude = fields.Char()
    latitude = fields.Char()
    speed = fields.Float()
    course = fields.Float()
    acc_status = fields.Char() # // ACC status, true for open, false for off
    position_type = fields.Char() # // Location type, GPS/LBS/WiFi
    license_number = fields.Char() # // Plate number
    vin_number = fields.Integer()
    status_time_desc = fields.Datetime() # Status Duration
    signal_time = fields.Integer() # Last signal time
    activate_time = fields.Integer() # Activate time
    sim_end_time = fields.Integer() # SImCard End time
    platform_end_time = fields.Integer() # Platform End time
    end_time = fields.Integer() # User End time
    charge_percentage = fields.Integer() # Wireless battery level 0-100
    gps_time = fields.Integer() # Location time

