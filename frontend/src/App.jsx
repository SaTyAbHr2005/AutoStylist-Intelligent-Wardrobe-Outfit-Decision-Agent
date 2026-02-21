import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import Home from './pages/Home';
import Upload from './pages/Upload';
import Recommendations from './pages/Recommendations';
import WardrobeMgmt from './pages/WardrobeMgmt';
import Login from './pages/Login';
import Register from './pages/Register';
import Profile from './pages/Profile';
import './App.css';

function App() {
  return (
    <Router>
      <div className="app">
        <Header />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/upload" element={<Upload />} />
            <Route path="/recommendations" element={<Recommendations />} />
            <Route path="/wardrobe" element={<WardrobeMgmt />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/profile" element={<Profile />} />
          </Routes>
        </main>
        <footer className="footer">
          <p>&copy; 2026 AutoStylist. Intelligent Wardrobe & Outfit Decision Agent.</p>
        </footer>
      </div>
    </Router>
  );
}

export default App;
