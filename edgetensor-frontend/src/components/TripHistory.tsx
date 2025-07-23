import React, { useState } from 'react';
import { MapContainer, TileLayer, Polyline } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import { toast } from 'react-toastify';

interface TripPoint {
  lat: number;
  lng: number;
  timestamp: string;
}

interface TripHistoryProps {
  deviceId: string;
}

const API_BASE = '/api/v2.0/devices/matrack';

const Spinner = () => (
  <div style={{ textAlign: 'center', padding: 32 }}>
    <div className="spinner" style={{ width: 40, height: 40, border: '4px solid #ccc', borderTop: '4px solid #333', borderRadius: '50%', animation: 'spin 1s linear infinite', margin: '0 auto' }} />
    <style>{`@keyframes spin { 100% { transform: rotate(360deg); } }`}</style>
  </div>
);

const TripHistory: React.FC<TripHistoryProps> = ({ deviceId }) => {
  const [start, setStart] = useState('');
  const [end, setEnd] = useState('');
  const [trip, setTrip] = useState<TripPoint[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchHistory = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API_BASE}/${deviceId}/history?start_time=${encodeURIComponent(start)}&end_time=${encodeURIComponent(end)}`);
      if (!res.ok) throw new Error('Failed to fetch history');
      const data = await res.json();
      setTrip(data);
      toast.success('Trip history loaded');
    } catch (e) {
      setError('Could not load trip history.');
      toast.error('Could not load trip history.');
    } finally {
      setLoading(false);
    }
  };

  const polylinePositions = trip.map((p) => [p.lat, p.lng]) as [number, number][];
  const center = polylinePositions.length > 0 ? polylinePositions[0] : [37.7749, -122.4194];

  return (
    <div>
      <form onSubmit={fetchHistory} style={{ marginBottom: 16 }}>
        <label>
          Start date/time:
          <input type="datetime-local" value={start} onChange={e => setStart(e.target.value)} required disabled={loading} />
        </label>
        <label style={{ marginLeft: 8 }}>
          End date/time:
          <input type="datetime-local" value={end} onChange={e => setEnd(e.target.value)} required disabled={loading} />
        </label>
        <button type="submit" style={{ marginLeft: 8 }} disabled={loading}>Show History</button>
      </form>
      {loading && <Spinner />}
      {error && <div style={{ color: 'red', marginBottom: 8 }}>{error}</div>}
      <MapContainer center={center as [number, number]} zoom={10} style={{ height: '60vh', width: '100%' }}>
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution="&copy; OpenStreetMap contributors"
        />
        {polylinePositions.length > 1 && (
          <Polyline positions={polylinePositions} color="blue" />
        )}
      </MapContainer>
    </div>
  );
};

export default TripHistory; 