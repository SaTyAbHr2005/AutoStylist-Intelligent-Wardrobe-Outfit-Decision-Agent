import { BACKEND_BASE_URL } from '../services/api';
import '../styles/ImageCard.css';

export default function ImageCard({ image, title, colors = [], style = '' }) {
  const imageUrl = image?.startsWith('http') ? image : `${BACKEND_BASE_URL}/static/${image}`;

  return (
    <div className="image-card">
      <div className="image-container">
        <img src={imageUrl} alt={title} className="card-image" onError={(e) => {
          e.target.src = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="200" height="200"%3E%3Crect fill="%23ccc" width="200" height="200"/%3E%3Ctext x="50%25" y="50%25" font-size="16" fill="%23999" text-anchor="middle" dy=".3em"%3EImage Not Found%3C/text%3E%3C/svg%3E';
        }} />
      </div>
      {title && <h3 className="card-title">{title}</h3>}
      {colors?.length > 0 && (
        <div className="color-palette">
          {colors.map((color, idx) => (
            <div
              key={idx}
              className="color-dot"
              style={{ backgroundColor: color }}
              title={color}
            />
          ))}
        </div>
      )}
      {style && <p className="card-style">{style}</p>}
    </div>
  );
}
