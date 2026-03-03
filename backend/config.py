import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

# base directory
BASE_DIR = Path(__file__).resolve().parent

# environment
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
IS_PRODUCTION = ENVIRONMENT == "production"

# API settings
API_TITLE = "Cooking Assistant API"
API_VERSION = "0.1.0"
API_DESCRIPTION = "ML-powered recipe recommendation system"

# CORS origins
if IS_PRODUCTION:
    CORS_ORIGINS = [
        "https://*.vercel.app",
        "https://cooking-assistant.vercel.app",  # Your actual domain
    ]
else:
    CORS_ORIGINS = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

# Claude API
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# File Paths
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"
RECIPE_DATA_PATH = DATA_DIR / "RAW_recipes.csv"

# ML Model Settings
TFIDF_MAX_FEATURES = 5000
RECIPE_MATCH_TOP_N = 5
MIN_MATCH_THRESHOLD = 0.1

# Time Predictor Settings
TIME_PREDICTOR_MODEL_PATH = MODELS_DIR / "time_predictor.pkl"

# Recipe Simplifier Settings
MAX_SIMPLIFICATION_TOKENS = 1000

# Logging
LOG_LEVEL = "INFO" if IS_PRODUCTION else "DEBUG"

# Rate Limiting (for production)
RATE_LIMIT_PER_MINUTE = 60 if IS_PRODUCTION else 1000