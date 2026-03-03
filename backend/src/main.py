from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Cooking Assistant API",
    description="ML-powered recipe recommendation system",
    version="0.1.0"
)

# CORS middleware - allows frontend to call API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Local development
        "https://*.vercel.app",   # Vercel deployment
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "Cooking Assistant API",
        "version": "0.1.0",
        "status": "running"
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