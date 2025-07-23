-- Devices table
CREATE TABLE devices (
    device_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    license_plate TEXT,
    imei TEXT UNIQUE,
    -- Add other static fields as needed
    UNIQUE(imei)
);

-- Real-time locations table
CREATE TABLE realtime_locations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_id TEXT NOT NULL,
    timestamp DATETIME NOT NULL,
    lat REAL NOT NULL,
    lng REAL NOT NULL,
    speed REAL,
    heading REAL,
    ignition_status INTEGER,
    -- Add other fields as needed
    FOREIGN KEY (device_id) REFERENCES devices(device_id) ON DELETE CASCADE,
    INDEX idx_realtime_device_time (device_id, timestamp)
);

-- Trips table
CREATE TABLE trips (
    trip_id TEXT PRIMARY KEY,
    device_id TEXT NOT NULL,
    start_time DATETIME NOT NULL,
    end_time DATETIME NOT NULL,
    start_lat REAL NOT NULL,
    start_lng REAL NOT NULL,
    end_lat REAL NOT NULL,
    end_lng REAL NOT NULL,
    distance REAL,
    FOREIGN KEY (device_id) REFERENCES devices(device_id) ON DELETE CASCADE,
    INDEX idx_trips_device_time (device_id, start_time, end_time)
);

-- Alarms table
CREATE TABLE alarms (
    alarm_id TEXT PRIMARY KEY,
    device_id TEXT NOT NULL,
    timestamp DATETIME NOT NULL,
    type TEXT NOT NULL,
    lat REAL NOT NULL,
    lng REAL NOT NULL,
    media_url TEXT,
    FOREIGN KEY (device_id) REFERENCES devices(device_id) ON DELETE CASCADE,
    INDEX idx_alarms_device_time (device_id, timestamp)
); 