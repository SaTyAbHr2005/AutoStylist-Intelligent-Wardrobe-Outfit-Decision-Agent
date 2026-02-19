import { useState } from 'react';
import './App.css';

function App() {
  const [gender, setGender] = useState('male');
  const [file, setFile] = useState(null);
  const [category, setCategory] = useState('top');
  const [style, setStyle] = useState('casual');
  const [occasion, setOccasion] = useState('casual');
  const [result, setResult] = useState(null);
  const [uploadStatus, setUploadStatus] = useState('');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a file");
      return;
    }

    const formData = new FormData();
    formData.append('file', file);
    formData.append('category', category);
    formData.append('style', style);
    formData.append('gender', gender);

    try {
      const response = await fetch('/api/upload', {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      if (response.ok) {
        setUploadStatus(`Uploaded: ${data.category}`);
        setFile(null); // Reset file input
      } else {
        setUploadStatus(`Error: ${data.detail || 'Upload failed'}`);
      }
    } catch (error) {
      console.error('Error uploading:', error);
      setUploadStatus('Error uploading file');
    }
  };

  const handleRecommend = async () => {
    const formData = new FormData();
    formData.append('occasion', occasion);
    formData.append('gender', gender);

    try {
      const response = await fetch('/api/recommend', {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      if (response.ok) {
        setResult(data);
      } else {
        alert(data.error || "Failed to get recommendations");
      }
    } catch (error) {
      console.error('Error getting recommendations:', error);
      alert('Error communicating with server');
    }
  };

  return (
    <div className="container">
      <h1>AutoStylist</h1>

      <div className="gender-selector">
        <label>
          <input
            type="radio"
            value="male"
            checked={gender === 'male'}
            onChange={(e) => setGender(e.target.value)}
          /> Male
        </label>
        <label>
          <input
            type="radio"
            value="female"
            checked={gender === 'female'}
            onChange={(e) => setGender(e.target.value)}
          /> Female
        </label>
      </div>

      <div className="section upload-section">
        <h2>Upload Item ({gender})</h2>
        <input type="file" onChange={handleFileChange} />
        <select value={category} onChange={(e) => setCategory(e.target.value)}>
          <option value="top">Top</option>
          <option value="bottom">Bottom</option>
          <option value="shoes">Shoes</option>
          <option value="accessories">Accessory</option>
          <option value="jewellery">Jewellery</option>
          <option value="full_body">Full Body (Saree/Lehenga)</option>
        </select>
        <select value={style} onChange={(e) => setStyle(e.target.value)}>
          <option value="casual">Casual</option>
          <option value="formal">Formal</option>
          <option value="party">Party</option>
          <option value="traditional">Traditional</option>
        </select>
        <button onClick={handleUpload}>Upload</button>
        <p>{uploadStatus}</p>
      </div>

      <div className="section recommend-section">
        <h2>Get Recommendation ({gender})</h2>
        <select value={occasion} onChange={(e) => setOccasion(e.target.value)}>
          <option value="casual">Casual</option>
          <option value="office">Office</option>
          <option value="party">Party</option>
          <option value="traditional">Traditional</option>
        </select>
        <button onClick={handleRecommend}>Recommend</button>

        <button onClick={handleRecommend}>Recommend</button>

        {result && (
          <div className="results">
            {result.recommendations.best && (
              <div className="outfit">
                <h3>Best Outfit</h3>
                {result.recommendations.best.full_body ? (
                  <div className="item">
                    <p>Full Body</p>
                    <img src={`http://localhost:8000/${result.recommendations.best.full_body}`} alt="Full Body" width="100" />
                  </div>
                ) : (
                  <>
                    <div className="item">
                      <p>Top</p>
                      <img src={`http://localhost:8000/${result.recommendations.best.top}`} alt="Top" width="100" />
                    </div>
                    <div className="item">
                      <p>Bottom</p>
                      <img src={`http://localhost:8000/${result.recommendations.best.bottom}`} alt="Bottom" width="100" />
                    </div>
                  </>
                )}
                {result.extras?.shoes && (
                  <div className="item">
                    <p>Shoes</p>
                    <img src={`http://localhost:8000/${result.extras.shoes}`} alt="Shoes" width="100" />
                  </div>
                )}
                {result.extras?.jewellery && (
                  <div className="item">
                    <p>Jewellery</p>
                    <img src={`http://localhost:8000/${result.extras.jewellery}`} alt="Jewellery" width="100" />
                  </div>
                )}
                {result.extras?.accessories && result.extras.accessories.map((acc, index) => (
                  <div className="item" key={index}>
                    <p>Accessory</p>
                    <img src={`http://localhost:8000/${acc}`} alt={`Accessory ${index}`} width="100" />
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
