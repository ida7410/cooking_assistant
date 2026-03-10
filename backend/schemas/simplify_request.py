from pydantic import BaseModel, Field
from typing import Optional


class SimplifyRequest(BaseModel):
    skill_level: Optional[str] = Field(
        default='beginner',
        description="Target skill level for simplification",
        pattern="^(beginner|intermediate|expert)$"
    )