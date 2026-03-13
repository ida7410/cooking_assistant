import pandas as pd

from models.content_recommender import ContentRecommender
from models.collaborative_recommender import CollaborativeRecommender
from models.hybrid_recommender import HybridRecommender
from schemas import Recipe
from src.logger import get_logger

logger = get_logger(__name__)


class RecommenderManager:

    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RecommenderManager, cls).__new__(cls)
        return cls._instance


    def __init__(self):
        if not RecommenderManager._initialized:
            logger.info("Initializing recommender manager...")
            self.content_recommender = None
            self.collab_recommender = None
            self.hybrid_recommender = None

            self.recipes = None
            self.interactions = None
            RecommenderManager._initialized = True


    def _load_data(self):
        if self.recipes is None:
            import os
            if os.path.exists('/data/RAW_recipes.csv'):
                logger.info("Loading recipes & interactions...")
                self.recipes = pd.read_csv('/data/RAW_recipes.csv')
                self.interactions = pd.read_csv('/data/RAW_interactions.csv')
                logger.info("Data loaded")
            else:
                raise FileNotFoundError(
                    "Data files not found. Please upload RAW_recipes.csv and RAW_interactions.csv via /upload-file endpoint"
                )


    def get_content_recommender(self):
        logger.info("Loading content recommender...")
        self._load_data()
        if self.content_recommender is None:
            self.content_recommender = ContentRecommender(self.recipes)
        logger.info("Content recommender Loaded")
        return self.content_recommender


    def get_collab_recommender(self):
        logger.info("Loading collab recommender...")
        self._load_data()
        if self.collab_recommender is None:
            self.collab_recommender = CollaborativeRecommender(self.recipes, self.interactions)
        logger.info("Collab recommender Loaded")
        return self.collab_recommender


    def get_hybrid_recommender(self):
        logger.info("Loading hybrid recommender...")
        if self.hybrid_recommender is None:
            content_recommender = self.get_content_recommender()
            collab_recommender = self.get_collab_recommender()
            self.hybrid_recommender = HybridRecommender(content_recommender, collab_recommender)
        logger.info("Hybrid recommender Loaded")
        return self.hybrid_recommender


    def recommend(self, recipe:Recipe, top_n: int, strategy: str):
        if strategy == 'content':
            return self.get_content_recommender().find_similar(recipe, top_n)
        elif strategy == 'collaborative':
            return self.get_collab_recommender().find_similar(recipe, top_n)
        elif strategy == 'hybrid':
            return self.get_hybrid_recommender().find_similar(recipe, top_n)
        else:
            raise ValueError(f"Unknown strategy: {strategy}. Must be 'content', 'collaborative', or 'hybrid'")


_manager = RecommenderManager()
def get_recommender_manager():
    return _manager