from typing import Optional

from pydantic import BaseModel

from schemas.recipe import Recipe


class RecipeRecommendation(BaseModel):
    recipe: Recipe
    similarity_score: float

    # recipe matcher
    missing_ingredients: Optional[list] = None

    # content recommendation
    ingredient_similarity: Optional[float] = None
    tag_similarity: Optional[float] = None
    time_similarity: Optional[float] = None

    # collab recommendation
    common_users: Optional[float] = None
    jaccard: Optional[float] = None
    support: Optional[float] = None
    confidence: Optional[float] = None

    # hybrid recommendation
    content_score: Optional[float] = None
    collab_score: Optional[float] = None
    in_both: Optional[bool] = None