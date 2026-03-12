# 🍳 Cooking Assistant

> AI-powered recipe recommendation system with ML-based similarity matching and personalized cooking insights

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-14-black.svg)](https://nextjs.org/)

---

## 🎯 Project Overview

**Cooking Assistant** is a full-stack machine learning application that helps users discover recipes based on available ingredients and provides personalized cooking recommendations. Built as a portfolio project demonstrating production-ready ML engineering and modern web development practices.

### **Key Features**

- 🔍 **Smart Recipe Search** - Find recipes using ingredients you have on hand
- 🤖 **ML-Powered Recommendations** - Hybrid recommendation system combining content-based and collaborative filtering
- ⏱️ **Cooking Time Prediction** - Personalized time estimates based on skill level
- 📚 **Recipe Simplification** - AI-generated beginner-friendly instructions using Claude API
- 📊 **Data-Driven Insights** - Built on 231k+ recipes and 1.1M+ user ratings from Food.com

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (Next.js 14)                     │
│                  TypeScript + Tailwind CSS                   │
└────────────────────────┬────────────────────────────────────┘
                         │ REST API
┌────────────────────────▼────────────────────────────────────┐
│                   Backend (FastAPI)                          │
│                 Python 3.10+ + Pydantic                      │
├──────────────────────────────────────────────────────────────┤
│                    ML Models Layer                           │
│  ┌─────────────┬──────────────┬──────────────┬────────────┐ │
│  │  Recipe     │ Recommender  │    Time      │   Recipe   │ │
│  │  Matcher    │  (Hybrid)    │  Predictor   │ Simplifier │ │
│  │  (TF-IDF)   │ (Content +   │ (Random      │  (Claude   │ │
│  │             │  Collab)     │  Forest)     │   API)     │ │
│  └─────────────┴──────────────┴──────────────┴────────────┘ │
└──────────────────────────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│                    Data Layer                                │
│   231,637 recipes • 1,132,367 user ratings (Food.com)       │
└──────────────────────────────────────────────────────────────┘
```

---

## 🚀 Tech Stack

### **Backend**
- **Framework:** FastAPI 0.104+
- **ML/Data:** scikit-learn, pandas, numpy
- **NLP:** TF-IDF vectorization (5000 features)
- **AI:** Anthropic Claude API (recipe simplification)
- **Validation:** Pydantic v2

### **Frontend**
- **Framework:** Next.js 14 (App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **Components:** shadcn/ui

### **Infrastructure**
- **Deployment:** Vercel (frontend) + Railway (backend)
- **CI/CD:** GitHub Actions
- **Version Control:** Git + GitHub

---

## 📊 ML Models

### **1. Recipe Matcher** 
- **Algorithm:** TF-IDF + Cosine Similarity
- **Input:** User ingredients list
- **Output:** Top N matching recipes with similarity scores
- **Performance:** Sub-second search across 231k recipes

### **2. Hybrid Recommender**
- **Content-Based:** 65% ingredients, 30% tags, 5% cooking time
- **Collaborative:** Item-based co-occurrence filtering on 1.1M ratings
- **Fusion:** 50/50 weighted combination with min-max normalization
- **Fallback:** Content-only mode for recipes with sparse interaction data

### **3. Cooking Time Predictor**
- **Algorithm:** Random Forest Regressor (100 estimators)
- **Features:** Steps count, ingredients count, extracted time, cooking methods
- **Performance:** R² = 0.499, MAE = 14.8 minutes
- **Personalization:** Adjusts for beginner/intermediate/expert skill levels

### **4. Recipe Simplifier**
- **Model:** Claude Sonnet 4 (Anthropic API)
- **Function:** Converts complex culinary terms into beginner-friendly language
- **Output:** Step-by-step instructions with timing and visual cues

---

## 📁 Project Structure

```
cooking-assistant/
├── backend/                      # FastAPI application
│   ├── src/                      # Application code
│   │   ├── main.py              # FastAPI app entry point
│   │   ├── dependencies.py      # Dependency injection
│   │   ├── logger.py            # Logging configuration
│   │   └── routers/             # API route handlers
│   ├── models/                   # ML models
│   │   ├── content_recommender.py
│   │   ├── collaborative_recommender.py
│   │   ├── hybrid_recommender.py
│   │   ├── recipe_matcher.py
│   │   ├── cooking_time_predictor.py
│   │   ├── recipe_simplifier.py
│   │   └── recommender_manager.py
│   ├── schemas/                  # Pydantic data models
│   ├── data/                     # Dataset files
│   ├── config.py                 # Configuration
│   └── requirements.txt
│
├── frontend/                     # Next.js application
│   ├── app/                      # App router pages
│   ├── components/               # React components
│   ├── lib/                      # Utilities
│   └── types/                    # TypeScript types
│
├── .github/                      # GitHub workflows
│   └── workflows/
│       ├── backend-tests.yml
│       └── frontend-tests.yml
│
├── docs/                         # Documentation
└── README.md                     # This file
```

---

## 🛠️ Installation & Setup

### **Prerequisites**
- Python 3.10+
- Node.js 18+
- npm or yarn

### **Backend Setup**

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY

# Run development server
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

API will be available at `http://localhost:8000`  
Interactive docs at `http://localhost:8000/docs`

### **Frontend Setup**

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Setup environment variables
cp .env.example .env.local
# Edit .env.local and set NEXT_PUBLIC_API_URL

# Run development server
npm run dev
```

Application will be available at `http://localhost:3000`

---

## 📖 API Documentation

### **Core Endpoints**

#### **Search Recipes**
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

#### **Get Recipe Details**
```http
GET /api/recipe/{recipe_id}
```

#### **Get Recommendations**
```http
POST /api/recipe/recommend

{
  "recipe_id": 2886,
  "top_n": 10,
  "strategy": "hybrid"  // "content" | "collaborative" | "hybrid"
}
```

#### **Simplify Recipe**
```http
POST /api/recipe/simplify

{
  "recipe_id": 2886,
  "skill_level": "beginner" // "beginner" | "intermediate" | "expert"
}
```

**Full API documentation:** `http://localhost:8000/docs`

---

## 📈 Performance Metrics

| Model | Metric | Value |
|-------|--------|-------|
| Time Predictor | R² Score | 0.499 |
| Time Predictor | MAE | 14.8 minutes |
| Recipe Matcher | Search Time | <0.1s |
| Hybrid Recommender | Cold Start Coverage | 100% |
| Data Loading | Initial Load | ~30s |
| Data Loading | Subsequent Requests | <0.1s |

---

## 🔬 Technical Highlights

### **Architecture Patterns**
- **Singleton Pattern** - Models loaded once at startup, shared across requests
- **Dependency Injection** - FastAPI dependencies for clean code organization
- **Type Safety** - Pydantic validation across all API boundaries
- **Structured Logging** - Environment-based log levels (DEBUG/INFO/WARNING/ERROR)
- **Error Handling** - Graceful degradation with informative messages

### **Machine Learning**
- **Feature Engineering** - Text extraction from recipe steps for time prediction
- **Hybrid System** - Combined content + collaborative filtering with score normalization
- **Sparse Data Handling** - Fallback strategies for recipes with limited ratings
- **Model Caching** - Pickle serialization for trained models

### **Performance**
- **Efficient Loading** - Singleton pattern reduces memory by 50%
- **Fast Search** - TF-IDF vectorization enables sub-second queries
- **Optimized Predictions** - Pre-computed vectors for instant recommendations

---

## 🚀 Deployment

### **Backend (Railway)**
```bash
# Environment variables required:
ENVIRONMENT=production
ANTHROPIC_API_KEY=your_key_here
LOG_LEVEL=INFO
```

### **Frontend (Vercel)**
```bash
# Environment variables required:
NEXT_PUBLIC_API_URL=https://your-backend.railway.app
```

---

## 📊 Dataset

**Source:** [Food.com Recipes and Interactions](https://www.kaggle.com/datasets/shuyangli94/food-com-recipes-and-user-interactions)

- **Recipes:** 231,637 unique recipes
- **Interactions:** 1,132,367 user ratings
- **Date Range:** 2000-2018
- **Coverage:** All recipes have ≥1 rating

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📮 Contact

For questions or opportunities, reach out via [GitHub Issues](https://github.com/ida7410/cooking_assistant/issues) or LinkedIn.

---