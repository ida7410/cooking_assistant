from typing import List, Optional

from pydantic import BaseModel, Field


class RecipeSearchRequest(BaseModel):
    ingredients: List[str] = Field(
        ...,
        min_length=1,
        description="List of ingredients to search for",
        examples=["chicken", "rice", "soy sauce"]
    )
    skill_level: Optional[str] = Field(
        default='intermediate',
        description="User's cooking skill level",
        pattern="^(beginner|intermediate|expert)$"
    )
    simplify_steps: Optional[bool] = Field(
        default=False,
        description="Whether to simplify recipe steps"
    )
    top_n: Optional[int] = Field(
        default=10,
        ge=1,
        le=50,
        description="Number of results to return"
    )
