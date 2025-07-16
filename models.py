from pydantic import BaseModel
from typing import List, Optional

class DeviceData(BaseModel):
    device: str
    date: str
    lat: float
    lng: float
    time: str
    speed: float
    battery: Optional[str]
    deviceAddedOn: Optional[str]
    packetType: Optional[str]
    gpsfix: Optional[str]
    dateTimeago: Optional[str]

class DeviceListResponse(BaseModel):
    status: bool
    message: str
    data: List[DeviceData]

class DeviceInfoData(BaseModel):
    id: str
    imei: str
    model: Optional[str]
    installDate: Optional[str]
    status: Optional[str]
    # Add more fields as needed

class DeviceInfoResponse(BaseModel):
    status: bool
    message: str
    data: DeviceInfoData

class RealTimeLocData(BaseModel):
    status: bool
    message: str
    lat: Optional[float]
    lng: Optional[float]
    speed: Optional[float]
    time: Optional[str]
    # Add more fields as needed

class RealTimeLocResponse(BaseModel):
    status: bool
    message: str
    data: Optional[RealTimeLocData]

class TripData(BaseModel):
    event: str
    eventCode: str
    date: str
    color: Optional[str]
    time: str
    lat: float
    lng: float
    gpsFix: Optional[str]
    satellite: Optional[int]
    speed: float
    mileage: float
    direction: Optional[str]

class TripListResponse(BaseModel):
    status: bool
    message: str
    data: List[TripData]

class AlarmData(BaseModel):
    utcDateTime: str
    lat: float
    lng: float
    eventName: str
    time: str
    speed: float
    battery: Optional[float]
    condition: Optional[str]
    timestamp: Optional[str]
    filePath: Optional[str]

class AlarmListResponse(BaseModel):
    status: bool
    message: str
    data: List[AlarmData] 