-- Devices table
CREATE TABLE devices (
    device_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    license_plate VARCHAR(64),
    imei VARCHAR(32) UNIQUE NOT NULL,
    model VARCHAR(128),
    install_date DATE,
    status VARCHAR(32),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Real-time locations table
CREATE TABLE realtime_locations (
    id SERIAL PRIMARY KEY,
    device_id INTEGER NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    lat DOUBLE PRECISION NOT NULL,
    lng DOUBLE PRECISION NOT NULL,
    speed DOUBLE PRECISION,
    heading VARCHAR(32),
    ignition_status BOOLEAN,
    -- Add more fields as needed
    FOREIGN KEY (device_id) REFERENCES devices(device_id) ON DELETE CASCADE
);
CREATE INDEX idx_realtime_locations_device_time ON realtime_locations(device_id, timestamp DESC);

-- Trips table
CREATE TABLE trips (
    trip_id SERIAL PRIMARY KEY,
    device_id INTEGER NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP,
    start_lat DOUBLE PRECISION,
    start_lng DOUBLE PRECISION,
    end_lat DOUBLE PRECISION,
    end_lng DOUBLE PRECISION,
    distance DOUBLE PRECISION,
    FOREIGN KEY (device_id) REFERENCES devices(device_id) ON DELETE CASCADE
);
CREATE INDEX idx_trips_device_time ON trips(device_id, start_time DESC);

-- Alarms table
CREATE TABLE alarms (
    alarm_id SERIAL PRIMARY KEY,
    device_id INTEGER NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    type VARCHAR(64) NOT NULL,
    lat DOUBLE PRECISION,
    lng DOUBLE PRECISION,
    media_url TEXT,
    FOREIGN KEY (device_id) REFERENCES devices(device_id) ON DELETE CASCADE
);
CREATE INDEX idx_alarms_device_time ON alarms(device_id, timestamp DESC); 