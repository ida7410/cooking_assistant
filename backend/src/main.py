import shutil
from datetime import datetime

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

import config
from src.dependencies import model_state
from src.logger import setup_logging, get_logger
from src.routers import recipe

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

app.include_router(recipe.router)

setup_logging()
logger = get_logger(__name__)

@app.on_event("startup")
async def startup():
    logger.debug("Startup...")
    # load model
    model_state.initialize()

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "name": "Cooking Assistant API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "recipe_detail": "GET /api/recipe/{id}",
            "search": "POST /api/recipe/search",
            "simplify": "POST /api/recipe/simplify",
            "recommendations": "POST /api/recipe/recommend"
        }
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "models_loaded": model_state.is_ready(),
        "timestamp": datetime.now().isoformat(),
        "components": {
            "recipe_matcher": "ready" if model_state.recipe_matcher else "not loaded",
            "time_predictor": "ready" if model_state.time_predictor else "not loaded",
            "recipe_simplifier": "ready" if model_state.recipe_simplifier else "not loaded",
            "recommender_manager": "ready" if model_state.recommender_manager else "not loaded",
        }
    }


@app.post("/upload-file")
async def upload_file(file: UploadFile = File(...)):
    """Temporary endpoint to upload CSV files to Railway volume"""
    file_path = f"/data/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "filename": file.filename,
        "location": file_path,
        "message": "File uploaded successfully"
    }