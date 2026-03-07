# Backend

FastAPI server for recipe recommendations.

## Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

## 📝 Environment Variables
- `ENVIRONMENT` - development/production
- `ANTHROPIC_API_KEY` - Claude API key

## Plan
- Hybrid Scoring for Content Recommendation
  - 65% Ingredients (what's in the recipe)
  - 30% Tags (cuisine, meal type, dietary info)
  - 5% Time proximity (how close cooking times are)
- Interaction based Recommendation
  - Overlapping user in high rating
  - Matrix Factorization