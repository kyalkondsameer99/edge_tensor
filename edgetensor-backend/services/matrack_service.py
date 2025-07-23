from matrack_client import MatrackClient
from typing import Any

# Configure your Matrack API credentials
CLIENT_ID = "your_client_id"
CLIENT_SECRET = "your_client_secret"
BASE_URL = "https://api.matrack.live/v1"

client = MatrackClient(CLIENT_ID, CLIENT_SECRET, BASE_URL)

def sync_devices() -> Any:
    """Fetch and return the list of devices from Matrack API."""
    return client.list_devices()

def sync_realtime_locations() -> Any:
    """Fetch and return real-time locations for all devices."""
    devices = client.list_devices().get('data', [])
    locations = []
    for device in devices:
        device_id = device.get('device_id')
        if device_id:
            loc = client.get_realtime_loc(device_id)
            locations.append({"device_id": device_id, "location": loc})
    return locations

def sync_trips() -> Any:
    """Fetch and return trips for all devices."""
    devices = client.list_devices().get('data', [])
    trips = []
    for device in devices:
        device_id = device.get('device_id')
        if device_id:
            trip = client.list_trips(device_id)
            trips.append({"device_id": device_id, "trips": trip})
    return trips

def sync_alarms() -> Any:
    """Fetch and return alarms for all devices."""
    devices = client.list_devices().get('data', [])
    alarms = []
    for device in devices:
        device_id = device.get('device_id')
        if device_id:
            alarm = client.list_alarms(device_id)
            alarms.append({"device_id": device_id, "alarms": alarm})
    return alarms 