# 🍳 Smart Cooking Assistant

ML-powered recipe recommendation system with intelligent ingredient matching.

## Project Structure
```
cooking-assistant/
├── backend/     # FastAPI + ML models
└── frontend/    # Next.js web interface
```

## Features
- Recipe search from ingredients
- Cooking time prediction
- Recipe simplification
- Ingredient substitutions

## Tech Stack
**Backend:** Python, FastAPI, scikit-learn, Claude API
**Frontend:** Next.js, TypeScript, Tailwind CSS

## Quick Start

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Links
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs