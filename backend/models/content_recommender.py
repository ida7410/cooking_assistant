import ast

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from schemas.recipe import Recipe
from schemas.recipe_recommendation import RecipeRecommendation
from schemas.recommendation_response import RecommendationResponse


class ContentRecommender:
    def __init__(self, recipes, ingredient_weights=0.65, tags_weights=0.3, time_weights=0.05):
        # load data
        self.recipes = recipes
        self.ingredient_vectorizer = None
        self.ingredient_vector = None
        self.tag_vectorizer = None
        self.tag_vector = None

        # weights
        self.INGREDIENT_WEIGHTS = ingredient_weights
        self.TAG_WEIGHTS = tags_weights
        self.TIME_WEIGHTS = time_weights

        self._prepare_features()


    def _prepare_features(self):
        # Ingredient Vectors
        print("Preparing ingredient vectors...")

        # convert ingredient list to text
        self.recipes['ingredients_text'] = self.recipes['ingredients'].apply(
            lambda x: ' '.join(ast.literal_eval(x) if pd.notna(x) else x)
        )

        # create TF-ID vector for ingredients
        self.ingredient_vectorizer = TfidfVectorizer(max_features=5000)
        self.ingredient_vector = self.ingredient_vectorizer.fit_transform(self.recipes['ingredients'])
        print("Ingredient vectors prepared")


        # Tag Vectors
        print("Preparing tag vectors...")

        # convert ingredient list to text
        self.recipes['tags_text'] = self.recipes['tags'].apply(
            lambda x: ' '.join(ast.literal_eval(x) if pd.notna(x) else x)
        )

        # create TF-ID vector for ingredients
        self.tag_vectorizer = TfidfVectorizer(max_features=5000)
        self.tag_vector = self.ingredient_vectorizer.fit_transform(self.recipes['tags'])
        print("Tag vectors prepared")


    def _calculate_time_similarity(self, time1, time2):
        """Returns 1.0 (very similar, < 10 mins diff) ~ 0.0 (not similar >= 60 mins diff)"""

        time_diff = abs(time1 - time2)
        if time_diff < 10:
            return 1.0
        elif time_diff >= 60:
            return 0.0
        else:
            return 1 - (time_diff / 50)


    def find_similar(self, target_recipe:Recipe, top_n=10):
        target_recipe_id = target_recipe.id

        # find recipe index
        try:
            target_recipe_idx = self.recipes[self.recipes['id'] == target_recipe_id].index[0]
        except IndexError as e:
            response = RecommendationResponse(
                target=target_recipe,
                status='error',
                top_n=top_n,
                strategy='content',
                recommendations=[],
                error_message=f"{target_recipe.name} is not found in the recipes"
            )
            return response

        # get recipe info
        recipe_time = target_recipe.cooking_time

        # calculate ingredient similarity
        ingredient_sim = cosine_similarity(
            self.ingredient_vector[target_recipe_idx:target_recipe_idx + 1],
            self.ingredient_vector
        )[0]

        # calculate tag similarity
        tag_sim = cosine_similarity(
            self.tag_vector[target_recipe_idx:target_recipe_idx + 1],
            self.tag_vector
        )[0]

        # calculate time similarity
        time_sim = np.array([
            self._calculate_time_similarity(recipe_time, other_time)
            for other_time in self.recipes['minutes']
        ])

        # combine scores with weights
        final_scores = (
                self.INGREDIENT_WEIGHTS * ingredient_sim
                + self.TAG_WEIGHTS * tag_sim
                + self.TIME_WEIGHTS * time_sim
        )
        print(final_scores.shape)

        # get top N
        final_scores[target_recipe_idx] = -1
        top_indices = final_scores.argsort()[-top_n:][::-1]

        # build response
        recommendations = []
        for i in top_indices:
            recipe_row = self.recipes.iloc[i]
            recipe = Recipe.get_recipe_dataframe_from_row(recipe_row)
            rec = RecipeRecommendation(
                recipe=recipe,
                similarity_score=float(final_scores[i]),
                ingredient_similarity=float(ingredient_sim[i]),
                tag_similarity=float(tag_sim[i]),
                time_similarity=float(time_sim[i])
            )
            recommendations.append(rec)

        response = RecommendationResponse(
            target=target_recipe,
            status='success',
            top_n=top_n,
            strategy='content',
            recommendations=recommendations
        )

        return response
