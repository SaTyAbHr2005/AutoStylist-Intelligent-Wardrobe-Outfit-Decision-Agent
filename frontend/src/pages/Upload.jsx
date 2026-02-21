import { useState } from 'react';
import { uploadItem } from '../services/api';
import '../styles/Upload.css';

export default function Upload() {
  const [file, setFile] = useState(null);
  const [category, setCategory] = useState('top');
  const [style, setStyle] = useState('casual');
  const [gender, setGender] = useState('male');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [uploadedImage, setUploadedImage] = useState(null);
  const [colors, setColors] = useState([]);
  const [preview, setPreview] = useState(null);

  const baseCategories = ['top', 'bottom', 'shoes', 'accessories', 'jewellery'];
  const femaleExclusiveCategories = ['full_body', 'saree', 'lehenga'];
  const categories = gender === 'female' ? [...baseCategories, ...femaleExclusiveCategories] : baseCategories;

  const styles = ['casual', 'formal', 'party', 'traditional'];
  const genders = ['male', 'female'];

  const handleFileChange = (e) => {
    const selectedFile = e.target.files?.[0];
    if (!selectedFile) return;

    setFile(selectedFile);
    setError('');
    setSuccess('');

    // Create preview
    const reader = new FileReader();
    reader.onloadend = () => {
      setPreview(reader.result);
    };
    reader.readAsDataURL(selectedFile);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!file) {
      setError('Please select a file');
      return;
    }

    if (!category) {
      setError('Please select a category');
      return;
    }

    setLoading(true);
    setError('');
    setSuccess('');

    try {
      const response = await uploadItem(file, category, style, gender);
      setSuccess(`Item uploaded successfully!`);
      setColors(response.colors || []);
      setUploadedImage(response.image);

      // Reset form
      setFile(null);
      setPreview(null);
      setCategory('top');
      setStyle('casual');
      setGender('male');
    } catch (err) {
      setError(err.error || 'Upload failed. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="upload-page">
      <div className="upload-container">
        <div className="upload-header">
          <h1>📸 Add Item to Wardrobe</h1>
          <p>Upload a photo of your clothing item with proper lighting</p>
        </div>

        <div className="upload-content">
          <div className="upload-form-section">
            <form onSubmit={handleSubmit} className="upload-form">
              <div className="form-group">
                <label htmlFor="gender" className="form-label">
                  Gender *
                </label>
                <select
                  id="gender"
                  value={gender}
                  onChange={(e) => {
                    setGender(e.target.value);
                    // Reset category to 'top' if male is selected and a female-exclusive category was previously selected
                    if (e.target.value === 'male' && femaleExclusiveCategories.includes(category)) {
                      setCategory('top');
                    }
                  }}
                  className="form-control"
                  disabled={loading}
                >
                  {genders.map((g) => (
                    <option key={g} value={g}>
                      {g.charAt(0).toUpperCase() + g.slice(1)}
                    </option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label htmlFor="category" className="form-label">
                  Category *
                </label>
                <select
                  id="category"
                  value={category}
                  onChange={(e) => setCategory(e.target.value)}
                  className="form-control"
                  disabled={loading}
                >
                  {categories.map((cat) => (
                    <option key={cat} value={cat}>
                      {cat.replace('_', ' ').charAt(0).toUpperCase() + cat.replace('_', ' ').slice(1)}
                    </option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label htmlFor="style" className="form-label">
                  Style
                </label>
                <select
                  id="style"
                  value={style}
                  onChange={(e) => setStyle(e.target.value)}
                  className="form-control"
                  disabled={loading}
                >
                  {styles.map((s) => (
                    <option key={s} value={s}>
                      {s.charAt(0).toUpperCase() + s.slice(1)}
                    </option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label htmlFor="file" className="form-label">
                  Image File *
                </label>
                <div className="file-input-wrapper">
                  <input
                    type="file"
                    id="file"
                    accept="image/jpeg,image/png,image/webp"
                    onChange={handleFileChange}
                    disabled={loading}
                    className="file-input"
                  />
                  <span className="file-input-label">
                    {file ? file.name : 'Choose image (JPG, PNG, WEBP)'}
                  </span>
                </div>
                <small className="form-hint">Accepted formats: JPG, PNG, WEBP (Max 20MB)</small>
              </div>

              {error && <div className="alert alert-error">{error}</div>}
              {success && <div className="alert alert-success">{success}</div>}

              <button
                type="submit"
                disabled={loading || !file}
                className="btn btn-upload"
              >
                {loading ? 'Uploading...' : '📤 Upload Item'}
              </button>
            </form>
          </div>

          {preview && (
            <div className="upload-preview-section">
              <h3>Preview</h3>
              <div className="preview-card">
                <img src={preview} alt="Preview" className="preview-image" />
                <div className="preview-info">
                  <p>
                    <strong>Category:</strong> {category}
                  </p>
                  <p>
                    <strong>Style:</strong> {style}
                  </p>
                </div>
              </div>
            </div>
          )}
        </div>

        {uploadedImage && colors.length > 0 && (
          <div className="upload-result">
            <h2>✅ Upload Successful!</h2>
            <div className="result-content">
              <div className="result-image">
                <img
                  src={uploadedImage.startsWith('http') ? uploadedImage : `http://localhost:8000/static/${uploadedImage}`}
                  alt="Uploaded"
                  className="result-img"
                  onError={(e) => {
                    e.target.src = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="200" height="200"%3E%3Crect fill="%23ccc" width="200" height="200"/%3E%3C/svg%3E';
                  }}
                />
              </div>
              <div className="result-details">
                <h3>Detected Colors</h3>
                <div className="colors-display">
                  {colors.map((color, idx) => {
                    const rgbColor = Array.isArray(color) ? `rgb(${color.join(',')})` : color;
                    return (
                      <div key={idx} className="color-sample">
                        <div
                          className="color-square"
                          style={{ backgroundColor: rgbColor }}
                        />
                        <span className="color-name">{rgbColor}</span>
                      </div>
                    );
                  })}
                </div>
                <button
                  className="btn btn-secondary mt-20"
                  onClick={() => {
                    setUploadedImage(null);
                    setColors([]);
                    setSuccess('');
                  }}
                >
                  Upload Another Item
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
