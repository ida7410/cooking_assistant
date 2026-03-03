# 🍳 Smart Cooking Assistant

![License](https://img.shields.io/github/license/ida7410/cooking-assistant)
![GitHub issues](https://img.shields.io/github/issues/ida7410/cooking-assistant)

ML-powered recipe recommendation system with intelligent ingredient matching.

## 🎯 Features

- 🔍 **Recipe Matching**: TF-IDF similarity-based recipe search
- ⏱️ **Time Prediction**: ML-powered cooking time estimation
- 📝 **Recipe Simplification**: AI-powered beginner-friendly instructions
- 🔄 **Ingredient Substitutions**: Smart alternatives for missing ingredients

## 🏗️ Architecture
```
Frontend (Next.js)  ←→  Backend (FastAPI)  ←→  ML Models
    Vercel                  Railway           scikit-learn
```

## 🚀 Quick Start

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # Add your API keys
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install
cp .env.example .env.local  # Configure API URL
npm run dev
```

## 📝 Environment Variables

### Backend
- `ENVIRONMENT` - development/production
- `ANTHROPIC_API_KEY` - Claude API key

### Frontend
- `NEXT_PUBLIC_API_URL` - Backend API URL

See `.env.example` files for details.

## 📊 Tech Stack

**Backend:** Python, FastAPI, scikit-learn, Claude API  
**Frontend:** Next.js 14, TypeScript, Tailwind CSS  
**Deployment:** Vercel + Railway

## 📝 License

MIT © 2026 Hyeonbeen (Ida) Yoon