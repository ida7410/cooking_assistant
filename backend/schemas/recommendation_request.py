from pydantic import BaseModel, Field
from typing import Optional


class RecommendationRequest(BaseModel):
    recipe_id: int
    top_n: int
    strategy: Optional[str] = Field(
        default='hybrid',
        description="Recommendation strategy",
        pattern="^(content|collaborative|hybrid)$"
    )