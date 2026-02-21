import { Link, useNavigate } from 'react-router-dom';
import { useEffect, useState, useRef } from 'react';
import '../styles/Header.css';
import { getMe, logoutUser, setAuthToken } from '../services/api';

export default function Header() {
  const [user, setUser] = useState(null);
  const [menuOpen, setMenuOpen] = useState(false);
  const navigate = useNavigate();
  const menuRef = useRef();

  const fetchUser = () => {
    const token = localStorage.getItem('token');
    if (token) {
      setAuthToken(token);
      getMe()
        .then((u) => setUser(u))
        .catch(() => {
          localStorage.removeItem('token');
          setAuthToken(null);
          setUser(null);
        });
    } else {
      setUser(null);
    }
  };

  useEffect(() => {
    fetchUser();
    window.addEventListener('authChange', fetchUser);

    const onDocClick = (e) => {
      if (menuRef.current && !menuRef.current.contains(e.target)) setMenuOpen(false);
    };
    document.addEventListener('click', onDocClick);
    return () => {
      document.removeEventListener('click', onDocClick);
      window.removeEventListener('authChange', fetchUser);
    }
  }, []);

  const handleLogout = async () => {
    try {
      await logoutUser();
    } catch (e) {
      // ignore server error during logout
    }
    localStorage.removeItem('token');
    setAuthToken(null);
    setUser(null);
    window.dispatchEvent(new Event('authChange'));
    navigate('/login');
  };

  const initials = user?.full_name ? user.full_name.split(' ').map(n => n[0]).slice(0, 2).join('') : 'AU';

  return (
    <header className="header">
      <div className="header-container">
        <Link to="/" className="logo">
          <h1>✨ AutoStylist</h1>
        </Link>
        <nav className="nav-menu">
          <Link to="/" className="nav-link">Home</Link>
          <Link to="/wardrobe" className="nav-link">My Wardrobe</Link>
          <Link to="/upload" className="nav-link">Upload Item</Link>
          <Link to="/recommendations" className="nav-link">Get Recommendations</Link>
        </nav>

        <div className="profile-area" ref={menuRef}>
          {user ? (
            <div className="profile-wrapper">
              <button className="profile-btn" onClick={() => setMenuOpen(s => !s)} aria-label="Profile menu">
                <div className="profile-icon">{initials}</div>
              </button>
              {menuOpen && (
                <div className="profile-menu">
                  <Link to="/profile" className="profile-menu-item" onClick={() => setMenuOpen(false)}>View Profile</Link>
                  <button className="profile-menu-item" onClick={handleLogout}>Logout</button>
                </div>
              )}
            </div>
          ) : (
            <div className="auth-links">
              <Link to="/login" className="nav-link">Log in</Link>
              <Link to="/register" className="nav-link">Register</Link>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}
