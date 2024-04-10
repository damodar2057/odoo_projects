from odoo import models, fields, api
import requests
from ..models.iopgps_client import IOPGPSClient


class BindFleetGps(models.Model):
    _name = 'bind.fleet.gps'

    vehicle_id = fields.Many2one('fleet.vehicle',required=True)
    gps_device_id = fields.Many2one('gps.device.info',required=True)
    status = fields.Boolean()

    def get_iopgps_access_token(self):
        # Create an instance of IOPGPSClient
        iopgps_client = IOPGPSClient()

        # Call the get_access_token method on the instance
        access_token = iopgps_client.get_access_token()

        return access_token

    @api.model
    def create(self, vals):
        access_token = self.get_iopgps_access_token()
        vehicle_ref_id = vals.get('vehicle_id')
        vehicle_ref = self.env['fleet.vehicle'].browse(vehicle_ref_id)
        gps_ref_id = vals.get('gps_device_id')
        # Fetch the related record
        gps_ref = self.env['gps.device.info'].browse(gps_ref_id)
        payload = {
            "data":[
                {
                    "name":gps_ref.name,
                    "cardNo":gps_ref.sim_card_info,
                    "imei":gps_ref.imei_no
                },
            ],
            "vin":vehicle_ref.vin,
            "carOwner": vehicle_ref.carOwner,
            "contactUser": vehicle_ref.contactUser,
            "licenseNumber": vehicle_ref.license_no,
            "contractNumber": vehicle_ref.contract_no,
            "contactTel": vehicle_ref.contactRef
        }
        bind_url = "https://open.iopgps.com/api/vehicle"
        response = requests.post(bind_url,params={
            "accessToken":access_token,
        },json=payload)
        response_data = response.json()
        if response.status_code == 200:
            self.status = True
            result = super(BindFleetGps, self).create(vals)
        else:
            print("Error")

        # print(gps_ref.imei_no)
        # # Ensure to call the original create method and return its result
        result = super(BindFleetGps, self).create(vals)
        return result
    #
    # @api.model
    # def unlink(self):
    #     access_token = self.get_iopgps_access_token()
    #     payload = {
    #         "imeis":[
    #             "1234321",
    #             "13432123"
    #         ]
    #     }
    #     response = requests.put(url="https://open.iopgps.com/api/device/unbind/vehicle",
    #                  params={
    #                      'accessToken':access_token
    #                  },json=payload)
    #     if response.status_code == 200:
    #         super(BindFleetGps,self).unlink()
class MobileWithGPS(models.Model):
    _name = 'mobile.gps'

    driver_id = fields.Many2one('driver.details',required=True)
    imei_no = fields.Char('imei')
    device_type = fields.Selection([('android','Android'),
                                    ('ios','IOS')])
    device_model = fields.Char("Device Model")
    device_manufacturer = fields.Char("Manufacturer")
