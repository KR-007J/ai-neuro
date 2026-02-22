# 🎨 NeuroLearn AI Dashboard

## Modern, Vibrant Frontend Dashboard

A beautiful, responsive dashboard built with HTML, CSS, and vanilla JavaScript. Features smooth animations, vibrant gradients, and enterprise-grade design.

## ✨ Features

- **Animated Background** - Floating gradient orbs with smooth animations
- **Smooth Transitions** - All interactions have polished animations
- **Vibrant Design** - Modern color gradients and glass morphism effects
- **Responsive Layout** - Works on all screen sizes
- **Interactive Cards** - Hover effects and smooth transitions
- **Real Progress Tracking** - Animated progress bars and stats
- **No Dependencies** - Pure HTML, CSS, and JavaScript

## 🚀 Quick Start

### Option 1: Simple File Server (Easiest)

```bash
# Navigate to frontend directory
cd frontend

# Python 3
python -m http.server 8080

# Or with Node.js (if you have it)
npx serve

# Open browser to http://localhost:8080
```

### Option 2: VS Code Live Server

1. Install "Live Server" extension in VS Code
2. Right-click on `index.html`
3. Select "Open with Live Server"

### Option 3: Double Click

Simply double-click `index.html` to open in your browser!

## 🎯 Connecting to Backend API

The dashboard is configured to connect to the FastAPI backend at `http://localhost:8000`.

Make sure your backend is running:

```bash
# In project root
uvicorn app.main:app --reload
```

Then open the frontend, and it will automatically fetch data from the API.

## 📁 File Structure

```
frontend/
├── index.html      # Main HTML file
├── styles.css      # All styles with animations
├── app.js          # Interactive functionality
└── README.md       # This file
```

## 🎨 Design Features

### Color Palette
- **Primary Gradient**: Purple to Indigo (#667eea → #764ba2)
- **Success**: Emerald Green (#10b981)
- **Info**: Blue (#3b82f6)
- **Warning**: Orange (#f97316)

### Typography
- **Main Font**: Plus Jakarta Sans (modern, professional)
- **Code Font**: JetBrains Mono

### Animations
- Fade-in-up on scroll
- Smooth hover transitions
- Animated progress bars
- Floating gradient orbs
- Pulsing indicators

## 🔧 Customization

### Change Colors

Edit the CSS variables in `styles.css`:

```css
:root {
    --primary: #667eea;
    --secondary: #764ba2;
    /* Add your colors */
}
```

### Add New Pages

1. Create a new section in `index.html`
2. Add navigation link in sidebar
3. Update `app.js` navigation handler

### Connect Real API

Update `API_BASE_URL` in `app.js`:

```javascript
const API_BASE_URL = 'https://your-api.onrender.com/api/v1';
```

## 🌐 Deployment

### Deploy Frontend (Netlify/Vercel)

1. Push frontend folder to GitHub
2. Connect to Netlify or Vercel
3. Set build directory to `frontend`
4. Deploy!

### Update API URL

When deploying, update the API URL in `app.js` to your production backend URL.

## 📱 Responsive Design

The dashboard is fully responsive:
- **Desktop**: Full sidebar + grid layout
- **Tablet**: Optimized card sizes
- **Mobile**: Stacked layout, hidden sidebar

## 🎯 Key Components

### Stat Cards
Display key metrics with icons, values, and trend indicators

### Progress Items
Show module completion with animated progress bars

### Cognitive Profile
Display user's learning characteristics

### Recommendations
AI-powered content suggestions

### Activity Timeline
Recent learning activities with status indicators

## 💡 Tips

- **Performance**: All animations use CSS transforms for 60fps
- **Accessibility**: Proper ARIA labels and semantic HTML
- **SEO**: Meta tags and structured data
- **PWA Ready**: Can be converted to PWA easily

## 🚀 Next Steps

1. ✅ Open `index.html` in browser
2. ✅ Start the backend API
3. ✅ Explore the interactive dashboard
4. ✅ Customize colors and content
5. ✅ Deploy to production

---

**Built with ❤️ using modern web technologies**
