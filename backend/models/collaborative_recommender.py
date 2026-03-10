from collections import defaultdict

from schemas.recipe import Recipe
from schemas.recipe_recommendation import RecipeRecommendation
from schemas.recommendation_response import RecommendationResponse


class CollaborativeRecommender:
    def __init__(self, recipes, interactions, min_rating=4, min_common_users=3):
        self.min_rating = min_rating
        self.min_common_users = min_common_users

        self.recipes = recipes
        self.interactions = interactions
        self.recipe_user = {} # recipe_id : set of user id

        self._build_user_map()


    def _build_user_map(self):
        for _, row in self.interactions.iterrows():
            recipe_id = row['recipe_id']
            user_id = row['user_id']

            if recipe_id not in self.recipe_user:
                self.recipe_user[recipe_id] = set()

            self.recipe_user[recipe_id].add(user_id)

        print(f"Built a map of {len(self.recipe_user):,} recipes")


    def find_similar(self, target_recipe:Recipe, top_n=10):
        target_recipe_id = target_recipe.id
        if target_recipe_id not in self.recipe_user:
            response = RecommendationResponse(
                target=target_recipe,
                status='error',
                top_n=top_n,
                strategy='collaborative',
                recommendations=[],
                error_message=f"{target_recipe['name']} is not found in the recipe_user"
            )
            return response

        # get users who liked it
        users_liked_target = self.recipe_user[target_recipe_id]
        if len(users_liked_target) < self.min_common_users:
            response = RecommendationResponse(
                target=target_recipe,
                status='error',
                top_n=top_n,
                strategy='collaborative',
                recommendations=[],
                error_message=f"{target_recipe['name']} has too few ratings ({len(users_liked_target)})"
            )
            return response

        # find co-occurrence
        co_occurrence = defaultdict()
        for other_recipe_id, other_users in self.recipe_user.items():
            if other_recipe_id == target_recipe_id:
                continue

            common_users = other_users & users_liked_target
            num_common = len(common_users)
            if num_common >= self.min_common_users: # only if # of common users >= min common users (3)
                co_occurrence[other_recipe_id] = num_common

        # sort by occurrence count until top n
        sorted_occurrence = sorted(
            co_occurrence.items(),
            key=lambda x: x[1],
            reverse=True
        )[:top_n]

        # build result
        recommendations = []
        for other_recipe_id, count in sorted_occurrence:
            other_users = self.recipe_user[other_recipe_id]
            union_size = len(users_liked_target | other_users)

            jaccard = count / union_size if union_size > 0 else 0 # % of common / target + other
            confidence = count / len(users_liked_target) if len(users_liked_target) > 0 else 0 # % of common / target
            support = count / len(other_users) if len(other_users) > 0 else 0 # % of comon / other

            max_possible_common = min(len(users_liked_target), len(other_users))
            normalized_score = count / max_possible_common if max_possible_common > 0 else 0

            recipe_row = self.recipes[self.recipes['id'] == other_recipe_id].iloc[0]
            recipe = Recipe.get_recipe_dataframe_from_row(recipe_row)
            rec = RecipeRecommendation(
                recipe=recipe,
                similarity_score=normalized_score,
                common_users=count,
                jaccard=jaccard,
                support=support,
                confidence=confidence
            )
            recommendations.append(rec)

        response = RecommendationResponse(
            target=target_recipe,
            status='success',
            top_n=top_n,
            strategy='collaborative',
            recommendations=recommendations
        )

        return response
