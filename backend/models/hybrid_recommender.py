import numpy as np

from models.schemas.recipe import Recipe
from models.schemas.recipe_recommendation import RecipeRecommendation
from models.schemas.recommendation_response import RecommendationResponse


class HybridRecommender:
    def __init__(self, content_recommender, collab_recommender, min_rating=4, min_common_users=3):
        self.min_rating = min_rating
        self.min_common_users = min_common_users
        self.content_recommender = content_recommender
        self.collab_recommender = collab_recommender
        self.recipes = content_recommender.recipes


    def _normalize_scores(self, scores):
        if not scores:
            return {}

        values = list(scores.values())
        if len(values) == 0:
            return {}

        min_score = np.min(values)
        max_score = np.max(values)

        if min_score == max_score:
            return {k: 1.0 for k in scores.keys()}

        normalized = {
            recipe_id: (score - min_score) / (max_score - min_score)
            for recipe_id, score in scores.items()
        }

        return normalized


    def find_similar(self, target_recipe:Recipe, top_n=10):
        content_rec = self.content_recommender.find_similar(target_recipe, 50)
        collab_rec = self.collab_recommender.find_similar(target_recipe, 50)

        content_scores = {} if content_rec.status == 'error' else {
            rec.recipe.id: rec.similarity_score
            for rec in content_rec.recommendations
        }
        collab_scores = {} if collab_rec.status == 'error'  else {
            rec.recipe.id: rec.similarity_score
            for rec in collab_rec.recommendations
        }

        content_norm = self._normalize_scores(content_scores)
        collab_norm = self._normalize_scores(collab_scores)

        all_recipes = set(content_norm.keys()) | set(collab_norm.keys())

        hybrid_scores = {}
        for recipe_id in all_recipes:
            content_score = content_norm.get(recipe_id, 0)
            collab_score = collab_norm.get(recipe_id, 0)

            hybrid_score = 0.5 * content_score + 0.5 * collab_score
            hybrid_scores[recipe_id] = {
                'hybrid_score': hybrid_score,
                'normalized_content_score': content_score,
                'normalized_collab_score': collab_score,
                'in_both': (recipe_id in collab_norm) and (recipe_id in content_norm)
            }

        sorted_recipes = sorted(
            hybrid_scores.items(),
            key=lambda item: item[1]['hybrid_score'],
            reverse=True
        )[:top_n]

        recommendations = []
        for recipe_id, score in sorted_recipes:
            recipe_row = self.recipes[self.recipes['id'] == recipe_id].iloc[0]
            recipe = Recipe.get_recipe_dataframe_from_row(recipe_row)
            rec = RecipeRecommendation(
                recipe=recipe,
                similarity_score=score['hybrid_score'],
                content_score=score['normalized_content_score'],
                collab_score=score['normalized_collab_score'],
                in_both=score['in_both']
            )
            recommendations.append(rec)

        response = RecommendationResponse(
            target=target_recipe,
            status='success',
            top_n=top_n,
            strategy='hybrid',
            recommendations=recommendations
        )
        return response
