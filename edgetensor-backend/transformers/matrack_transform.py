from datetime import datetime
from typing import Optional

# Example SQLAlchemy ORM models (replace with your actual models)
class DeviceORM:
    def __init__(self, device_id, name, license_plate, imei):
        self.device_id = device_id
        self.name = name
        self.license_plate = license_plate
        self.imei = imei

class RealTimeLocationORM:
    def __init__(self, device_id, timestamp, lat, lng, speed, heading, ignition_status):
        self.device_id = device_id
        self.timestamp = timestamp
        self.lat = lat
        self.lng = lng
        self.speed = speed
        self.heading = heading
        self.ignition_status = ignition_status

class TripORM:
    def __init__(self, trip_id, device_id, start_time, end_time, start_lat, start_lng, end_lat, end_lng, distance):
        self.trip_id = trip_id
        self.device_id = device_id
        self.start_time = start_time
        self.end_time = end_time
        self.start_lat = start_lat
        self.start_lng = start_lng
        self.end_lat = end_lat
        self.end_lng = end_lng
        self.distance = distance

class AlarmORM:
    def __init__(self, alarm_id, device_id, timestamp, alarm_type, lat, lng, media_url):
        self.alarm_id = alarm_id
        self.device_id = device_id
        self.timestamp = timestamp
        self.alarm_type = alarm_type
        self.lat = lat
        self.lng = lng
        self.media_url = media_url

# --- Transformers ---
def parse_timestamp(ts: Optional[str]) -> Optional[datetime]:
    if not ts:
        return None
    try:
        return datetime.fromisoformat(ts)
    except Exception:
        return None

def kmh_to_ms(speed_kmh: Optional[float]) -> Optional[float]:
    if speed_kmh is None:
        return None
    return speed_kmh * 1000 / 3600

def device_data_to_orm(device_data):
    return DeviceORM(
        device_id=device_data.device_id,
        name=getattr(device_data, 'name', None),
        license_plate=getattr(device_data, 'license_plate', None),
        imei=getattr(device_data, 'imei', None)
    )

def realtime_loc_data_to_orm(loc_data, device_id):
    return RealTimeLocationORM(
        device_id=device_id,
        timestamp=parse_timestamp(getattr(loc_data, 'timestamp', None)),
        lat=getattr(loc_data, 'latitude', None),
        lng=getattr(loc_data, 'longitude', None),
        speed=kmh_to_ms(getattr(loc_data, 'speed', None)),
        heading=getattr(loc_data, 'heading', None),
        ignition_status=getattr(loc_data, 'ignition_status', None)
    )

def trip_data_to_orm(trip_data, device_id):
    return TripORM(
        trip_id=trip_data.trip_id,
        device_id=device_id,
        start_time=parse_timestamp(getattr(trip_data, 'start_time', None)),
        end_time=parse_timestamp(getattr(trip_data, 'end_time', None)),
        start_lat=getattr(trip_data, 'start_lat', None),
        start_lng=getattr(trip_data, 'start_lng', None),
        end_lat=getattr(trip_data, 'end_lat', None),
        end_lng=getattr(trip_data, 'end_lng', None),
        distance=getattr(trip_data, 'distance', None)
    )

def alarm_data_to_orm(alarm_data, device_id):
    return AlarmORM(
        alarm_id=alarm_data.alarm_id,
        device_id=device_id,
        timestamp=parse_timestamp(getattr(alarm_data, 'timestamp', None)),
        alarm_type=getattr(alarm_data, 'alarm_type', None),
        lat=getattr(alarm_data, 'latitude', None),
        lng=getattr(alarm_data, 'longitude', None),
        media_url=getattr(alarm_data, 'media_url', None)
    ) 