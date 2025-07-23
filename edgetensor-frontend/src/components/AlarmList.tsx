import React, { useState } from 'react';
import { toast } from 'react-toastify';

interface Alarm {
  alarm_id: string;
  device_id: string;
  timestamp: string;
  type: string;
  lat: number;
  lng: number;
  media_url?: string;
}

interface AlarmListProps {
  alarms: Alarm[];
}

const Spinner = () => (
  <div style={{ textAlign: 'center', padding: 16 }}>
    <div className="spinner" style={{ width: 30, height: 30, border: '4px solid #ccc', borderTop: '4px solid #333', borderRadius: '50%', animation: 'spin 1s linear infinite', margin: '0 auto' }} />
    <style>{`@keyframes spin { 100% { transform: rotate(360deg); } }`}</style>
  </div>
);

const AlarmList: React.FC<AlarmListProps> = ({ alarms }) => {
  const [mediaUrl, setMediaUrl] = useState<string | null>(null);
  const [mediaType, setMediaType] = useState<'video' | 'image' | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleRowClick = async (alarm: Alarm) => {
    if (!alarm.media_url || loading) return;
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`/dashcamAlertFiles/getSignedUrl?filePath=${encodeURIComponent(alarm.media_url)}`);
      if (!res.ok) throw new Error('Failed to fetch media URL');
      const data = await res.json();
      setMediaUrl(data.signedUrl);
      // Guess media type from file extension
      if (alarm.media_url.match(/\.(mp4|mov)$/i)) {
        setMediaType('video');
      } else if (alarm.media_url.match(/\.(jpg|jpeg|png|gif)$/i)) {
        setMediaType('image');
      } else {
        setMediaType(null);
      }
      toast.success('Media loaded');
    } catch (e) {
      setMediaUrl(null);
      setMediaType(null);
      setError('Could not load media.');
      toast.error('Could not load media.');
    }
    setLoading(false);
  };

  return (
    <div>
      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr>
            <th>Timestamp</th>
            <th>Type</th>
            <th>Location</th>
            <th>Media</th>
          </tr>
        </thead>
        <tbody>
          {alarms.map((alarm, i) => (
            <tr key={i} style={{ cursor: alarm.media_url && !loading ? 'pointer' : 'default', opacity: loading ? 0.5 : 1 }} onClick={() => handleRowClick(alarm)}>
              <td>{alarm.timestamp}</td>
              <td>{alarm.type}</td>
              <td>{alarm.lat}, {alarm.lng}</td>
              <td>{alarm.media_url ? 'View' : '-'}</td>
            </tr>
          ))}
        </tbody>
      </table>
      {loading && <Spinner />}
      {error && <div style={{ color: 'red', marginTop: 8 }}>{error}</div>}
      {mediaUrl && mediaType === 'video' && (
        <div style={{ marginTop: 16 }}>
          <video src={mediaUrl} controls style={{ maxWidth: '100%' }} />
        </div>
      )}
      {mediaUrl && mediaType === 'image' && (
        <div style={{ marginTop: 16 }}>
          <img src={mediaUrl} alt="Alarm media" style={{ maxWidth: '100%' }} />
        </div>
      )}
    </div>
  );
};

export default AlarmList; 