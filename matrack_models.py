from pydantic import BaseModel
from typing import List, Optional

class DeviceData(BaseModel):
    device_id: str
    name: Optional[str]
    license_plate: Optional[str]
    imei: Optional[str]
    # Add other static fields as needed

class DeviceListResponse(BaseModel):
    status: bool
    message: str
    data: List[DeviceData]

class DeviceInfoData(BaseModel):
    device_id: str
    name: Optional[str]
    license_plate: Optional[str]
    imei: Optional[str]
    # Add other fields as needed

class DeviceInfoResponse(BaseModel):
    status: bool
    message: str
    data: DeviceInfoData

class RealTimeLocData(BaseModel):
    device_id: str
    latitude: float
    longitude: float
    timestamp: str
    speed: Optional[float]
    heading: Optional[float]
    ignition_status: Optional[int]
    # Add other fields as needed

class RealTimeLocResponse(BaseModel):
    status: bool
    message: str
    data: Optional[RealTimeLocData]

class TripData(BaseModel):
    trip_id: str
    start_time: str
    end_time: str
    start_lat: float
    start_lng: float
    end_lat: float
    end_lng: float
    distance: float
    # Add other fields as needed

class TripListResponse(BaseModel):
    status: bool
    message: str
    data: List[TripData]

class AlarmData(BaseModel):
    alarm_id: str
    timestamp: str
    alarm_type: str
    latitude: float
    longitude: float
    media_url: Optional[str]
    # Add other fields as needed

class AlarmListResponse(BaseModel):
    status: bool
    message: str
    data: List[AlarmData] 