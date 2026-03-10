from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import config
from models.cooking_time_predictor import CookingTimePredictor
from models.recipe_matcher import RecipeMatcher
from models.recipe_simplifier import RecipeSimplifier
from models.recommender_manager import get_recommender_manager

app = FastAPI(
    title=config.API_TITLE,
    description=config.API_DESCRIPTION,
    version=config.API_VERSION
)

# CORS middleware with config
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# load model on startup
recommender_manager = get_recommender_manager()
recipe_matcher = RecipeMatcher()
time_predictor = CookingTimePredictor()
recipe_simplifier = RecipeSimplifier()
@app.on_event("startup")
async def startup():
    global recommender_manager, recipe_matcher, time_predictor, recipe_simplifier
    print("Loading models...")
    recommender_manager = get_recommender_manager()
    print("Recommender manager loaded")
    recipe_matcher = RecipeMatcher()
    print("Recipe matcher loaded")
    time_predictor = CookingTimePredictor()
    print("Time predictor loaded")
    recipe_simplifier = RecipeSimplifier()
    print("Recipe simplifier loaded\n")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "name": "Cooking Assistant API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/api/health",
            "search": "POST /api/recipes/search",
            "recipe_detail": "GET /api/recipes/{id}",
            "recommendations": "GET /api/recipes/{id}/recommendations",
            "simplify": "POST /api/recipes/{id}/simplify"
        }
    }


@app.get("/api/health")
async def health():
    return {
        "status": "healthy",
        "models_loaded": True,
        "timestamp": datetime.now().isoformat(),
        "components": {
            "recipe_matcher": "ready",
            "time_predictor": "ready",
            "recipe_simplifier": "ready",
            "content_recommender": "ready",
            "collaborative_recommender": "ready",
            "hybrid_recommender": "ready"
        }
    }
