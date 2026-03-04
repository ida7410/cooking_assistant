import pickle

import pandas as pd
import re
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from pathlib import Path


class CookingTimePredictor:
    def __init__(self, data_path='data/RAW_recipes.csv', model_path='models/saved/time_predictor.pkl'):
        self.data_path = data_path
        self.model_path = Path(model_path)
        self.model = None
        self.feature_cols = [
            'n_steps',
            'n_ingredients',
            'extracted_time',
            'has_bake',
            'has_fry',
            'has_boil',
            'has_simmer',
            'has_grill',
            'has_slow_cook'
        ]
        self.methods = {
            'bake': ['bake', 'oven', 'roast'],
            'fry': ['fry', 'sauté'],
            'boil': ['boil'],
            'simmer': ['simmer'],
            'grill': ['grill', 'bbq'],
            'slow_cook': ['slow cooker', 'crockpot'],
        }

        if self.model_path.exists():
            self._load_model()
        else:
            self._train_model()


    def _load_model(self):
        with open(self.model_path, 'rb') as f:
            self.model = pickle.load(f)
        print("Loaded model")
        print(f"{self.model}")


    def _train_model(self):
        # exclude outlier datas
        df = pd.read_csv(self.data_path)
        df_clean = df[df['minutes'] <= 180]

        # extract times in steps
        df_clean['extracted_time'] = df_clean['steps'].apply(self._extract_time)

        # tags for cooking methods
        for method, keywords in self.methods.items():
            pattern = '|'.join(keywords)
            df_clean[f'has_{method}'] = df_clean['steps'].str.contains(
                pattern, case=False, na=False
            ).astype(int)


        # set X & y
        X = df_clean[self.feature_cols]
        y = df_clean['minutes']

        # divide train & test
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # train model
        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=15,
            random_state=42,
        )
        self.model.fit(X_train, y_train)

        # predict
        y_pred = self.model.predict(X_test)

        # metrics
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        # print result
        print(f"MAE: {mae:.1f} minutes")
        print(f"R2 : {r2:.3f}")

        self.model_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.model_path, 'wb') as f:
            pickle.dump(self.model, f)
        print(f"Model saved to {self.model_path}")

    # extract times
    def _extract_time(self, text):
        if pd.isna(text):
            return 0
        pattern = r'(\d+(?:-\d+)?)\s*(minute|minutes|min|hour|hours|hr)'
        matches = re.findall(pattern, str(text).lower())
        total = 0
        for match in matches:
            amount_str, unit = match
            if '-' in amount_str:
                amount_str = amount_str.split('-')[-1]
            try:
                num = int(amount_str)
            except ValueError:
                continue
            if 'hour' in unit or 'hr' in unit:
                num *= 60
            total += num
        return total


    # extract features
    def _extract_features(self, recipe_row):
        steps_text = str(recipe_row.get('steps', '')).lower()
        features = {
            'n_steps': recipe_row.get('n_steps', 0),
            'n_ingredients': recipe_row.get('n_ingredients', 0),
            'extracted_time': self._extract_time(steps_text),
        }

        for method, keywords in self.methods.items():
            features[f'has_{method}'] = int(any(kw in steps_text for kw in keywords))
        return features


    # predict
    def predict(self, recipe_row, skill_level='intermediate'):
        # extract feature
        features = self._extract_features(recipe_row)

        # set X
        X = pd.DataFrame([features])[self.feature_cols]

        # predict
        base_time = self.model.predict(X)[0]

        # adjust
        n_steps = recipe_row.get('n_steps', 0)
        complexity = min(n_steps / 10, 1.5)

        multipliers = {
            'beginner': 1.3 + (complexity * 0.2),
            'intermediate': 1.0,
            'expert': 0.7 + (complexity * 0.1)
        }
        multiplier = multipliers.get(skill_level, 1.0)
        adjusted_time = base_time * multiplier

        return {
            'base_time': int(base_time),
            'adjusted_time': int(adjusted_time),
            'skill_level': skill_level,
            'extracted_time': features['extracted_time'],  # For debugging
        }



def main():
    predictor = CookingTimePredictor()

    df = pd.read_csv('data/RAW_recipes.csv')
    sample_recipes = df.sample(5)
    for idx, recipe in sample_recipes.iterrows():
        print(f"Recipe: {recipe['name']}")
        print(f"  Actual time: {recipe['minutes']} min")
        print(f"  Steps: {recipe['n_steps']}, Ingredients: {recipe['n_ingredients']}")

        # Predict for different skill levels
        for skill in ['beginner', 'intermediate', 'expert']:
            prediction = predictor.predict(recipe, skill_level=skill)
            print(f"  {skill:12}: {prediction['adjusted_time']:3} min")

        print()


if __name__ == '__main__':
    main()