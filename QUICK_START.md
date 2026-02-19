# AutoStylist - Quick Start Guide

## 🚀 Getting Started in 3 Minutes

### Step 1: Start Backend Server
```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
✅ Backend running at: **http://localhost:8000**

### Step 2: Start Frontend Server
```bash
cd frontend
npm run dev
```
✅ Frontend running at: **http://localhost:5173**

### Step 3: Open in Browser
Visit: **http://localhost:5173**

---

## 📱 UI Overview

### Navigation Menu (Top)
- ✨ AutoStylist (Logo)
- Home
- My Wardrobe
- Upload Item
- Get Recommendations

### Main Pages

#### 🏠 Home (/)
- Hero section with quick start buttons
- Feature showcase
- Getting started guide
- Occasion information

#### 📸 Upload Item (/upload)
1. Select category (Top, Bottom, Shoes, Accessories, Jewellery)
2. Select style (Casual, Formal, Party, Traditional)
3. Choose image file
4. See color analysis results

#### ✨ Get Recommendations (/recommendations)
1. Select occasion
2. View weather & context
3. Choose from 3 outfit recommendations
4. Provide feedback (Like/Dislike/Wear This)
5. See suggested shoes, accessories, jewelry

#### 👕 My Wardrobe (/wardrobe)
- View all uploaded items
- Filter by category
- See color palette for each item
- Track usage count

---

## 🎨 Design Highlights

- **Modern Gradient UI** (Indigo & Pink)
- **Responsive Design** (Works on mobile, tablet, desktop)
- **Professional Layout** (Clean, organized, easy to use)
- **Fast Performance** (Smooth animations, quick loading)
- **Dark Text on Light Background** (Easy to read)

---

## 🔧 Troubleshooting

### Backend Issues

**Problem:** "ModuleNotFoundError: No module named 'app'"
```bash
# Make sure you're in the backend directory
cd backend
# Then run with python -m flag
python -m uvicorn app.main:app --reload
```

**Problem:** "Connection refused" on port 8000
```bash
# Port already in use? Change to different port
python -m uvicorn app.main:app --reload --port 8001
# Then update frontend api.js with new port
```

**Problem:** MongoDB connection error
```bash
# Make sure MongoDB is running
# Windows: Search for MongoDB in Services, or run mongod
# Mac/Linux: brew services start mongodb-community
```

### Frontend Issues

**Problem:** Page shows blank or errors
1. Open browser console (F12)
2. Check for error messages
3. Verify backend is running at http://localhost:8000
4. Clear browser cache and reload

**Problem:** "Cannot find module 'react-router-dom'"
```bash
cd frontend
npm install react-router-dom axios
```

**Problem:** Styling looks wrong
1. Clear browser cache (Ctrl+Shift+Del on Windows, Cmd+Shift+Del on Mac)
2. Hard refresh (Ctrl+Shift+R or Cmd+Shift+R)
3. Check if CSS files are in styles/ folder

### API Issues

**Problem:** Upload fails with CORS error
✅ This has been fixed! CORS is enabled on backend

**Problem:** API returns 500 error
1. Check backend console for error details
2. Verify MongoDB is running
3. Check if uploads/ and static/processed/ directories exist

---

## 📊 API Endpoints

All endpoints require form data (not JSON):

### 1. Upload Item
```
POST http://localhost:8000/api/upload
- file: (image file)
- category: top|bottom|shoes|accessories|jewellery
- style: casual|formal|party|traditional
```

### 2. Get Recommendations
```
POST http://localhost:8000/api/recommend
- occasion: casual|office|party|traditional
```

### 3. Send Feedback
```
POST http://localhost:8000/api/feedback
- action: like|dislike|wear
- selected_top, selected_bottom, etc.
```

### 4. Get Context
```
POST http://localhost:8000/api/context
- occasion: casual|office|party|traditional
```

---

## 🎯 Usage Workflow

### First Time User Flow

1. **Go to Home Page**
   - Read about AutoStylist
   - Understand how it works

2. **Upload Items**
   - Click "Upload Item" or "Add to Wardrobe"
   - Upload photos of your clothes
   - Add at least 2-3 items per category
   - System analyzes colors automatically

3. **Get Recommendations**
   - Click "Get Recommendations"
   - Select an occasion
   - View outfit suggestions
   - See shoe and accessory suggestions

4. **Provide Feedback**
   - Like: This outfit looks great!
   - Dislike: Not my style
   - Wear This: I'm wearing this outfit today
   - ML model learns from your preferences

5. **View Wardrobe**
   - Click "My Wardrobe"
   - See all uploaded items
   - Filter by category
   - View color palettes

---

## 📱 Responsive Breakpoints

- **Mobile** (< 480px): Single column, stacked layout
- **Tablet** (480px - 768px): Two columns, adjusted sizing
- **Desktop** (> 768px): Three+ columns, full layout

Test on your phone! The design works great on mobile screens.

---

## 🎨 Color Codes

If you want to customize colors, edit `src/index.css`:

```css
:root {
  --primary-color: #6366f1;      /* Indigo */
  --secondary-color: #ec4899;    /* Pink */
  --accent-color: #f59e0b;       /* Amber */
  --success-color: #10b981;      /* Green */
  --error-color: #ef4444;        /* Red */
}
```

---

## 📦 Project Structure

```
AutoStylist-Intelligent-Wardrobe-Outfit-Decision-Agent/
├── backend/
│   ├── app/
│   │   ├── main.py              ← API endpoints here
│   │   ├── routes/              ← Upload, Recommend, Feedback
│   │   ├── services/            ← Decision engine, colors
│   │   └── config/              ← Database config
│   └── requirements.txt          ← Python dependencies
├── frontend/
│   ├── src/
│   │   ├── pages/               ← Home, Upload, etc.
│   │   ├── components/          ← Header, Cards
│   │   ├── services/            ← API calls
│   │   ├── styles/              ← CSS files
│   │   └── App.jsx              ← Main app
│   ├── package.json             ← npm dependencies
│   └── index.html               ← HTML entry point
└── PROJECT_COMPLETION_SUMMARY.md ← Full documentation
```

---

## ✅ Feature Checklist

### Upload Page
- ✅ File upload
- ✅ Category selector
- ✅ Style selector  
- ✅ Image preview
- ✅ Color analysis
- ✅ Success message
- ✅ Error handling

### Recommendations Page
- ✅ Occasion selector
- ✅ Context display (weather, location)
- ✅ 3 outfit tiers
- ✅ Tab switching
- ✅ Feedback buttons
- ✅ Accessories section
- ✅ Error handling

### Wardrobe Page
- ✅ Statistics cards
- ✅ Category filter
- ✅ Grid view
- ✅ Color indicators
- ✅ Usage tracking
- ✅ Empty state

### Navigation
- ✅ Sticky header
- ✅ Navigation links
- ✅ Logo/branding
- ✅ Professional design

---

## 🔐 Important Notes

### Backend Logic Unchanged ✅
- No core functionality modified
- All business logic preserved
- Only CORS added for frontend

### Frontend Fully Integrated ✅
- All API calls working
- All features connected
- Professional UI complete

### Both Servers Run Independently ✅
- Backend: Python/FastAPI
- Frontend: React/Vite
- Zero conflicts

---

## 📞 Need Help?

### Check These First
1. Is backend running? (http://localhost:8000)
2. Is frontend running? (http://localhost:5173)
3. Is MongoDB running?
4. Check browser console for errors (F12)
5. Check network tab for API errors

### Common Errors
- "API not found" → Backend not running
- "Cannot upload" → MongoDB not connected
- "Page blank" → Frontend build issue, try refreshing
- "Styling weird" → Clear cache (Ctrl+Shift+Delete)

### Files to Check
- Backend: `backend/app/main.py` (CORS configured)
- Frontend: `frontend/src/services/api.js` (API endpoints)
- Styling: `frontend/src/styles/` (CSS files)

---

## 🎉 You're All Set!

Your AutoStylist application is ready to use. Enjoy getting smart outfit recommendations! 

**Frontend:** http://localhost:5173
**Backend API:** http://localhost:8000
**API Docs:** http://localhost:8000/docs

---

*Built with React, FastAPI, and lots of ❤️*
