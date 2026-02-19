import { Link } from 'react-router-dom';
import '../styles/Header.css';

export default function Header() {
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
      </div>
    </header>
  );
}
