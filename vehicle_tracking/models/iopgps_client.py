import requests
from odoo import http
import time


class IOPGPSClient:
    def __init__(self):
        self.auth_url = "https://open.iopgps.com/api/auth"
        self.app_id = "shangrila"
        self.signature = "2e36f4b5a2abda50a5481479720b9ed1"
        self.time = 1699868056

    def get_access_token(self):
        session = http.request.session
        access_token = session.get('iopgps_access_token')
        expiration_time = session.get('iopgps_access_token_expiration')

        if not access_token or not expiration_time or self.is_token_expired(expiration_time):
            access_token, expiration_time = self.refresh_access_token()
            print("Auth request is continously sending")
            session['iopgps_access_token'] = access_token
            session['iopgps_access_token_expiration'] = expiration_time

        return access_token

    def is_token_expired(self, expiration_time):
        current_time = int(time.time())
        if expiration_time <= current_time:
            return True
        else:
            return False

    def refresh_access_token(self):
        payload = {
            "appid": self.app_id,
            "signature": self.signature,
            "time": self.time
        }
        response = requests.post(self.auth_url, json=payload)

        if response.status_code == 200:
            data = response.json()
            new_access_token = data.get('accessToken')
            print(new_access_token)
            new_expiration_time = data.get('expiresIn')
            current_timestamp_in_milliseconds = int(time.time()*1000)
            expiration_time_in_milliseconds = current_timestamp_in_milliseconds + new_expiration_time
            new_expiration_time_unix = expiration_time_in_milliseconds // 1000
            return new_access_token, new_expiration_time_unix
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None, None
