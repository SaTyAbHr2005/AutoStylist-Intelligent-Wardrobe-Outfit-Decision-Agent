import { useState } from 'react';
import ImageCard from './ImageCard';
import '../styles/OutfitRecommendation.css';
import { sendFeedback } from '../services/api';

export default function OutfitRecommendation({ recommendations, context, onFeedbackSent }) {
  const [loading, setLoading] = useState(false);
  const [selectedOutfit, setSelectedOutfit] = useState('best');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleFeedback = async (action, outfit) => {
    setLoading(true);
    setError('');
    setSuccess('');
    
    try {
      const data = {
        selected_top: outfit === 'best' ? recommendations.best?.top : outfit === 'medium' ? recommendations.medium?.top : recommendations.average?.top,
        selected_bottom: outfit === 'best' ? recommendations.best?.bottom : outfit === 'medium' ? recommendations.medium?.bottom : recommendations.average?.bottom,
        medium_top: recommendations.medium?.top || '',
        medium_bottom: recommendations.medium?.bottom || '',
        average_top: recommendations.average?.top || '',
        average_bottom: recommendations.average?.bottom || '',
        action: action,
      };

      const response = await sendFeedback(data);
      setSuccess(`Feedback recorded: ${action}`);
      onFeedbackSent?.();
    } catch (err) {
      setError(err.error || 'Failed to send feedback');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="outfit-recommendation">
      <div className="context-info">
        <h3>Today's Context</h3>
        <div className="context-grid">
          <div className="context-item">
            <span className="label">Location:</span> {context?.city}
          </div>
          <div className="context-item">
            <span className="label">Temperature:</span> {context?.temperature}°C
          </div>
          <div className="context-item">
            <span className="label">Weather:</span> {context?.weather}
          </div>
          <div className="context-item">
            <span className="label">Occasion:</span> {context?.occasion}
          </div>
        </div>
      </div>

      <div className="recommendation-tabs">
        <button
          className={`tab-btn ${selectedOutfit === 'best' ? 'active' : ''}`}
          onClick={() => setSelectedOutfit('best')}
        >
          ⭐ Best Match
        </button>
        <button
          className={`tab-btn ${selectedOutfit === 'medium' ? 'active' : ''}`}
          onClick={() => setSelectedOutfit('medium')}
        >
          👍 Good Option
        </button>
        <button
          className={`tab-btn ${selectedOutfit === 'average' ? 'active' : ''}`}
          onClick={() => setSelectedOutfit('average')}
        >
          👌 Alternative
        </button>
      </div>

      {error && <div className="error-message">{error}</div>}
      {success && <div className="success-message">{success}</div>}

      <div className="outfit-display">
        {selectedOutfit === 'best' && recommendations.best && (
          <div className="outfit-group">
            <h4 className="outfit-title">Best Match Outfit</h4>
            <div className="outfit-items">
              <div className="outfit-item">
                <ImageCard image={recommendations.best.top} title="Top" />
              </div>
              <div className="outfit-item">
                <ImageCard image={recommendations.best.bottom} title="Bottom" />
              </div>
            </div>
            <div className="feedback-buttons">
              <button 
                className="feedback-btn like" 
                onClick={() => handleFeedback('like', 'best')}
                disabled={loading}
              >
                👍 Like
              </button>
              <button 
                className="feedback-btn dislike" 
                onClick={() => handleFeedback('dislike', 'best')}
                disabled={loading}
              >
                👎 Dislike
              </button>
              <button 
                className="feedback-btn wear" 
                onClick={() => handleFeedback('wear', 'best')}
                disabled={loading}
              >
                ✨ Wear This
              </button>
            </div>
          </div>
        )}

        {selectedOutfit === 'medium' && recommendations.medium && (
          <div className="outfit-group">
            <h4 className="outfit-title">Good Option</h4>
            <div className="outfit-items">
              <div className="outfit-item">
                <ImageCard image={recommendations.medium.top} title="Top" />
              </div>
              <div className="outfit-item">
                <ImageCard image={recommendations.medium.bottom} title="Bottom" />
              </div>
            </div>
            <div className="feedback-buttons">
              <button 
                className="feedback-btn like" 
                onClick={() => handleFeedback('like', 'medium')}
                disabled={loading}
              >
                👍 Like
              </button>
              <button 
                className="feedback-btn dislike" 
                onClick={() => handleFeedback('dislike', 'medium')}
                disabled={loading}
              >
                👎 Dislike
              </button>
              <button 
                className="feedback-btn wear" 
                onClick={() => handleFeedback('wear', 'medium')}
                disabled={loading}
              >
                ✨ Wear This
              </button>
            </div>
          </div>
        )}

        {selectedOutfit === 'average' && recommendations.average && (
          <div className="outfit-group">
            <h4 className="outfit-title">Alternative Outfit</h4>
            <div className="outfit-items">
              <div className="outfit-item">
                <ImageCard image={recommendations.average.top} title="Top" />
              </div>
              <div className="outfit-item">
                <ImageCard image={recommendations.average.bottom} title="Bottom" />
              </div>
            </div>
            <div className="feedback-buttons">
              <button 
                className="feedback-btn like" 
                onClick={() => handleFeedback('like', 'average')}
                disabled={loading}
              >
                👍 Like
              </button>
              <button 
                className="feedback-btn dislike" 
                onClick={() => handleFeedback('dislike', 'average')}
                disabled={loading}
              >
                👎 Dislike
              </button>
              <button 
                className="feedback-btn wear" 
                onClick={() => handleFeedback('wear', 'average')}
                disabled={loading}
              >
                ✨ Wear This
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Extras section */}
      {(recommendations.extras?.shoes || recommendations.extras?.accessories?.length || recommendations.extras?.jewellery) && (
        <div className="extras-section">
          <h3>Suggested Extras</h3>
          <div className="extras-grid">
            {recommendations.extras?.shoes && (
              <div className="extra-item">
                <h4>👞 Shoes</h4>
                <ImageCard image={recommendations.extras.shoes} title="Shoes" />
              </div>
            )}
            {recommendations.extras?.accessories?.length > 0 && (
              <div className="extra-item">
                <h4>🎒 Accessories</h4>
                <div className="extra-items-list">
                  {recommendations.extras.accessories.map((acc, idx) => (
                    <ImageCard key={idx} image={acc} />
                  ))}
                </div>
              </div>
            )}
            {recommendations.extras?.jewellery && (
              <div className="extra-item">
                <h4>💎 Jewellery</h4>
                <ImageCard image={recommendations.extras.jewellery} title="Jewellery" />
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
