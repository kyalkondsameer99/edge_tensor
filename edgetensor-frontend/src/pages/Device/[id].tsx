import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { toast } from 'react-toastify';

interface Location {
  id: number;
  device_id: string;
  timestamp: string;
  lat: number;
  lng: number;
  speed?: number;
  heading?: number;
  ignition_status?: number;
}

interface Trip {
  trip_id: string;
  device_id: string;
  start_time: string;
  end_time: string;
  start_lat: number;
  start_lng: number;
  end_lat: number;
  end_lng: number;
  distance: number;
}

interface Alarm {
  alarm_id: string;
  device_id: string;
  timestamp: string;
  type: string;
  lat: number;
  lng: number;
  media_url?: string;
}

const API_BASE = '/api/v2.0/devices/matrack';

const Spinner = () => (
  <div style={{ textAlign: 'center', padding: 32 }}>
    <div className="spinner" style={{ width: 40, height: 40, border: '4px solid #ccc', borderTop: '4px solid #333', borderRadius: '50%', animation: 'spin 1s linear infinite', margin: '0 auto' }} />
    <style>{`@keyframes spin { 100% { transform: rotate(360deg); } }`}</style>
  </div>
);

const DevicePage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [location, setLocation] = useState<Location | null>(null);
  const [locLoading, setLocLoading] = useState(false);
  const [locError, setLocError] = useState<string | null>(null);
  const [tab, setTab] = useState<'trips' | 'alarms'>('trips');
  const [trips, setTrips] = useState<Trip[]>([]);
  const [tripsLoading, setTripsLoading] = useState(false);
  const [tripsError, setTripsError] = useState<string | null>(null);
  const [alarms, setAlarms] = useState<Alarm[]>([]);
  const [alarmsLoading, setAlarmsLoading] = useState(false);
  const [alarmsError, setAlarmsError] = useState<string | null>(null);

  useEffect(() => {
    setLocLoading(true);
    setLocError(null);
    const fetchLocation = async () => {
      try {
        const res = await fetch(`${API_BASE}/${id}/location`);
        if (!res.ok) throw new Error('Failed to fetch location');
        const data = await res.json();
        setLocation(data);
        toast.success('Device status loaded');
      } catch (e) {
        setLocError('Could not load current status.');
        toast.error('Could not load current status.');
      } finally {
        setLocLoading(false);
      }
    };
    fetchLocation();
  }, [id]);

  useEffect(() => {
    if (tab === 'trips') {
      setTripsLoading(true);
      setTripsError(null);
      const fetchTrips = async () => {
        try {
          const res = await fetch(`${API_BASE}/${id}/trips`);
          if (!res.ok) throw new Error('Failed to fetch trips');
          const data = await res.json();
          setTrips(data);
          toast.success('Trips loaded');
        } catch (e) {
          setTripsError('Could not load trips.');
          toast.error('Could not load trips.');
        } finally {
          setTripsLoading(false);
        }
      };
      fetchTrips();
    } else {
      setAlarmsLoading(true);
      setAlarmsError(null);
      const fetchAlarms = async () => {
        try {
          const res = await fetch(`${API_BASE}/${id}/alarms`);
          if (!res.ok) throw new Error('Failed to fetch alarms');
          const data = await res.json();
          setAlarms(data);
          toast.success('Alarms loaded');
        } catch (e) {
          setAlarmsError('Could not load alarms.');
          toast.error('Could not load alarms.');
        } finally {
          setAlarmsLoading(false);
        }
      };
      fetchAlarms();
    }
  }, [id, tab]);

  return (
    <div style={{ maxWidth: 800, margin: '0 auto', padding: 24 }}>
      <h2>Device: {id}</h2>
      {locLoading ? <Spinner /> : locError ? <div style={{ color: 'red' }}>{locError}</div> : location ? (
        <div style={{ marginBottom: 24 }}>
          <strong>Speed:</strong> {location.speed ?? '-'} km/h<br />
          <strong>Status:</strong> {location.ignition_status ?? '-'}<br />
          <strong>Last updated:</strong> {location.timestamp}
        </div>
      ) : (
        <div>Loading current status...</div>
      )}
      <div style={{ display: 'flex', gap: 16, marginBottom: 16 }}>
        <button onClick={() => setTab('trips')} style={{ fontWeight: tab === 'trips' ? 'bold' : 'normal' }} disabled={tripsLoading || alarmsLoading}>Trips</button>
        <button onClick={() => setTab('alarms')} style={{ fontWeight: tab === 'alarms' ? 'bold' : 'normal' }} disabled={tripsLoading || alarmsLoading}>Alarms</button>
      </div>
      <div>
        {tab === 'trips' ? (
          tripsLoading ? <Spinner /> : tripsError ? <div style={{ color: 'red' }}>{tripsError}</div> : (
            <div>
              <h3>Trips</h3>
              <ul>
                {trips.map((trip, i) => (
                  <li key={i}>
                    <strong>{trip.trip_id}</strong> {trip.start_time} → {trip.end_time} | {trip.distance} km
                  </li>
                ))}
              </ul>
            </div>
          )
        ) : (
          alarmsLoading ? <Spinner /> : alarmsError ? <div style={{ color: 'red' }}>{alarmsError}</div> : (
            <div>
              <h3>Alarms</h3>
              <ul>
                {alarms.map((alarm, i) => (
                  <li key={i}>
                    <strong>{alarm.type}</strong> at {alarm.timestamp} ({alarm.lat}, {alarm.lng})
                  </li>
                ))}
              </ul>
            </div>
          )
        )}
      </div>
    </div>
  );
};

export default DevicePage; 