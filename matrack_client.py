import requests
import time
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from models import DeviceListResponse, DeviceInfoResponse, RealTimeLocResponse, TripListResponse, AlarmListResponse

# --- MatrackClient class and imports follow ---

class MatrackClient:
    def __init__(self, client_id: str, client_secret: str, base_url: str = 'https://api.matrack.live/v1'):
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = base_url.rstrip('/')
        self.token_url = f'{self.base_url}/auth/token'
        self._access_token = None
        self._refresh_token = None
        self._expires_at = 0

    def _get_token(self):
        now = time.time()
        if self._access_token and self._expires_at > now + 10:
            return self._access_token
        # If refresh_token exists, try to refresh
        if self._refresh_token:
            refreshed = self._refresh_access_token()
            if refreshed:
                return self._access_token
        # Otherwise, get a new token
        data = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        response = requests.post(self.token_url, data=data, timeout=10)
        if response.status_code == 200:
            token_data = response.json()
            self._access_token = token_data['access_token']
            self._refresh_token = token_data.get('refresh_token')
            self._expires_at = now + token_data.get('expires_in', 3600)
            return self._access_token
        else:
            raise Exception(f"Token request failed: {response.status_code} {response.text}")

    def _refresh_access_token(self):
        if not self._refresh_token:
            return False
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': self._refresh_token,
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        response = requests.post(self.token_url, data=data, timeout=10)
        if response.status_code == 200:
            token_data = response.json()
            self._access_token = token_data['access_token']
            self._refresh_token = token_data.get('refresh_token')
            self._expires_at = time.time() + token_data.get('expires_in', 3600)
            return True
        else:
            self._access_token = None
            self._refresh_token = None
            self._expires_at = 0
            return False

    def _auth_headers(self) -> Dict[str, str]:
        token = self._get_token()
        return {'Authorization': f'Bearer {token}'}

    def list_devices(self) -> Any:
        url = f'{self.base_url}/device/list'
        response = requests.get(url, headers=self._auth_headers(), timeout=10)
        response.raise_for_status()
        return response.json()

    def get_device_info(self, device_id: str) -> Any:
        url = f'{self.base_url}/device/info'
        params = {'id': device_id}
        response = requests.get(url, headers=self._auth_headers(), params=params, timeout=10)
        response.raise_for_status()
        return response.json()

    def get_realtime_loc(self, device_id: str) -> Any:
        url = f'{self.base_url}/device/get_realtimeloc'
        params = {'id': device_id}
        response = requests.get(url, headers=self._auth_headers(), params=params, timeout=10)
        response.raise_for_status()
        return response.json()

    def list_trips(self, device_id: str) -> Any:
        url = f'{self.base_url}/trip/list'
        params = {'id': device_id}
        response = requests.get(url, headers=self._auth_headers(), params=params, timeout=10)
        response.raise_for_status()
        return response.json()

    def list_alarms(self, device_id: str) -> Any:
        url = f'{self.base_url}/alarm/list'
        params = {'id': device_id}
        response = requests.get(url, headers=self._auth_headers(), params=params, timeout=10)
        response.raise_for_status()
        return response.json()
