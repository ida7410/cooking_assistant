# 🔧 Cooking Assistant - Backend API

> FastAPI-based REST API with ML-powered recipe recommendations

---

## 📋 Table of Contents

- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
- [ML Models](#ml-models)
- [Development](#development)
- [Testing](#testing)

---

## 🎯 Overview

The backend is a FastAPI application serving ML-powered recipe recommendations through a RESTful API. It implements a hybrid recommendation system, cooking time prediction, and AI-powered recipe simplification.

### **Key Features**

- ⚡ **Fast API Performance** - Async endpoints with <100ms response time
- 🤖 **4 ML Models** - Recipe matcher, hybrid recommender, time predictor, recipe simplifier
- 🔄 **Singleton Pattern** - Efficient model management (models loaded once, shared across requests)
- 📊 **Type Safety** - Full Pydantic validation
- 🔍 **Auto Documentation** - Interactive Swagger/OpenAPI docs
- 📝 **Structured Logging** - Configurable log levels (DEBUG/INFO/WARNING/ERROR)

---

## 🛠️ Tech Stack

| Category | Technologies |
|----------|-------------|
| **Framework** | FastAPI 0.110+ |
| **ML/Data** | scikit-learn, pandas, numpy |
| **NLP** | TF-IDF Vectorization |
| **AI** | Anthropic Claude API |
| **Validation** | Pydantic v2 |
| **Server** | Uvicorn (ASGI) |
| **Testing** | pytest, httpx |

---

## 📁 Project Structure

```
backend/
├── src/                          # Application code
│   ├── main.py                  # FastAPI app & startup
│   ├── dependencies.py          # Dependency injection
│   ├── logger.py                # Logging setup
│   └── routers/                 # API endpoints
│       ├── __init__.py
│       └── recipe.py            # Recipe routes
│
├── models/                       # ML models
│   ├── __init__.py
│   ├── content_recommender.py   # Content-based filtering
│   ├── collaborative_recommender.py  # Collaborative filtering
│   ├── hybrid_recommender.py    # Hybrid system
│   ├── recipe_matcher.py        # Ingredient-based search
│   ├── cooking_time_predictor.py # Time prediction (Random Forest)
│   ├── recipe_simplifier.py     # AI simplification (Claude)
│   ├── recommender_manager.py   # Model orchestration (Singleton)
│   └── saved/                   # Trained models
│       └── time_predictor.pkl
│
├── schemas/                      # Pydantic models
│   ├── __init__.py
│   ├── recipe.py                # Recipe schema
│   ├── recipe_recommendation.py # Recommendation schema
│   ├── recommendation_response.py
│   ├── recipe_search_request.py
│   ├── recommendation_request.py
│   └── simplify_request.py
│
├── config.py                     # Configuration
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment template
└── README.md                     # This file
```

---

## 📡 API Endpoints

### **Base URL**
- Development: `http://localhost:8000`
- Production: `https://cookingassistant-production.up.railway.app`

### **Interactive Documentation**
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### **Core Endpoints**

#### **1. Search Recipes by Ingredients**
```http
POST /api/recipe/search
Content-Type: application/json

{
  "ingredients": ["chicken", "rice", "soy sauce"],
  "skill_level": "intermediate",
  "simplify_steps": false,
  "top_n": 10
}
```

**Response:**
```json
[
  {
    "recipe": {
      "id": 12345,
      "name": "Chicken Fried Rice",
      "ingredients": ["chicken", "rice", "soy sauce", ...],
      "steps": [...],
      "cooking_time": 30
    },
    "similarity_score": 0.85,
    "predicted_time": 35,
    "time_breakdown": {
      "base_time": 30,
      "adjusted_time": 35,
      "skill_level": "intermediate"
    }
  }
]
```

#### **2. Get Recipe Details**
```http
GET /api/recipe/{recipe_id}
```

**Response:**
```json
{
  "recipe": {
    "id": 2886,
    "name": "Best Banana Bread",
    "ingredients": [...],
    "steps": [...],
    "n_ingredients": 8,
    "n_steps": 10,
    "cooking_time": 60
  },
  "predicted_time": {
    "base_time": 60,
    "beginner": 78,
    "intermediate": 60,
    "expert": 42
  }
}
```

#### **3. Get Recommendations**
```http
POST /api/recipe/recommend

{
  "recipe_id": 2886,
  "top_n": 10,
  "strategy": "hybrid"
}
```

**Strategies:**
- `"content"` - Ingredient/tag similarity only
- `"collaborative"` - User rating patterns only
- `"hybrid"` - Combined (recommended)

**Response:**
```json
{
  "target": {...},
  "status": "success",
  "strategy": "hybrid",
  "recommendations": [
    {
      "recipe": {...},
      "similarity_score": 0.82,
      "content_score": 0.75,
      "collab_score": 0.89,
      "in_both": true
    }
  ]
}
```

#### **4. Simplify Recipe Steps**
```http
POST /api/recipe/simplify

{
  "recipe_id": 2886,
  "skill_level": "beginner"
}
```

**Response:**
```json
{
  "recipe_id": 2886,
  "recipe_name": "Best Banana Bread",
  "original_steps": [...],
  "simplified_steps": "1. Heat your oven to 350°F (that's medium heat)...",
  "skill_level": "beginner"
}
```

#### **5. Health Check**
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "models_loaded": true,
  "timestamp": "2026-03-12T10:30:00Z",
  "components": {
    "recipe_matcher": "ready",
    "time_predictor": "ready",
    "recipe_simplifier": "ready",
    "recommender_manager": "ready"
  }
}
```

---

## 🤖 ML Models

### **1. Recipe Matcher**
- **File:** `models/recipe_matcher.py`
- **Algorithm:** TF-IDF + Cosine Similarity
- **Input:** List of ingredients
- **Output:** Top N matching recipes
- **Performance:** <0.1s for 231k recipes

### **2. Content Recommender**
- **File:** `models/content_recommender.py`
- **Features:** Ingredients (65%), Tags (30%), Time (5%)
- **Algorithm:** TF-IDF vectorization + weighted similarity
- **Coverage:** 100% (all recipes)

### **3. Collaborative Recommender**
- **File:** `models/collaborative_recommender.py`
- **Algorithm:** Item-based co-occurrence
- **Data:** 1.1M user ratings
- **Metrics:** Jaccard, confidence, support
- **Coverage:** ~98% (recipes with ≥3 ratings)

### **4. Hybrid Recommender**
- **File:** `models/hybrid_recommender.py`
- **Fusion:** 50/50 weighted combination
- **Normalization:** Min-max scaling
- **Fallback:** Content-only for sparse data

### **5. Cooking Time Predictor**
- **File:** `models/cooking_time_predictor.py`
- **Algorithm:** Random Forest (100 trees)
- **Features:** Steps, ingredients, extracted time, cooking methods
- **Performance:** R² = 0.499, MAE = 14.8 min
- **Model:** Saved to `models/saved/time_predictor.pkl`

### **6. Recipe Simplifier**
- **File:** `models/recipe_simplifier.py`
- **Model:** Claude Sonnet 4 (Anthropic API)
- **Temperature:** 0.3 (consistent output)
- **Max Tokens:** 2000

---

## 🔨 Development

### **Run Development Server**

```bash
# With auto-reload
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# With custom log level
LOG_LEVEL=DEBUG uvicorn src.main:app --reload
```

### **Adding New Endpoints**

1. Create route in `src/routers/recipe.py`
2. Define request/response schemas in `schemas/`
3. Add dependency injection if needed
4. Test via `/docs`

### **Model Management**

Models are loaded once at startup via singleton pattern:

```python
# In src/dependencies.py
class ModelState:
    def initialize(self):
        self.recommender_manager = get_recommender_manager()
        # Models loaded once, shared across all requests
```

**Benefits:**
- 30s initial load → <0.1s per request
- 50% memory savings vs loading per-request

---

## 📊 Performance Optimization

### **Current Optimizations**

1. **Singleton Pattern** - Models loaded once (30s → 0.1s)
2. **TF-IDF Caching** - Vectors computed at startup
3. **DataFrame Indexing** - Fast recipe lookups
4. **Async Endpoints** - Non-blocking I/O

### **Future Optimizations** (TODO)

- [ ] Redis caching for frequent requests
- [ ] Model quantization for faster inference
- [ ] Batch prediction for time predictor
- [ ] Database for user interactions (Phase 2)

---

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [scikit-learn Documentation](https://scikit-learn.org/)
- [Anthropic API Docs](https://docs.anthropic.com/)

---