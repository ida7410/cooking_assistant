import ast
from typing import List

from pydantic import BaseModel


class Recipe(BaseModel):
    id: int
    name: str
    description: str
    tags: List[str]
    ingredients: List[str]
    n_ingredients: int
    steps: List[str]
    n_steps: int
    cooking_time: int


    @classmethod
    def get_recipe_dataframe_from_row(cls, row):
        try:
            tags = ast.literal_eval(row['tags'])
        except:
            tags = []

        try:
            ingredients = ast.literal_eval(row['ingredients'])
        except:
            ingredients = []

        try:
            steps = ast.literal_eval(row['steps'])
        except:
            steps = []

        recipe = cls(
            id=int(row['id']),  # use 'id' from dataset
            name=row['name'],
            description=str(row.get('description', '')),
            tags=tags,
            ingredients=ingredients,
            n_ingredients=len(ingredients),
            steps=steps,
            n_steps=len(steps),
            cooking_time=int(row['minutes'])
        )
        return recipe