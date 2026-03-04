import pandas as pd
from pathlib import Path

# load data
data_path = Path(__file__).parent / "data" / "RAW_recipes.csv"
df = pd.read_csv(data_path)

# basic info
print(f"Total recipes: {len(df)}\n")
print(f"Columns: {list(df.columns)}\n")
print(f"First few rows:")
print(df.head())
print("\n\n")

# ingredients column
print("Sample ingredients:")
print(df['ingredients'].head(3))
print("\n\n")

# check missing val
print(f"Missing values:")
print(df.isna().sum())
print("\n\n")

# save sample for inspection
df.head(100).to_csv("data/sample_recipes.csv", index=False)
print(f"Saved 100 sample recipes to data/sample_recipes.csv")