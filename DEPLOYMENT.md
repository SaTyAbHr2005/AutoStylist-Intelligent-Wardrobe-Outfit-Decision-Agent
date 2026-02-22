# AutoStylist - Deployment Guide

## Problem with Previous Render Deployment

The previous deployment failed with:
```
Port scan timeout reached, no open ports detected. Bind your service to at least one port.
```

### Root Cause
1. **Missing PORT binding**: Uvicorn was not explicitly binding to the `$PORT` environment variable that Render provides
2. **Incorrect command format**: The start command wasn't properly reading the Render-supplied `$PORT` 
3. **CORS issues**: Frontend couldn't communicate with backend due to missing production origins
4. **No graceful startup**: App wasn't signaling successful startup to Render's health checker

## Solution Implemented

### 1. Created `Procfile` (Project Root)
Routes Render to start the backend with proper PORT binding:
```
web: cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers 1
```

### 2. Updated Backend CORS (`app/main.py`)
- Configured to accept `*` (all origins) in production
- Can read `FRONTEND_URL` from environment for fine-tuned CORS later
- Added startup logging for deployment debugging

### 3. Updated Backend Requirements (`requirements.txt`)
- Added `uvicorn[standard]` with async workers
- Added `email-validator` for Pydantic EmailStr
- Added `gunicorn` for alternative WSGI server option

### 4. Updated Frontend Config (`vite.config.js`)
- Configured to bind to `0.0.0.0` on dynamic Render PORT
- Added preview mode for production builds
- Enabled proper host binding for containerized environment

### 5. Environment Configuration (`.env.example`)
- Define required env vars for production deployment
- MONGO_URI, SECRET_KEY, Cloudinary credentials
- FRONTEND_URL and VITE_API_BASE_URL for cross-service communication

## Deployment Steps on Render

### Backend Deployment
1. Go to [Render.com](https://render.com)
2. Create a **New Web Service**
3. Connect your GitHub repository
4. Configure:
   - **Build Command**: `cd backend && pip install -r requirements.txt`
   - **Start Command**: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers 1`
   - **Python Version**: 3.11
   - **Environment Variables** (from `.env.example`):
     ```
     MONGO_URI=mongodb+srv://YOUR_USERNAME:YOUR_PASSWORD@cluster.mongodb.net/autostylist
     SECRET_KEY=your-very-long-random-secret-key
     CLOUDINARY_CLOUD_NAME=your-value
     CLOUDINARY_API_KEY=your-value
     CLOUDINARY_API_SECRET=your-value
     FRONTEND_URL=https://your-frontend-render-domain.onrender.com
     ```
5. Deploy

### Frontend Deployment
1. Create a **New Static Site** on Render
2. Connect your GitHub repository
3. Configure:
   - **Build Command**: `cd frontend && npm install && npm run build`
   - **Publish Directory**: `frontend/dist`
   - **Environment Variables**:
     ```
     VITE_API_BASE_URL=https://your-backend-render-domain.onrender.com/api
     ```
4. Deploy

### MongoDB Connection
For production, use **MongoDB Atlas** (free tier available):
1. Create cluster at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Get connection string: `mongodb+srv://username:password@cluster.mongodb.net/autostylist`
3. Set `MONGO_URI` in Render backend environment

## Troubleshooting Render Deployment

### Issue: "No open ports detected"
**Solution**: Ensure Procfile exists at project root and start command binds to `$PORT`:
```
web: cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Issue: "CORS errors from frontend"
**Solution**: Update `FRONTEND_URL` env var in backend and ensure it's in CORS origins.

### Issue: "MongoDB connection refused"
**Solution**: 
- Verify `MONGO_URI` is correct
- Whitelist Render IPs in MongoDB Atlas (IP whitelist: 0.0.0.0/0 for development)
- Check database name matches in code

### Issue: "502 Bad Gateway"
**Solution**:
- Check backend logs: Render dashboard → Logs
- Ensure all environment variables are set
- Verify PORT binding in logs

## Local Testing Before Deployment

### Start Backend
```bash
cd backend
pip install -r requirements.txt
export PORT=8000  # or set in .env
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Start Frontend
```bash
cd frontend
npm install
npm run build
npm run preview -- --host 0.0.0.0 --port 4173
```

### Test Production Build Locally
```bash
# Backend
cd backend
uvicorn app.main:app --reload

# Frontend (in new terminal)
cd frontend
npm run build
npm run preview
```

## Production Checklist

- [ ] Backend deployed and responding at `/`
- [ ] Frontend deployed and accessible
- [ ] MongoDB Atlas cluster configured and connected
- [ ] All environment variables set in Render
- [ ] CORS configured for frontend domain
- [ ] Test login: register → login → profile → logout
- [ ] Test upload: upload item → view in wardrobe
- [ ] Test recommendations: add top + bottom → get outfit recommendations
- [ ] Monitor Render logs for errors

## Key Files Modified for Deployment

1. **Procfile** - Tells Render how to start backend
2. **backend/app/main.py** - Updated CORS for production
3. **backend/requirements.txt** - Added production dependencies
4. **frontend/vite.config.js** - Configured for Render environment
5. **.env.example** - Template for environment variables
6. **render.yaml** - (Optional) Full deployment config if using render.yaml

## Next Steps

After deployment verification:
1. Monitor performance and logs
2. Set stricter CORS origins (replace `*` with actual frontend domain)
3. Implement proper error logging and alerting
4. Add database backups
5. Set up CI/CD for automated deployments on push
