import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from schemas.recipe import Recipe
from schemas.recipe_recommendation import RecipeRecommendation
from schemas.recommendation_response import RecommendationResponse
from src.logger import get_logger

logger = get_logger(__name__)


class RecipeMatcher:
    def __init__(self):
        # load recipes
        self.recipes = None
        self.vectorizer = None
        self.recipe_vectors = None


    def _load_data(self):
        if self.recipes is None:
            import os
            if os.path.exists('/data/RAW_recipes.csv'):
                logger.info("Loading recipes & interactions...")
                self.recipes = pd.read_csv('/data/RAW_recipes.csv')
                logger.info("Data loaded successfully")

                # create ingredient vectors
                self.vectorizer = TfidfVectorizer()
                self.recipe_vectors = self.vectorizer.fit_transform(
                    self.recipes['ingredients'].astype(str)
                )
                logger.info("Vectorization for ingredients completed")
            else:
                raise FileNotFoundError(
                    "Data files not found. Please upload RAW_recipes.csv via /upload-file endpoint"
                )

    def find_matches(self, user_ingredients, top_n=5):
        self._load_data()
        # convert user ingredients to vector
        user_text = ' '.join(user_ingredients)
        user_vector = self.vectorizer.transform([user_text])

        # calculate similarity
        similarities = cosine_similarity(user_vector, self.recipe_vectors)[0]

        # get top matches
        top_indices = similarities.argsort()[-top_n:][::-1]

        recommendations = []
        for i in top_indices:
            recipe_row = self.recipes.iloc[i]
            recipe = Recipe.get_recipe_dataframe_from_row(recipe_row)
            rec = RecipeRecommendation(
                recipe=recipe,
                similarity_score=similarities[i]
            )
            recommendations.append(rec)

        response = RecommendationResponse(
            target=user_ingredients,
            status='success',
            top_n=top_n,
            strategy='matcher',
            recommendations=recommendations
        )

        return response

    def _estimate_difficulty(self, recipe_row):
        """Estimate difficulty based on steps and ingredients"""
        n_steps = recipe_row.get('n_steps', 0)
        n_ingredients = recipe_row.get('n_ingredients', 0)

        # Simple heuristic
        if n_steps <= 5 and n_ingredients <= 7:
            return "Easy"
        elif n_steps <= 10 and n_ingredients <= 12:
            return "Medium"
        else:
            return "Hard"
