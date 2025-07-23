import requests
import time
from typing import Optional, Dict, Any

class MatrackClient:
    def __init__(self, client_id: str, client_secret: str, base_url: str = "https://api.matrack.live/v1"):
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = base_url.rstrip("/")
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None
        self.token_expiry: float = 0.0

    def _get_token(self):
        url = f"{self.base_url}/auth/token"
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials"
        }
        resp = requests.post(url, data=data)
        resp.raise_for_status()
        token_data = resp.json()
        self.access_token = token_data["access_token"]
        self.refresh_token = token_data.get("refresh_token")
        self.token_expiry = time.time() + token_data.get("expires_in", 3600) - 60  # 60s buffer

    def _refresh_token(self):
        if not self.refresh_token:
            self._get_token()
            return
        url = f"{self.base_url}/auth/token"
        data = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        resp = requests.post(url, data=data)
        resp.raise_for_status()
        token_data = resp.json()
        self.access_token = token_data["access_token"]
        self.refresh_token = token_data.get("refresh_token")
        self.token_expiry = time.time() + token_data.get("expires_in", 3600) - 60

    def _ensure_token(self):
        if not self.access_token or time.time() > self.token_expiry:
            if self.refresh_token:
                self._refresh_token()
            else:
                self._get_token()

    def _headers(self) -> Dict[str, str]:
        self._ensure_token()
        return {"Authorization": f"Bearer {self.access_token}"}

    def list_devices(self) -> Any:
        url = f"{self.base_url}/devices"
        resp = requests.get(url, headers=self._headers())
        resp.raise_for_status()
        return resp.json()

    def get_device_info(self, device_id: str) -> Any:
        url = f"{self.base_url}/devices/{device_id}"
        resp = requests.get(url, headers=self._headers())
        resp.raise_for_status()
        return resp.json()

    def get_realtime_loc(self, device_id: str) -> Any:
        url = f"{self.base_url}/devices/{device_id}/realtime"
        resp = requests.get(url, headers=self._headers())
        resp.raise_for_status()
        return resp.json()

    def list_trips(self, device_id: str) -> Any:
        url = f"{self.base_url}/devices/{device_id}/trips"
        resp = requests.get(url, headers=self._headers())
        resp.raise_for_status()
        return resp.json()

    def list_alarms(self, device_id: str) -> Any:
        url = f"{self.base_url}/devices/{device_id}/alarms"
        resp = requests.get(url, headers=self._headers())
        resp.raise_for_status()
        return resp.json() 