from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import config

app = FastAPI(
    title=config.API_TITLE,
    description=config.API_DESCRIPTION,
    version=config.API_VERSION
)

# CORS middleware with config
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": config.API_TITLE,
        "version": config.API_VERSION,
        "status": "running",
        "environment": config.ENVIRONMENT
    }


@app.post("/recipe/search")
async def recipe_search(ingredients: List[str]):
    template = {
        "recipes": [
            {
                "id": 1,
                "name": "Chicken Fried Rice",
                "match_percentage": 85,
                "cooking_time": 25,
                "difficulty": "Easy",
                "missing_ingredients": ["egg", "green onion"]
            },
            {
                "id": 2,
                "name": "Garlic Soy Chicken",
                "match_percentage": 75,
                "cooking_time": 30,
                "difficulty": "Easy",
                "missing_ingredients": ["ginger"]
            }
        ],
        "total_found": 2
    }
    return template