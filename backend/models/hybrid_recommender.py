import pandas as pd
import numpy as np
from content_recommender import ContentRecommender
from collaborative_recommender import CollaborativeRecommender

class HybridRecommender:
    def __init__(self, min_rating=4, min_common_users=3):
        self.min_rating = min_rating
        self.min_common_users = min_common_users
        self.content_recommender = ContentRecommender()
        self.collab_recommender = CollaborativeRecommender()


    def _normalize(self, scores):
        values = list(scores.values())
        min_score = np.min(values)
        max_score = np.max(values)

        if min_score == max_score:
            return {k: 1.0 for k in scores.keys()}

        normalized = {
            recipe_id: (score - min_score) / (max_score - min_score)
            for recipe_id, score in scores.items()
        }

        return normalized


    def find_similar(self, recipe_id, top_n):
        content_rec = self.content_recommender.find_similar(recipe_id, 50)
        collab_rec = self.collab_recommender.find_similar(recipe_id, 50)

        content_scores = {} if 'error' in content_rec else {
            rec['recipe_id']: rec['similarity_score']
            for rec in content_rec['recommendations']
        }
        collab_scores = {} if 'error' in collab_rec else {
            rec['recipe_id']: rec['normalized']
            for rec in collab_rec['recommendations']
        }

        content_norm = self._normalize(content_scores)
        collab_norm = self._normalize(collab_scores)

        all_recipes = set(content_norm.keys()) | set(collab_norm.keys())

        hybrid_scores = {}
        for recipe_id in all_recipes:
            content_score = content_scores.get(recipe_id, 0)
            collab_score = collab_scores.get(recipe_id, 0)

            hybrid_score = 0.5 * content_score + 0.5 * collab_score
            hybrid_scores[recipe_id] = {
                'hybrid_score': hybrid_score,
                'content_score': content_score,
                'collab_score': collab_score,
                'in_both': (recipe_id in collab_norm) and (recipe_id in content_norm)
            }

        sorted_recipes = sorted(
            hybrid_scores.items(),
            key=lambda item: item[1]['hybrid_score'],
            reverse=True
        )[:top_n]

        recommendations = []
        for recipe_id, score in sorted_recipes:
            recommendations.append({
                'recipe_id': recipe_id,
                'hybrid_score': score['hybrid_score'],
                'content_score': score['content_score'],
                'collab_score': score['collab_score'],
                'in_both': score['in_both']
            })

        result = {
            'target_recipe_id': recipe_id,
            'top_n': top_n,
            'strategy': 'hybrid',
            'recommendations': recommendations
        }
        return result


def main():
    recommender = HybridRecommender()
    test_id = 2886
    result = recommender.find_similar(test_id, 10)
    recipes_df = pd.read_csv('data/RAW_recipes.csv')

    for i, rec in enumerate(result['recommendations'], 1):
        rec_name = recipes_df[recipes_df['id'] == rec['recipe_id']]['name'].values[0]

        print(f"{i}. {rec_name}")
        print(f"   Hybrid Score: {rec['hybrid_score']:.3f}")
        print(f"   └─ Content: {rec['content_score']:.3f} | Collaborative: {rec['collab_score']:.3f}")

        if rec['in_both']:
            print(f"   ⭐ In BOTH lists (strong signal!)")

        print()


if __name__ == '__main__':
    main()