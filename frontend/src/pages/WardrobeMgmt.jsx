import { useState, useEffect } from 'react';
import '../styles/WardrobeMgmt.css';

export default function WardrobeMgmt() {
  const [wardrobe, setWardrobe] = useState([]);
  const [filteredWardrobe, setFilteredWardrobe] = useState([]);
  const [filter, setFilter] = useState('all');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const categories = ['all', 'top', 'bottom', 'shoes', 'accessories', 'jewellery'];

  useEffect(() => {
    // In a real app, you'd fetch from backend
    // For now, showing placeholder UI
    loadWardrobe();
  }, []);

  useEffect(() => {
    if (filter === 'all') {
      setFilteredWardrobe(wardrobe);
    } else {
      setFilteredWardrobe(wardrobe.filter((item) => item.category === filter));
    }
  }, [filter, wardrobe]);

  const loadWardrobe = () => {
    // This would be an API call in a complete implementation
    setLoading(false);
    // Placeholder data
    setWardrobe([]);
  };

  return (
    <div className="wardrobe-page">
      <div className="wardrobe-container">
        <div className="wardrobe-header">
          <h1>👕 My Wardrobe</h1>
          <p>Manage and organize your clothing collection</p>
        </div>

        <div className="wardrobe-stats">
          <div className="stat-card">
            <div className="stat-number">{wardrobe.length}</div>
            <div className="stat-label">Total Items</div>
          </div>
          <div className="stat-card">
            <div className="stat-number">{wardrobe.filter((i) => i.category === 'top').length}</div>
            <div className="stat-label">Tops</div>
          </div>
          <div className="stat-card">
            <div className="stat-number">{wardrobe.filter((i) => i.category === 'bottom').length}</div>
            <div className="stat-label">Bottoms</div>
          </div>
          <div className="stat-card">
            <div className="stat-number">{wardrobe.filter((i) => i.category === 'shoes').length}</div>
            <div className="stat-label">Shoes</div>
          </div>
        </div>

        <div className="filter-section">
          <h2>Filter by Category</h2>
          <div className="filter-buttons">
            {categories.map((cat) => (
              <button
                key={cat}
                className={`filter-btn ${filter === cat ? 'active' : ''}`}
                onClick={() => setFilter(cat)}
              >
                {cat.charAt(0).toUpperCase() + cat.slice(1)}
              </button>
            ))}
          </div>
        </div>

        {error && <div className="alert alert-error">{error}</div>}

        <div className="wardrobe-grid">
          {loading ? (
            <div className="loading">
              <p>Loading wardrobe...</p>
            </div>
          ) : filteredWardrobe.length > 0 ? (
            filteredWardrobe.map((item) => (
              <div key={item._id} className="wardrobe-item-card">
                <div className="item-image">
                  <img
                    src={`http://localhost:8000/static/${item.image_path}`}
                    alt={item.category}
                    onError={(e) => {
                      e.target.src = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="200" height="200"%3E%3Crect fill="%23ccc" width="200" height="200"/%3E%3C/svg%3E';
                    }}
                  />
                </div>
                <div className="item-info">
                  <h3>{item.category}</h3>
                  <p>
                    <strong>Style:</strong> {item.style}
                  </p>
                  <p>
                    <strong>Usage:</strong> {item.usage_count} times
                  </p>
                  <p>
                    <strong>Preference:</strong> {item.preference_score}
                  </p>
                  <div className="item-colors">
                    {item.colors?.map((color, idx) => (
                      <div
                        key={idx}
                        className="color-indicator"
                        style={{ backgroundColor: color }}
                        title={color}
                      />
                    ))}
                  </div>
                </div>
              </div>
            ))
          ) : (
            <div className="empty-state">
              <p>📭 No items in this category</p>
              <p className="empty-hint">Upload items to build your wardrobe</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
