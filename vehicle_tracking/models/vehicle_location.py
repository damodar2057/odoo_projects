from odoo import models, fields, api, tools
import requests
import hashlib
import time
# import schedule
from datetime import datetime, timezone, timedelta
from ..models.iopgps_client import IOPGPSClient
# from nepali_datetime import NEPAL_TIME_UTC_OFFSET

class VehicleCurrentLocation(models.Model):
    _name = 'vehicle.location'
    _description = 'Vehicle Location Data'

    vehicle_id = fields.Char(string='Vehicle IMEI ID')
    # attached_gps_id = fields.Char()
    latitude = fields.Float(string='Latitude',digits=(10,7))
    longitude = fields.Float(string='Longitude',digits=(10,7))
    gps_time = fields.Char("GPS Time")
    address = fields.Char("Address")
    title = fields.Char()
    status=fields.Selection([('running','Running'),('active','Active'),('inactive','Inactive'),('out of contact','Out of Contact')],string="Status",default='active')

    # speed = fields.Float(string='Speed')
    # time = fields.Datetime(string='Timestamp', default=fields.Datetime.now)
    # vehicle_id = fields.Many2one('delivery.vehicle', string='Vehicle', required=True)

    # Add other relevant fields as needed
    # access_token_cache = {}
    #
    #
    # def calculate_signature(self,login_key, time):
    #     # Step 1: MD5 hashing
    #     step1_hash = hashlib.md5(login_key.encode('utf-8')).hexdigest()
    #     print(step1_hash)
    #     timestamp = time
    #     # Step 2: Append timestamp
    #     step2_data = f"{step1_hash}{timestamp}"
    #     print(step2_data)
    #
    #     # Step 3: MD5 hashing again
    #     signature = hashlib.md5(step2_data.encode('utf-8')).hexdigest()
    #
    #     return signature
    #
    #
    #
    # @api.model
    # # @tools.ormcache('access_token_cache', 'get_auth_token','appid', 'signature', 'time')
    # def get_auth_token(self, appid, signature, timestamp):
    #     url = 'https://open.iopgps.com/api/auth'
    #
    #     appid = appid
    #     time = timestamp
    #     signature = '2e36f4b5a2abda50a5481479720b9ed1'
    #
    #     # request body
    #
    #     # check if the access token is in cache and is not expired
    #     cached_token_info = self.access_token_cache.get((appid,signature, time),{})
    #     if 'token' in cached_token_info and 'expires_at' in cached_token_info:
    #         current_time = int(time.time())
    #         if current_time < cached_token_info['expires_at']:
    #             return cached_token_info['token']
    #
    #     payload = {
    #         'appid': appid,
    #         'signature': signature,
    #         'time': time
    #     }
    #
    #     # Now make the api call
    #     try:
    #         # print(first)
    #         response = requests.post(url, json=payload)
    #         print(response)
    #         response_data = response.json()
    #
    #         # check if the request was successful or not
    #         if response.status_code == 200 and 'accesstoken' in response_data:
    #             access_token = response_data['accesstoken']
    #             expires_in = response_data.get('expiresIn',7200)
    #             # cache the access token with its expiration time
    #             expires_at = int(time.time()) + expires_in
    #             self.access_token_cache[(appid, signature, time)] = {'token': access_token, 'expires_at': expires_at}
    #             # You can now use the access token
    #             return access_token
    #         else:
    #             # Handle error or raise an exception
    #
    #             error_message = response_data.get('message', 'Unknown error')
    #             raise Exception(f"Error: {error_message}")
    #
    #
    #     except requests.RequestException as e:
    #         raise Exception(f"Connection Error: {e}")
    #
    # def get_request_headers(self):
    #     # Get headers with access token for the api requests
    #     appid = 'shangrila'
    #     login_key = "FnhBw@uCE7f2g4YC&teqXvCQWZbxhNR&"
    #     timestamp = 1699868056
    #
    #     # Retrieve the access token from the cache or generate a new one
    #     access_token = self.get_auth_token(appid, self.calculate_signature(login_key, timestamp),timestamp)
    #
    #     # Setup headers with access token
    #     headers = {
    #         'Authorization': f'Bearer {access_token}',
    #         'Content-Type': 'application/json'
    #     }
    #     return headers
    #
    #     # Get the device location

    @api.model_create_multi
    def create(self,vals):
        # vals['status']=True
        record=super(VehicleCurrentLocation,self).create(vals)

        record.update_location_of_gps()
        return record

        # return record

    def update_location_of_gps(self):
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
    def get_iopgps_access_token(self):
        # Create an instance of IOPGPSClient
        iopgps_client = IOPGPSClient()

        # Call the get_access_token method on the instance
        access_token = iopgps_client.get_access_token()
        print(access_token)

        return access_token
    def get_device_location(self, **kwargs):
        vehicle_ref=self.env['fleet.vehicle'].search([])
        for v_ref in vehicle_ref:
            if(v_ref.vehicle_attached_gps_imei):
                print(v_ref.vehicle_attached_gps_imei)
                print("called for imei")
                imei = v_ref.vehicle_attached_gps_imei
                accessToken = self.get_iopgps_access_token()
                # accessToken = "b4a2353d84f411ee8475fa163ece138c"
                url = 'https://open.iopgps.com/api/device/location'

                try:
                    response = requests.get(url, params={'accessToken': accessToken, 'imei': imei})
                    response_data = response.json()


                    if response.status_code == 200:
                        mileage_model_ref = self.env['vehicle.mileage.statistics']
                        print("printed before calling update_mileage_statistics")
                        mileage_model_ref.update_mileage_statistics(imei)
                        print("returned from update_mileage_statistics")
                        self.save_location_data(response_data, imei)
                        # Assuming 'gpsTime' is a Unix timestamp in response_data
                        unix_time = response_data.get('gpsTime')
                        formatted_time = self.convert_unix_to_datetime(unix_time)

                        return {
                            "lat": response_data['lat'],
                            "lng": response_data['lng'],
                            "time": formatted_time
                        }
                    else:
                        error_message = response_data.get('message', 'Unknown error')
                        raise Exception(f"Error: {error_message}")
                except requests.RequestException as e:
                    raise Exception(f"Connection Error")

    def convert_unix_to_datetime(self, unix_time):
        if unix_time:
            # Convert Unix timestamp to a datetime object
            datetime_obj = datetime.fromtimestamp(unix_time)

            # Format the datetime object as a string
            formatted_time = datetime_obj.strftime('%Y-%m-%d %H:%M:%S')

            return formatted_time
        else:
            return None
    def save_location_data(self,location_data,imei):
        DeviceLocation = self.env['vehicle.location']
        timestamp = location_data.get('gpsTime')
        utc_time = datetime.utcfromtimestamp(timestamp)
        # Add the Nepal time zone offset (UTC+5:45)
        nepal_time = utc_time + timedelta(hours=5, minutes=45)
        # Format the datetime object as a string
        formatted_time = nepal_time.strftime('%Y-%m-%d %H:%M:%S')
        print(imei)
        print(location_data.get)
        print(formatted_time)

        # iterate through the location data and save each location entry
        DeviceLocation.create({
            'vehicle_id': imei,
            'longitude': location_data.get('lng'),
            'latitude': location_data.get('lat'),
            'gps_time':formatted_time,
            'address': location_data.get('address')
        })
        print("Location Loaded")


    # schedule the method to run every  10 seconds

    def schedule_location_job(self):
        schedule.every(10).seconds.do(self.get_device_location)

        while True:
            schedule.run_pending()
            time.sleep(15)









