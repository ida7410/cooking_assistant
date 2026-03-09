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

## Environment Variables
- `ENVIRONMENT` - development/production
- `ANTHROPIC_API_KEY` - Claude API key

## Features
- Add content-based recommender (TF-IDF: 65% ingredients, 30% tags, 5% time)
- Add collaborative recommender (item-based co-occurrence on 1.1M user ratings)
- Add hybrid recommender (50/50 weighted combination with fallback)
- Implement singleton RecommenderManager for efficient data loading (loads once, shares across all recommenders)
- Create Pydantic schemas for type-safe responses (Recipe, RecipeRecommendation, RecommendationResponse)
- Add consistent error handling with status field and error_message
- Handle edge cases (empty recommendations, missing data, unpopular recipes)
- All recommenders tested and verified working

## Components:
- Content: R²=0.488 (TF-IDF cosine similarity)
- Collaborative: User co-occurrence with Jaccard/confidence scoring
- Hybrid: Normalized score combination with graceful degradation
- Recipe Matcher: Ingredient-based TF-IDF matching