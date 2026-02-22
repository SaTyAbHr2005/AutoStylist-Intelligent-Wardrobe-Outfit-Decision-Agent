# AutoStylist - Intelligent Wardrobe & Outfit Decision Agent

A full-stack AI-powered wardrobe management and outfit recommendation system using FastAPI, React, MongoDB, and Machine Learning.

## 📋 Features

✅ **User Authentication**: Secure registration, login, profile management, logout  
✅ **Wardrobe Upload**: Upload clothing items with automatic background removal and color extraction  
✅ **Smart Recommendations**: AI-powered outfit recommendations based on occasion, weather, and style  
✅ **Wardrobe Management**: View, organize, and manage your clothing collection  
✅ **Responsive UI**: Mobile-friendly React frontend with intuitive navigation  
✅ **Profile Management**: View user profile, logout from profile dropdown  

## 🚀 Quick Start (Local Development)

### Prerequisites
- Python 3.11+
- Node.js 18+
- MongoDB (local or Atlas cloud)

### Setup

1. **Clone and navigate**
```bash
cd AutoStylist-Intelligent-Wardrobe-Outfit-Decision-Agent
```

2. **Backend Setup**
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env  # and fill with your credentials
```

3. **Frontend Setup**
```bash
cd ../frontend
npm install
```

4. **Run Backend**
```bash
cd ../backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

5. **Run Frontend** (in new terminal)
```bash
cd frontend
npm run dev
```

6. **Access**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 🧪 Testing

### E2E Tests (Backend)
```bash
cd backend
python scripts/e2e_test.py          # Register/login/me endpoints
python scripts/e2e_upload_test.py   # Upload image  
python scripts/upload_two_items.py  # Upload top + bottom for recommendations
```

### Manual Test Flow
1. Register: `/register`
2. Login: `/login` (credentials saved)
3. Profile: `/profile` (click profile menu top-right)
4. Upload: `/upload` (add clothing items)
5. Recommendations: `/recommendations` (get AI outfit suggestions)
6. Logout: Click profile menu → Logout

## 📦 Project Structure

```
AutoStylist-Intelligent-Wardrobe-Outfit-Decision-Agent/
├── backend/
│   ├── app/
│   │   ├── config/          # Database config
│   │   ├── models/          # Pydantic models
│   │   ├── routes/          # API endpoints
│   │   ├── services/        # Business logic
│   │   └── main.py          # FastAPI app
│   ├── scripts/             # E2E test scripts
│   ├── requirements.txt     # Python dependencies
│   ├── Procfile             # Render deployment
│   └── .env.example         # Environment template
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── pages/           # Page components
│   │   ├── services/        # API client
│   │   ├── styles/          # CSS
│   │   └── App.jsx          # Main app
│   ├── package.json         # Npm dependencies
│   ├── vite.config.js       # Vite config
│   └── .env.example         # Frontend env template
├── Procfile                 # Root Render config
├── render.yaml              # Render deployment config
└── DEPLOYMENT.md            # Deployment guide
```

## 🔧 Tech Stack

**Backend**:
- FastAPI (async REST API)
- FastAPI-JWT-Auth (OAuth2 authentication)
- MongoDB (database)
- Pydantic (data validation)
- Cloudinary (image hosting)
- rembg (background removal)
- scikit-learn (color analysis)

**Frontend**:
- React 19 (UI framework)
- React Router 7 (routing)
- Axios (HTTP client)
- Vite (build tool)
- CSS3 (styling with media queries for responsive design)

## 🌐 Deployment (Render.com)

See [DEPLOYMENT.md](./DEPLOYMENT.md) for complete deployment guide.

**TL;DR**:
1. Create Render Web Service (Backend)
2. Create Render Static Site (Frontend)
3. Set environment variables from `.env.example`
4. Deploy

## 📝 API Endpoints

### Auth
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user
- `POST /api/auth/logout` - Logout user

### Upload
- `POST /api/upload` - Upload wardrobe item

### Recommendations
- `POST /api/recommend` - Get outfit recommendations

### Wardrobe
- `GET /api/wardrobe` - List all items
- `GET /api/wardrobe/{category}` - Get items by category
- `GET /api/stats` - Get wardrobe statistics

### Feedback
- `POST /api/feedback` - Submit outfit feedback

## 🔐 Environment Variables

See `.env.example` for all required variables:

```
MONGO_URI=mongodb+srv://...
SECRET_KEY=your-random-secret
CLOUDINARY_CLOUD_NAME=...
CLOUDINARY_API_KEY=...
CLOUDINARY_API_SECRET=...
FRONTEND_URL=http://localhost:5173
VITE_API_BASE_URL=http://localhost:8000/api
```

## 📸 Features in Detail

### Image Upload
- Automatic background removal using rembg
- Color palette extraction
- Cloudinary cloud storage
- Supported formats: JPG, PNG, WEBP

### Recommendations Engine
- Color theory matching
- Style compatibility
- Occasion-based filtering
- Weather context awareness

### User Experience
- Clean, intuitive UI
- Mobile-responsive design
- Real-time feedback
- Personalized recommendations

## 🐛 Troubleshooting

**Backend won't start**: Check MongoDB connection string in `.env`  
**Upload fails**: Verify Cloudinary credentials and file format  
**CORS errors**: Ensure backend CORS includes frontend URL  
**Port conflicts**: Change PORT in `.env` or kill process on port 8000/5173  

## 📄 License

MIT License - See LICENSE file

## 👥 Contributing

Contributions welcome! Please fork, create feature branch, and submit PR.

## 📞 Support

For issues, check logs:
- Backend: `cd backend && tail -f logs.txt`
- Frontend: Browser console (F12)

---

**Made with ❤️ for smarter wardrobe management**
