from typing import List, Optional

from pydantic import BaseModel

from schemas.recipe import Recipe
from schemas.recipe_recommendation import RecipeRecommendation


class RecommendationResponse(BaseModel):
    target: Recipe | List[str]
    status: str
    top_n: int
    strategy: str
    recommendations: List[RecipeRecommendation]
    error_message: Optional[str] = None