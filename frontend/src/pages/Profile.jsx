import { useEffect, useState } from 'react';
import { getMe } from '../services/api';
import '../styles/Upload.css';

export default function Profile() {
  const [user, setUser] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    getMe()
      .then(u => setUser(u))
      .catch(e => setError(e.detail || e.error || 'Failed to load profile'));
  }, []);

  if (error) return <div className="upload-page"><h2>Profile</h2><div className="error">{error}</div></div>;

  return (
    <div className="upload-page">
      <h2>Profile</h2>
      {user ? (
        <div className="profile-card">
          <p><strong>Name:</strong> {user.full_name}</p>
          <p><strong>Email:</strong> {user.email}</p>
          <p><strong>Member since:</strong> {new Date(user.created_at).toLocaleString()}</p>
        </div>
      ) : (
        <div>Loading...</div>
      )}
    </div>
  );
}
