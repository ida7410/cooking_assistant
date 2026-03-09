import pandas as pd
from pathlib import Path
from collections import defaultdict


class CollaborativeRecommender:
    def __init__(self, data_path='data/RAW_interactions.csv', min_rating=4, min_common_users=3):
        self.data_path = Path(data_path)
        self.min_rating = min_rating
        self.min_common_users = min_common_users

        self.df = None
        self.recipe_user = {} # recipe_id : set of user id

        self._load_data()
        self._build_user_map()


    def _load_data(self):
        print("Loading data...")
        self.df = pd.read_csv(self.data_path)
        print(f"Loaded {len(self.df)} rows")


    def _build_user_map(self):
        for _, row in self.df.iterrows():
            recipe_id = row['recipe_id']
            user_id = row['user_id']

            if recipe_id not in self.recipe_user:
                self.recipe_user[recipe_id] = set()

            self.recipe_user[recipe_id].add(user_id)

        print(f"Built a map of {len(self.recipe_user):,} recipes")


    def find_similar(self, target_recipe_id, top_n=10):
        if target_recipe_id not in self.recipe_user:
            return {
                "error": f"{target_recipe_id} is not found",
                "recommendations": []
            }

        # get users who liked it
        users_liked_target = self.recipe_user[target_recipe_id]
        if len(users_liked_target) < self.min_common_users:
            return {
                "error": f"Recipe {target_recipe_id} has too few ratings ({len(users_liked_target)})",
                "recommendations": []
            }

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

            recommendations.append({
                "recipe_id": int(other_recipe_id),
                "common_users": count,
                "total_users_liked_other": int(len(self.recipe_user[other_recipe_id])),
                "jaccard": jaccard,
                "support": support,
                "confidence": confidence,
                "normalized": normalized_score
            })

        result = {
            "target_recipe_id": target_recipe_id,
            'top_n': top_n,
            'strategy': 'collaborative',
            "total_users_liked_target": int(len(users_liked_target)),
            "recommendations": recommendations
        }

        return result
