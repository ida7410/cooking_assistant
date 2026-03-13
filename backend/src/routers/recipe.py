from fastapi import APIRouter, HTTPException, Depends

from models import CookingTimePredictor, RecipeSimplifier
from models.recommender_manager import RecommenderManager
from schemas import Recipe, RecipeSearchRequest, SimplifyRequest
from schemas.recipe_response import RecipeResponse
from schemas.recommendation_request import RecommendationRequest
from src.dependencies import (
    get_rec_manager,
    get_recipe_matcher,
    get_time_predictor,
    get_recipe_simplifier
)

router = APIRouter(prefix="/api/recipe", tags=["recipe"])

@router.get("/{recipe_id}", response_model=RecipeResponse)
async def get_recipe(
        recipe_id: int,
        recommender_manager: RecommenderManager = Depends(get_rec_manager),
        time_predictor: CookingTimePredictor = Depends(get_time_predictor)
):
    try:
        recommender_manager._load_data()
        
        recipe_df = recommender_manager.recipes
        recipe_row = recipe_df[recipe_df['id'] == recipe_id]
        if recipe_row.empty:
            raise HTTPException(status_code=404, detail=f"Recipe (id: {recipe_id}) is not found.")

        recipe = Recipe.get_recipe_dataframe_from_row(recipe_row.iloc[0])
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


@router.post("/search")
async def search_recipes(
        request: RecipeSearchRequest,
        recipe_matcher = Depends(get_recipe_matcher),
        time_predictor: CookingTimePredictor = Depends(get_time_predictor),
        recipe_simplifier: RecipeSimplifier = Depends(get_recipe_simplifier)
):
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
                    recipe_name=rec.recipe.name,
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


@router.post("/simplify")
async def simplify_recipe(
        request: SimplifyRequest,
        recommender_manager: RecommenderManager = Depends(get_rec_manager),
        recipe_simplifier: RecipeSimplifier = Depends(get_recipe_simplifier)
):
    try:
        recipe_id = request.recipe_id
        recipe_df = recommender_manager.recipes
        recipe_row = recipe_df[recipe_df['id'] == recipe_id]
        if recipe_row.empty:
            raise HTTPException(status_code=404, detail=f"Recipe (id: {recipe_id}) is not found.")

        recipe = Recipe.get_recipe_dataframe_from_row(recipe_row.iloc[0])
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


@router.post('/recommend')
async def get_recommendation(
        request: RecommendationRequest,
        recommender_manager: RecommenderManager = Depends(get_rec_manager)
):
    try:
        recipe_id = request.recipe_id
        recipe_df = recommender_manager.recipes
        recipe_row = recipe_df[recipe_df['id'] == recipe_id]
        if recipe_row.empty:
            raise HTTPException(status_code=404, detail=f"Recipe (id: {recipe_id}) is not found.")

        recipe = Recipe.get_recipe_dataframe_from_row(recipe_row.iloc[0])
        recommendation = recommender_manager.recommend(recipe, request.top_n, request.strategy)
        return recommendation
    except HTTPException as e:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
