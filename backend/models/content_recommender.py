import ast
import os
from typing import final

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pathlib import Path

class ContentRecommender:
    def __init__(self, ingredient_weights=0.65, tags_weights=0.3, time_weights=0.05, data_path='data/RAW_recipes.csv'):
        # load data
        self.data_path = Path(data_path)
        self.df = None
        self.ingredient_vectorizer = None
        self.ingredient_vector = None
        self.tag_vectorizer = None
        self.tag_vector = None

        # weights
        self.INGREDIENT_WEIGHTS = ingredient_weights
        self.TAG_WEIGHTS = tags_weights
        self.TIME_WEIGHTS = time_weights

        self._load_data()
        self._prepare_features()


    def _load_data(self):
        print("Loading data...")
        self.df = pd.read_csv(self.data_path)
        print(f"{len(self.df)} recipes loaded")


    def _prepare_features(self):
        # Ingredient Vectors
        print("Preparing ingredient vectors...")

        # convert ingredient list to text
        self.df['ingredients_text'] = self.df['ingredients'].apply(
            lambda x: ' '.join(ast.literal_eval(x) if pd.notna(x) else x)
        )

        # create TF-ID vector for ingredients
        self.ingredient_vectorizer = TfidfVectorizer(max_features=5000)
        self.ingredient_vector = self.ingredient_vectorizer.fit_transform(self.df['ingredients'])
        print("Ingredient vectors prepared")


        # Tag Vectors
        print("Preparing tag vectors...")

        # convert ingredient list to text
        self.df['tags_text'] = self.df['tags'].apply(
            lambda x: ' '.join(ast.literal_eval(x) if pd.notna(x) else x)
        )

        # create TF-ID vector for ingredients
        self.tag_vectorizer = TfidfVectorizer(max_features=5000)
        self.tag_vector = self.ingredient_vectorizer.fit_transform(self.df['tags'])
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


    def find_similar(self, recipe_id, top_n=10):
        # find recipe index
        try:
            recipe_idx = self.df[self.df['id'] == recipe_id].index[0]
        except IndexError as e:
            return {
                "error": f"Recipe {recipe_id} not found",
                "recommendation": []
            }

        # get recipe info
        recipe = self.df.iloc[recipe_idx]
        recipe_time = recipe['minutes']

        # calculate ingredient similarity
        ingredient_sim = cosine_similarity(
            self.ingredient_vector[recipe_idx:recipe_idx+1],
            self.ingredient_vector
        )[0]

        # calculate tag similarity
        tag_sim = cosine_similarity(
            self.tag_vector[recipe_idx:recipe_idx+1],
            self.tag_vector
        )[0]

        # calculate time similarity
        time_sim = np.array([
            self._calculate_time_similarity(recipe_time, other_time)
            for other_time in self.df['minutes']
        ])

        # combine scores with weights
        final_scores = (
                self.INGREDIENT_WEIGHTS * ingredient_sim
                + self.TAG_WEIGHTS * tag_sim
                + self.TIME_WEIGHTS * time_sim
        )
        print(final_scores.shape)

        # get top N
        final_scores[recipe_idx] = -1
        top_indices = final_scores.argsort()[-top_n:][::-1]

        # build result
        recommendations = []
        for idx in top_indices:
            rec_recipe = self.df.iloc[idx]
            recommendations.append({
                'rec_recipe_id': int(rec_recipe['id']),
                'similarity_score': float(final_scores[idx]),
                'ingredient_similarity': float(ingredient_sim[idx]),
                'tag_similarity': float(tag_sim[idx]),
                'time_similarity': float(time_sim[idx]),
            })

        result = {
            'recipe_id': recipe_id,
            'recommendations': recommendations
        }

        return result



def main():
    recommender = ContentRecommender()
    df = pd.read_csv('data/RAW_recipes.csv')

    # Find a "Chicken Fried Rice" recipe
    test_recipes = df[df['name'].str.contains('fried rice', case=False, na=False)].head(3)

    print("Test recipes:")
    for idx, row in test_recipes.iterrows():
        print(f"  {row['id']}: {row['name']} ({row['minutes']} min)")

    print("\n" + "=" * 60)

    # Test recommendation for first fried rice recipe
    test_recipe_id = test_recipes.iloc[0]['id']
    test_recipe_name = test_recipes.iloc[0]['name']

    print(f"\nFinding similar recipes to: {test_recipe_name}")
    print(f"Recipe ID: {test_recipe_id}\n")

    results = recommender.find_similar(test_recipe_id, top_n=10)

    if 'error' in results:
        print(f"Error: {results['error']}")
    else:
        print(f"✅ Found {len(results['recommendations'])} recommendations:\n")

        for i, rec in enumerate(results['recommendations'], 1):
            rec_recipe = df[df['id'] == rec['rec_recipe_id']].iloc[0]
            print(f"{i}. {rec_recipe['name']}")
            print(f"   Overall Score: {rec['similarity_score']:.3f}")
            print(f"   - Ingredients: {rec['ingredient_similarity']:.3f} (65% weight)")
            print(f"   - Tags: {rec['tag_similarity']:.3f} (30% weight)")
            print(f"   - Time: {rec['time_similarity']:.3f} (5% weight)")
            print(f"   Cooking Time: {rec_recipe['minutes']} min")


if __name__ == '__main__':
    main()