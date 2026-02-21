import { Link } from 'react-router-dom';
import '../styles/Home.css';

export default function Home() {
  return (
    <div className="home">
      <section className="hero">
        <div className="hero-content">
          <h1>Welcome to AutoStylist</h1>
          <p>Your Intelligent Wardrobe & Outfit Decision Agent</p>
          <p className="hero-subtitle">
            Get personalized outfit recommendations based on weather, occasion, and your style preferences
          </p>
          <div className="hero-buttons">
            <Link to="/recommendations" className="btn btn-primary">
              Get Outfit Recommendations
            </Link>
            <Link to="/upload" className="btn btn-secondary">
              Add to Wardrobe
            </Link>
          </div>
        </div>
      </section>

      <section className="features">
        <h2>How It Works</h2>
        <div className="features-grid">
          <div className="feature-card">
            <div className="feature-icon">📸</div>
            <h3>Upload Items</h3>
            <p>Add your wardrobe items with photos and we'll analyze colors, styles, and categories.</p>
          </div>

          <div className="feature-card">
            <div className="feature-icon">🌍</div>
            <h3>Smart Context</h3>
            <p>We check your location, weather, and occasion to suggest perfect outfits.</p>
          </div>

          <div className="feature-card">
            <div className="feature-icon">✨</div>
            <h3>AI Recommendations</h3>
            <p>Get three levels of outfit recommendations ranked by compatibility and style.</p>
          </div>

          <div className="feature-card">
            <div className="feature-icon">❤️</div>
            <h3>Smart Learning</h3>
            <p>Provide feedback to teach the AI your preferences and improve recommendations.</p>
          </div>

          <div className="feature-card">
            <div className="feature-icon">👕</div>
            <h3>Complete Outfits</h3>
            <p>We suggest matching shoes, accessories, and jewelry for complete looks.</p>
          </div>

          <div className="feature-card">
            <div className="feature-icon">📊</div>
            <h3>Your Wardrobe</h3>
            <p>Manage and organize all your items in one place with detailed metadata.</p>
          </div>
        </div>
      </section>

      <section className="getting-started">
        <h2>Get Started</h2>
        <div className="steps">
          <div className="step">
            <div className="step-number">1</div>
            <h3>Build Your Wardrobe</h3>
            <p>
              <Link to="/upload">Upload photos</Link> of your clothes, shoes, and accessories.
            </p>
          </div>
          <div className="step-arrow">→</div>
          <div className="step">
            <div className="step-number">2</div>
            <h3>Get Recommendations</h3>
            <p>
              Choose an occasion and let AutoStylist <Link to="/recommendations">recommend outfits</Link>.
            </p>
          </div>
          <div className="step-arrow">→</div>
          <div className="step">
            <div className="step-number">3</div>
            <h3>Give Feedback</h3>
            <p>Tell us what you like or dislike to improve recommendations.</p>
          </div>
        </div>
      </section>

      <section className="occasions">
        <h2>Choose Your Occasion</h2>
        <div className="occasions-grid">
          <div className="occasion-card">
            <div className="occasion-emoji">👔</div>
            <h3>Office</h3>
            <p>Professional and formal wear</p>
          </div>
          <div className="occasion-card">
            <div className="occasion-emoji">🌤️</div>
            <h3>Casual</h3>
            <p>Relaxed everyday outfits</p>
          </div>
          <div className="occasion-card">
            <div className="occasion-emoji">🎉</div>
            <h3>Party</h3>
            <p>Stylish and festive looks</p>
          </div>
          <div className="occasion-card">
            <div className="occasion-emoji">👗</div>
            <h3>Traditional</h3>
            <p>Cultural and classic attire</p>
          </div>
        </div>
      </section>
    </div>
  );
}
