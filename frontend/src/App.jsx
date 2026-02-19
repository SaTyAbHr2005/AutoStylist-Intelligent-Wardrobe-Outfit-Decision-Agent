import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import Home from './pages/Home';
import Upload from './pages/Upload';
import Recommendations from './pages/Recommendations';
import WardrobeMgmt from './pages/WardrobeMgmt';
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
