from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import config
from models.recipe_matcher import RecipeMatcher

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

# load model on startup
matcher = None
@app.on_event("startup")
async def startup():
    global matcher
    matcher = RecipeMatcher()
    print("Recipe matcher loaded\n")

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
    if not matcher:
        return {"error": "Model not loaded"}
    results = matcher.find_matches(ingredients)
    return {"recipes": results, "total_found": len(results)}