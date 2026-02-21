import { useState } from 'react';
import { getRecommendations } from '../services/api';
import OutfitRecommendation from '../components/OutfitRecommendation';
import '../styles/Recommendations.css';

export default function Recommendations() {
  const [occasion, setOccasion] = useState('casual');
  const [gender, setGender] = useState('male');
  const [recommendations, setRecommendations] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [context, setContext] = useState(null);

  const genders = [
    { value: 'male', label: '👨 Male' },
    { value: 'female', label: '👩 Female' },
  ];

  const occasions = [
    { value: 'casual', label: '👕 Casual', description: 'Everyday relaxed wear' },
    { value: 'office', label: '👔 Office', description: 'Professional formal wear' },
    { value: 'party', label: '🎉 Party', description: 'Festive and stylish looks' },
    { value: 'traditional', label: '👗 Traditional', description: 'Cultural attire' },
  ];

  const handleGetRecommendations = async () => {
    setLoading(true);
    setError('');
    setRecommendations(null);

    try {
      const data = await getRecommendations(occasion, gender);
      setRecommendations(data.recommendations);
      setContext(data.context);
    } catch (err) {
      setError(err.error || 'Failed to get recommendations');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="recommendations-page">
      <div className="recommendations-container">
        <div className="recommendations-header">
          <h1>✨ Get Outfit Recommendations</h1>
          <p>
            Choose an occasion and let AutoStylist suggest the perfect outfit for you
          </p>
        </div>

        <div className="occasion-selector">
          <h2>Select Your Occasion</h2>
          <div className="occasions-list">
            {occasions.map((occ) => (
              <div
                key={occ.value}
                className={`occasion-option ${occasion === occ.value ? 'selected' : ''}`}
                onClick={() => {
                  setOccasion(occ.value);
                  setRecommendations(null);
                  setError('');
                }}
              >
                <div className="occasion-header">
                  <span className="occasion-label">{occ.label}</span>
                  <input
                    type="radio"
                    name="occasion"
                    value={occ.value}
                    checked={occasion === occ.value}
                    onChange={() => setOccasion(occ.value)}
                    className="occasion-radio"
                  />
                </div>
                <p className="occasion-desc">{occ.description}</p>
              </div>
            ))}
          </div>
        </div>

        <div className="occasion-selector" style={{ marginTop: '2rem' }}>
          <h2>Select Preference</h2>
          <div className="occasions-list">
            {genders.map((g) => (
              <div
                key={g.value}
                className={`occasion-option ${gender === g.value ? 'selected' : ''}`}
                onClick={() => {
                  setGender(g.value);
                  setRecommendations(null);
                  setError('');
                }}
              >
                <div className="occasion-header">
                  <span className="occasion-label">{g.label}</span>
                  <input
                    type="radio"
                    name="gender"
                    value={g.value}
                    checked={gender === g.value}
                    onChange={() => setGender(g.value)}
                    className="occasion-radio"
                  />
                </div>
              </div>
            ))}
          </div>
        </div>

        {error && (
          <div className="alert alert-error">
            <span>❌ {error}</span>
            <p className="error-hint">
              Make sure you have uploaded wardrobe items for this occasion.
            </p>
          </div>
        )}

        <div className="get-recommendations-btn-container">
          <button
            onClick={handleGetRecommendations}
            disabled={loading}
            className="btn btn-primary btn-large"
          >
            {loading ? '⏳ Getting Recommendations...' : '🎯 Get Recommendations'}
          </button>
        </div>

        {recommendations && context && (
          <OutfitRecommendation
            recommendations={recommendations}
            context={context}
            onFeedbackSent={handleGetRecommendations}
          />
        )}

        {!loading && !recommendations && !error && (
          <div className="placeholder">
            <p>👕 Select an occasion and click "Get Recommendations" to start</p>
          </div>
        )}
      </div>
    </div>
  );
}
