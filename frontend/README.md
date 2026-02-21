# AutoStylist Frontend

A modern, professional React frontend for the AutoStylist Intelligent Wardrobe & Outfit Decision Agent.

## Features

✨ **Professional UI Design**
- Modern gradient color scheme with primary (Indigo), secondary (Pink), and accent colors
- Responsive design for desktop, tablet, and mobile devices
- Smooth animations and transitions
- Professional typography and spacing

👕 **Complete Wardrobe Management**
- Upload wardrobe items with category and style classification
- View and organize items by category
- Display extracted color palettes for each item

🎯 **Smart Recommendations**
- Get personalized outfit recommendations for different occasions
- Casual, Office/Professional, Party, Traditional

📊 **Context-Aware Suggestions**
- Real-time weather integration
- Location-specific recommendations
- Occasion-based styling

💬 **Feedback System**
- Like/Dislike outfit recommendations
- "Wear This" action to track usage
- Machine learning model improvement through feedback

## Project Structure

```
src/
├── components/          # Reusable UI components
├── pages/              # Full page components
├── services/           # API integration
├── styles/             # CSS modules for components
├── App.jsx             # Main app component
├── main.jsx            # Entry point
└── index.css           # Global styles
```

## Pages

### 🏠 Home Page
- Hero section with CTA buttons
- Feature showcase
- Getting started guide
- Occasion selector cards

### 📸 Upload Page
- File upload with preview
- Category selection (Top, Bottom, Shoes, Accessories, Jewellery)
- Style selection (Casual, Formal, Party, Traditional)
- Extracted color display
- Success feedback with uploaded image

### ✨ Recommendations Page
- Occasion selector with radio buttons
- Context information display (weather, location, temperature)
- Three-tier outfit recommendations
- Feedback buttons (Like, Dislike, Wear This)
- Suggested extras (shoes, accessories, jewellery)

### 👕 Wardrobe Management Page
- Statistics dashboard
- Category filtering
- Grid view of wardrobe items
- Color palette display per item

## Getting Started

1. **Install dependencies**
   ```bash
   npm install
   ```

2. **Start development server**
   ```bash
   npm run dev
   ```

3. **Build for production**
   ```bash
   npm run build
   ```

## Technologies Used

- React 19.2.0
- React Router DOM
- Axios
- Vite
- CSS3

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## License

© 2026 AutoStylist. All rights reserved.

