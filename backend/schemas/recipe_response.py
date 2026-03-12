from pydantic import BaseModel

from schemas import Recipe


class RecipeResponse(BaseModel):
    recipe: Recipe
    predicted_time: dict