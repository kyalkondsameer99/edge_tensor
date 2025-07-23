from celery import Celery
from services.matrack_service import client
import datetime

# Configure Celery (adjust broker and backend as needed)
celery_app = Celery(
    'matrack_ingest',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

@celery_app.task
def fetch_and_store_realtime():
    """Fetch real-time locations for all devices every minute and save to DB."""
    devices = client.list_devices().get('data', [])
    for device in devices:
        device_id = device.get('device_id')
        if device_id:
            loc = client.get_realtime_loc(device_id)
            # TODO: Save loc to DB (implement your DB logic here)
            print(f"Saved realtime location for device {device_id}: {loc}")

@celery_app.task
def sync_historical():
    """Sync trips and alarms for all devices daily and upsert into DB."""
    devices = client.list_devices().get('data', [])
    for device in devices:
        device_id = device.get('device_id')
        if device_id:
            trips = client.list_trips(device_id)
            alarms = client.list_alarms(device_id)
            # TODO: Upsert trips and alarms into DB (implement your DB logic here)
            print(f"Upserted trips for device {device_id}: {trips}")
            print(f"Upserted alarms for device {device_id}: {alarms}")

# Example periodic task registration (if using Celery beat)
from celery.schedules import crontab

celery_app.conf.beat_schedule = {
    'fetch-and-store-realtime-every-minute': {
        'task': 'tasks.matrack_ingest.fetch_and_store_realtime',
        'schedule': crontab(),  # every minute
    },
    'sync-historical-daily': {
        'task': 'tasks.matrack_ingest.sync_historical',
        'schedule': crontab(hour=0, minute=0),  # every day at midnight
    },
} 