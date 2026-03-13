from typing import Optional

from fastapi import HTTPException

from models import RecipeSimplifier, RecipeMatcher, CookingTimePredictor
from models.recommender_manager import RecommenderManager, get_recommender_manager
from src.logger import get_logger

logger = get_logger(__name__)


class ModelState:
    def __init__(self):
        self.recommender_manager: Optional[RecommenderManager] = None
        self.recipe_simplifier: Optional[RecipeSimplifier] = None
        self.recipe_matcher: Optional[RecipeMatcher] = None
        self.time_predictor: Optional[CookingTimePredictor] = None

    def initialize(self):
        logger.info("Loading models...")
        self.recommender_manager = get_recommender_manager()
        logger.info("Recommender manager loaded")
        self.recipe_matcher = RecipeMatcher()
        logger.info("Recipe matcher loaded")
        self.time_predictor = CookingTimePredictor()
        logger.info("Time predictor loaded")
        self.recipe_simplifier = RecipeSimplifier()
        logger.info("Recipe simplifier loaded\n")


    def preload_data(self):
        logger.info("Preloading data...")

        try:
            if self.recommender_manager:
                self.recommender_manager._load_data()
                logger.info("Recommender data preloaded")
            if self.recipe_matcher:
                self.recipe_matcher._load_data()
                logger.info("Recipe matcher preloaded")
            if self.time_predictor:
                self.time_predictor._ensure_model_loaded()
                logger.info("Time predictor data preloaded")

            logger.info("All data successfully loaded")
        except Exception as e:
            logger.error(f"Error while preloading data {e}")


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
