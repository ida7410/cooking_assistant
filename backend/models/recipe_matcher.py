import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class RecipeMatcher:
    def __init__(self, data_path='data/RAW_recipes.csv'):
        # load recipes
        self.df = pd.read_csv(data_path)

        # create ingredient vectors
        self.vectorizer = TfidfVectorizer()
        self.recipe_vectors = self.vectorizer.fit_transform(
            self.df['ingredients'].astype(str)
        )

    def find_matches(self, user_ingredients, top_n=5):
        # convert user ingredients to vector
        user_text = ' '.join(user_ingredients)
        user_vector = self.vectorizer.transform([user_text])

        # calculate similarity
        similarities = cosine_similarity(user_vector, self.recipe_vectors)[0]

        # get top matches
        top_indices = similarities.argsort()[-top_n:][::-1]

        results = []
        for i in top_indices:
            recipe = {
                'id': int(self.df.iloc[i]['id']),  # use 'id' from dataset
                'name': self.df.iloc[i]['name'],
                'match_percentage': int(similarities[i] * 100),
                'ingredients': eval(self.df.iloc[i]['ingredients']),  # convert string to list
                'cooking_time': int(self.df.iloc[i]['minutes']),  # 'minutes'
                'difficulty': self._estimate_difficulty(self.df.iloc[i]),  # ← Add difficulty
                'missing_ingredients': []  # ← Add this (calculate later if needed)
            }
            results.append(recipe)

        return results

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
