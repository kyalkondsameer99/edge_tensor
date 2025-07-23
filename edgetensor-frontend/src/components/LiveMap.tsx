import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { useAppDispatch, useAppSelector } from '../store';
import { fetchDevices, setSelectedDevice } from '../store/deviceSlice';
import { toast } from 'react-toastify';

// Fix default icon issue with Leaflet in React
import iconUrl from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';

const DefaultIcon = L.icon({
  iconUrl,
  shadowUrl: iconShadow,
  iconAnchor: [12, 41],
});
L.Marker.prototype.options.icon = DefaultIcon;

const API_BASE = '/api/v2.0/devices/matrack';

const Spinner = () => (
  <div style={{ textAlign: 'center', padding: 32 }}>
    <div className="spinner" style={{ width: 40, height: 40, border: '4px solid #ccc', borderTop: '4px solid #333', borderRadius: '50%', animation: 'spin 1s linear infinite', margin: '0 auto' }} />
    <style>{`@keyframes spin { 100% { transform: rotate(360deg); } }`}</style>
  </div>
);

const LiveMap: React.FC = () => {
  const dispatch = useAppDispatch();
  const devices = useAppSelector((state) => state.devices.devices);
  const selected = useAppSelector((state) => state.devices.selectedDevice);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Poll devices every 30 seconds
  useEffect(() => {
    const fetchAll = async () => {
      setLoading(true);
      setError(null);
      try {
        await dispatch(fetchDevices()).unwrap();
        toast.success('Devices loaded');
      } catch (e) {
        setError('Failed to load devices. Please try again.');
        toast.error('Failed to load devices.');
      } finally {
        setLoading(false);
      }
    };
    fetchAll();
    const interval = setInterval(fetchAll, 30000);
    return () => clearInterval(interval);
  }, [dispatch]);

  // Center map on first device or default
  const center = devices.length > 0 && devices[0].lat && devices[0].lng
    ? [devices[0].lat, devices[0].lng]
    : [37.7749, -122.4194];

  // Fetch latest location for selected device (local state)
  const [location, setLocation] = React.useState<any>(null);
  const [locLoading, setLocLoading] = useState(false);
  const [locError, setLocError] = useState<string | null>(null);
  useEffect(() => {
    if (!selected) return;
    const fetchLocation = async () => {
      setLocLoading(true);
      setLocError(null);
      try {
        const res = await fetch(`${API_BASE}/${selected}/location`);
        if (!res.ok) throw new Error('Failed to fetch location');
        const data = await res.json();
        setLocation(data);
        toast.success('Location loaded');
      } catch (e) {
        setLocError('Could not load location.');
        toast.error('Could not load location.');
      } finally {
        setLocLoading(false);
      }
    };
    fetchLocation();
  }, [selected]);

  if (loading) return <Spinner />;
  if (error) return <div style={{ color: 'red', textAlign: 'center', margin: 32 }}>{error}</div>;

  return (
    <MapContainer center={center as [number, number]} zoom={6} style={{ height: '80vh', width: '100%' }} scrollWheelZoom={!loading && !error} dragging={!loading && !error}>
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution="&copy; OpenStreetMap contributors"
      />
      {devices.map((device) => (
        device.lat && device.lng && (
          <Marker
            key={device.device_id}
            position={[device.lat, device.lng]}
            eventHandlers={{
              click: () => dispatch(setSelectedDevice(device.device_id)),
            }}
          >
            {selected === device.device_id && (
              <Popup onClose={() => dispatch(setSelectedDevice(null))}>
                {locLoading ? <Spinner /> : locError ? <div style={{ color: 'red' }}>{locError}</div> : location && (
                  <div>
                    <strong>Device:</strong> {location.device_id}<br />
                    <strong>Lat:</strong> {location.lat}<br />
                    <strong>Lng:</strong> {location.lng}<br />
                    <strong>Speed:</strong> {location.speed ?? '-'} km/h<br />
                    <strong>Heading:</strong> {location.heading ?? '-'}<br />
                    <strong>Ignition:</strong> {location.ignition_status ?? '-'}<br />
                    <strong>Timestamp:</strong> {location.timestamp}
                  </div>
                )}
              </Popup>
            )}
          </Marker>
        )
      ))}
    </MapContainer>
  );
};

export default LiveMap; 