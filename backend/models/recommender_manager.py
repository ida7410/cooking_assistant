from content_recommender import ContentRecommender
from collaborative_recommender import CollaborativeRecommender
from hybrid_recommender import HybridRecommender

class RecommenderManager:

    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RecommenderManager, cls).__new__(cls)
        return cls._instance


    def __init__(self):
        if not RecommenderManager._initialized:
            print("Initializing recommender manager...")
            self.content_recommender = None
            self.collab_recommender = None
            self.hybrid_recommender = None
            RecommenderManager._initialized = True


    def get_content_recommender(self):
        print("Loading content recommender...")
        if self.content_recommender is None:
            self.content_recommender = ContentRecommender()
        print("Content recommender Loaded")
        return self.content_recommender


    def get_collab_recommender(self):
        print("Loading collab recommender...")
        if self.collab_recommender is None:
            self.collab_recommender = CollaborativeRecommender()
        print("Collab recommender Loaded")
        return self.collab_recommender


    def get_hybrid_recommender(self):
        print("Loading hybrid recommender...")
        if self.hybrid_recommender is None:
            content_recommender = self.get_content_recommender()
            collab_recommender = self.get_collab_recommender()
            self.hybrid_recommender = HybridRecommender(content_recommender, collab_recommender)
        print("Hybrid recommender Loaded")
        return self.hybrid_recommender


_manager = RecommenderManager()
def get_recommender_manager():
    return _manager