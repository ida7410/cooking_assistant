from typing import Optional

from fastapi import HTTPException

from models import RecipeSimplifier, RecipeMatcher, CookingTimePredictor
from models.recommender_manager import RecommenderManager, get_recommender_manager


class ModelState:
    def __init__(self):
        self.recommender_manager: Optional[RecommenderManager] = None
        self.recipe_simplifier: Optional[RecipeSimplifier] = None
        self.recipe_matcher: Optional[RecipeMatcher] = None
        self.time_predictor: Optional[CookingTimePredictor] = None

    def initialize(self):
        print("Loading models...")
        self.recommender_manager = get_recommender_manager()
        print("Recommender manager loaded")
        self.recipe_matcher = RecipeMatcher()
        print("Recipe matcher loaded")
        self.time_predictor = CookingTimePredictor()
        print("Time predictor loaded")
        self.recipe_simplifier = RecipeSimplifier()
        print("Recipe simplifier loaded\n")

    def is_ready(self):
        return all([
            self.recommender_manager is not None,
            self.recipe_simplifier is not None,
            self.recipe_matcher is not None,
            self.time_predictor is not None,
        ])


model_state = ModelState()
def get_rec_manager():
    if model_state.recommender_manager is None:
        raise HTTPException(status_code=503, detail="Recommender manager model not loaded")
    return model_state.recommender_manager

def get_recipe_simplifier():
    if model_state.recipe_simplifier is None:
        raise HTTPException(status_code=503, detail="Recipe simplifier model not loaded")
    return model_state.recipe_simplifier

def get_recipe_matcher():
    if model_state.recipe_matcher is None:
        raise HTTPException(status_code=503, detail="Recipe matcher model not loaded")
    return model_state.recipe_matcher

def get_time_predictor():
    if model_state.time_predictor is None:
        raise HTTPException(status_code=503, detail="Time predictor model not loaded")
    return model_state.time_predictor
