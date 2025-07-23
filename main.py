from fastapi import FastAPI, Depends, Query, Header, HTTPException
from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime, ForeignKey, desc
from sqlalchemy.orm import sessionmaker, declarative_base, Session, relationship
from typing import List
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
API_KEY = os.getenv("API_KEY", "your-production-api-key")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Device(Base):
    __tablename__ = "devices"
    device_id = Column(String, primary_key=True, index=True)
    name = Column(String)
    license_plate = Column(String)
    imei = Column(String)
    # Add other fields as needed

class RealTimeLocation(Base):
    __tablename__ = "realtime_locations"
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, ForeignKey("devices.device_id"), index=True)
    timestamp = Column(DateTime, index=True)
    lat = Column(Float)
    lng = Column(Float)
    speed = Column(Float)
    heading = Column(Float)
    ignition_status = Column(Integer)
    # Add other fields as needed

class Trip(Base):
    __tablename__ = "trips"
    trip_id = Column(String, primary_key=True, index=True)
    device_id = Column(String, ForeignKey("devices.device_id"), index=True)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    start_lat = Column(Float)
    start_lng = Column(Float)
    end_lat = Column(Float)
    end_lng = Column(Float)
    distance = Column(Float)
    # Add other fields as needed

class Alarm(Base):
    __tablename__ = "alarms"
    alarm_id = Column(String, primary_key=True, index=True)
    device_id = Column(String, ForeignKey("devices.device_id"), index=True)
    timestamp = Column(DateTime, index=True)
    type = Column(String)
    lat = Column(Float)
    lng = Column(Float)
    media_url = Column(String)
    # Add other fields as needed

app = FastAPI()

# Allow all origins for local development (adjust in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

# Example: protect all endpoints with API key
def api_key_dependency():
    return Depends(verify_api_key)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/api/v2.0/devices/matrack")
def get_devices(db: Session = Depends(get_db), api_key=Depends(verify_api_key)):
    devices = db.query(Device).all()
    return [
        {
            "device_id": d.device_id,
            "name": d.name,
            "license_plate": d.license_plate,
            "imei": d.imei
        }
        for d in devices
    ]

@app.get("/api/v2.0/devices/matrack/{device_id}/location")
def get_latest_location(device_id: str, db: Session = Depends(get_db), api_key=Depends(verify_api_key)):
    loc = db.query(RealTimeLocation).filter_by(device_id=device_id).order_by(desc(RealTimeLocation.timestamp)).first()
    if not loc:
        return {"error": "No location found for this device"}
    return {
        "id": loc.id,
        "device_id": loc.device_id,
        "timestamp": loc.timestamp,
        "lat": loc.lat,
        "lng": loc.lng,
        "speed": loc.speed,
        "heading": loc.heading,
        "ignition_status": loc.ignition_status
    }

@app.get("/api/v2.0/devices/matrack/{device_id}/history")
def get_location_history(
    device_id: str,
    start_time: str = Query(...),
    end_time: str = Query(...),
    db: Session = Depends(get_db),
    api_key=Depends(verify_api_key)
):
    # Parse the start and end times
    try:
        start_dt = datetime.fromisoformat(start_time)
        end_dt = datetime.fromisoformat(end_time)
    except Exception:
        return {"error": "Invalid date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)"}
    locations = db.query(RealTimeLocation).filter(
        RealTimeLocation.device_id == device_id,
        RealTimeLocation.timestamp >= start_dt,
        RealTimeLocation.timestamp <= end_dt
    ).order_by(RealTimeLocation.timestamp).all()
    return [
        {
            "id": loc.id,
            "device_id": loc.device_id,
            "timestamp": loc.timestamp,
            "lat": loc.lat,
            "lng": loc.lng,
            "speed": loc.speed,
            "heading": loc.heading,
            "ignition_status": loc.ignition_status
        }
        for loc in locations
    ]

@app.get("/api/v2.0/devices/matrack/{device_id}/trips")
def get_trips(device_id: str, db: Session = Depends(get_db), api_key=Depends(verify_api_key)):
    trips = db.query(Trip).filter_by(device_id=device_id).order_by(Trip.start_time).all()
    return [
        {
            "trip_id": t.trip_id,
            "device_id": t.device_id,
            "start_time": t.start_time,
            "end_time": t.end_time,
            "start_lat": t.start_lat,
            "start_lng": t.start_lng,
            "end_lat": t.end_lat,
            "end_lng": t.end_lng,
            "distance": t.distance
        }
        for t in trips
    ]

@app.get("/api/v2.0/devices/matrack/{device_id}/alarms")
def get_alarms(device_id: str, db: Session = Depends(get_db), api_key=Depends(verify_api_key)):
    alarms = db.query(Alarm).filter_by(device_id=device_id).order_by(Alarm.timestamp).all()
    return [
        {
            "alarm_id": a.alarm_id,
            "device_id": a.device_id,
            "timestamp": a.timestamp,
            "type": a.type,
            "lat": a.lat,
            "lng": a.lng,
            "media_url": a.media_url
        }
        for a in alarms
    ]

@app.get("/dashcamAlertFiles/getSignedUrl")
def get_signed_url(filePath: str = Query(...), api_key=Depends(verify_api_key)):
    # TODO: Replace with real signed URL logic (e.g., AWS S3, GCP, Azure)
    # For now, just return the filePath as a mock signed URL
    # In production, generate a time-limited signed URL for secure access
    return {"signedUrl": f"https://media.example.com/{filePath}?token=mock-signed-token"} 