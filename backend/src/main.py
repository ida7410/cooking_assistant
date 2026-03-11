from datetime import datetime

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import config
from models.cooking_time_predictor import CookingTimePredictor
from models.recipe_matcher import RecipeMatcher
from models.recipe_simplifier import RecipeSimplifier
from models.recommender_manager import get_recommender_manager
from schemas import Recipe, RecipeSearchRequest, SimplifyRequest
from schemas.recommendation_request import RecommendationRequest

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


@app.get("/api/recipes/{recipe_id}")
async def get_recipe(recipe_id: int):
    try:
        recipe_df = recommender_manager.recipes
        recipe_row = recipe_df[recipe_df['id'] == recipe_id].iloc[0]
        if recipe_row.empty:
            raise HTTPException(status_code=404, detail=f"Recipe (id: {recipe_id}) is not found.")

        recipe = Recipe.get_recipe_dataframe_from_row(recipe_row)
        predicted_times = {}
        for skill in ['beginner', 'intermediate', 'expert']:
            prediction = time_predictor.predict(
                recipe_row={
                    'n_steps': recipe.n_steps,
                    'n_ingredients': recipe.n_ingredients,
                    'steps': ' '.join(recipe.steps)
                },
                skill_level=skill
            )
            predicted_times[skill] = prediction['adjusted_time']

        return {
            "recipe": recipe,
            "predicted_time": {
                "base_time": recipe.cooking_time,
                **predicted_times
            }
        }

    except HTTPException as e:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/recipe/search")
async def search_recipes(request: RecipeSearchRequest):
    try:
        results = recipe_matcher.find_matches(
            user_ingredients=request.ingredients,
            top_n=request.top_n
        )

        enhanced_recommendations = []
        for rec in results.recommendations:
            # predict cooking time
            time_prediction = time_predictor.predict(
                recipe_row={
                    'n_steps': rec.recipe.n_steps,
                    'n_ingredients': rec.recipe.n_ingredients,
                    'steps': ' '.join(rec.recipe.steps)
                },
                skill_level=request.skill_level
            )

            simplified = None
            if request.simplify_steps:
                simplified = recipe_simplifier.simplify(
                    recipe_name=rec.recipe.recipe_name,
                    steps=rec.recipe.steps
                )

            enhanced_rec = {
                "recipe": rec.recipe,
                "similarity_score": rec.similarity_score,
                "predicted_time": time_prediction['adjusted_time'],
                "time_breakdown": time_prediction,
                "simplified_steps": simplified
            }
            enhanced_recommendations.append(enhanced_rec)

        return enhanced_recommendations

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/recipe/simplify")
async def simplify_recipe(request: SimplifyRequest):
    try:
        recipe_id = request.recipe_id
        recipe_df = recommender_manager.recipes
        recipe_row = recipe_df[recipe_df['id'] == recipe_id].iloc[0]
        if recipe_row.empty:
            raise HTTPException(status_code=404, detail=f"Recipe (id: {recipe_id}) is not found.")

        recipe = Recipe.get_recipe_dataframe_from_row(recipe_row)
        simplified_steps = recipe_simplifier.simplify(
            recipe_name=recipe.name,
            steps=recipe.steps,
            difficulty = request.skill_level
        )

        return {
            "recipe_id": recipe_id,
            "recipe_name": recipe.name,
            "original_steps": recipe.steps,
            "simplified_steps": simplified_steps,
            "skill_level": request.skill_level
        }
    except HTTPException as e:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post('/api/recipe/recommend')
async def get_recommendation(request: RecommendationRequest):
    try:
        recipe_id = request.recipe_id
        recipe_df = recommender_manager.recipes
        recipe_row = recipe_df[recipe_df['id'] == recipe_id].iloc[0]
        if recipe_row.empty:
            raise HTTPException(status_code=404, detail=f"Recipe (id: {recipe_id}) is not found.")

        recipe = Recipe.get_recipe_dataframe_from_row(recipe_row)
        recommendation = recommender_manager.recommend(recipe, request.top_n, request.strategy)
        return recommendation
    except HTTPException as e:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
