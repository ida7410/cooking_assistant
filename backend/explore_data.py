import re

import pandas as pd
from pathlib import Path

from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import numpy as np

# load data
data_path = Path(__file__).parent / "data" / "RAW_recipes.csv"
df = pd.read_csv(data_path)

def basic_info():
    # basic info
    print(f"Total recipes: {len(df)}")
    print(f"Columns: {list(df.columns)}")
    print(f"First few rows:")
    print(df.head())
    print("\n")

    # ingredients column
    print("Sample ingredients:")
    print(df['ingredients'].head(3))
    print("\n")

    # check missing val
    print(f"Missing values:")
    print(df.isna().sum())
    print("\n")

    # save sample for inspection
    df.head(100).to_csv("data/sample_recipes.csv", index=False)
    print(f"Saved 100 sample recipes to data/sample_recipes.csv")

def cooking_time():
    # cooking time desc
    print(f"Cooking time statistics:")
    print(df['minutes'].describe())
    print("\n")

    # steps desc
    print(f"Steps statistics:")
    print(df['n_steps'].describe())
    print("\n")

    # outliers
    print(f"Recipes > 1000 minutes: {len(df[df['minutes'] > 1000])}")
    print(f"Recipes > 500 minutes: {len(df[df['minutes'] > 500])}")
    print(f"Recipes > 100 minutes: {len(df[df['minutes'] > 100])}")
    print("\n")

    # reasonable (minutes <= 180)
    reasonable = df[df['minutes'] <= 180]
    print(f"Reasonable recipes: {len(reasonable)}")
    print(f"Percentage: {len(reasonable) / len(df) * 100:.1f}\n") # 92.5%

    # correlations w steps & cooking time
    print(f"Minutes vs N_steps: {df['minutes'].corr(df['n_steps']):.3f}")
    # corr w ingredients & cooking time
    print(f"Minutes vs N_ingredients: {df['minutes'].corr(df['n_ingredients']):.3f}")

    # exclude recipes > 180
    df_clean = df[df['minutes'] <= 180]
    X = df_clean[['n_steps', 'n_ingredients']]
    y = df_clean['minutes']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=10,
        random_state=42
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_absolute_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)

    print("Model Performance")
    print(f"MAE (Mean Absolute Error): {mae:.1f} minutes")
    print(f"RMSE (Root Mean Squared Error): {rmse:.1f} minutes")
    print(f"R² Score: {r2:.3f}")

    # feature importance
    importances = model.feature_importances_
    for feature, importance in zip(['n_steps', 'n_ingredients'], importances):
        print(f"{feature}: {importance:.3f}")


def test_corr_cooking_time():
    df_clean = df[df['minutes'] <= 180]

    # 1. check time related tags
    time_tags = df_clean['tags'].str.contains('minutes-or-less|hours-or-less', case=False, na=False)
    print(f"Recipe w/ time tags: {time_tags.sum()} ({time_tags.sum() / len(df_clean) * 100:.1f})")


    # 2. time in steps
    df_clean['extracted_time'] = df_clean['steps'].apply(extract_time)

    has_time = df_clean['extracted_time'] > 0
    print(f"Recipes with time in steps: {has_time.sum()} ({has_time.sum() / len(df_clean) * 100:.1f}%)")

    # correlation
    correlation = df_clean[has_time]['extracted_time'].corr(df_clean[has_time]['minutes'])
    print(f"Extracted time vs Actual time: {correlation:.3f}")


    # 3. cooking methods
    methods = {
        'bake/oven': ['bake', 'oven', 'roast'],
        'fry': ['fry', 'sauté'],
        'boil': ['boil'],
        'simmer': ['simmer'],
        'grill': ['grill', 'bbq'],
        'slow_cook': ['slow cooker', 'crockpot'],
    }
    for method_name, keywords in methods.items():
        pattern = '|'.join(keywords)
        has_method = df_clean['steps'].str.contains(pattern, case=False, na=False)
        count = has_method.sum()

        if count > 100:
            avg_time = df_clean[has_method]['minutes'].mean()
            print(f"{method_name:15} - {count:6} recipes - avg {avg_time:.0f} min")


def extract_time(text):
    pattern = r'(\d+(?:-\d+)?)\s*(minute|minutes|min|hour|hours|hr|sec|second|seconds)'
    matches = re.findall(pattern, str(text).lower())

    total = 0
    for match in matches:
        amount, unit = match

        if '-' in amount:
            amount = amount.split('-')[-1]
        num = int(amount)

        if 'hour' in unit or 'hr' in unit:
            num *= 60
        elif 'sec' in unit:
            num /= 60
        total += num

    return total


# cooking_time()
test_corr_cooking_time()