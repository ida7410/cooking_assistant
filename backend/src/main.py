from fastapi import FastAPI

app = FastAPI(title="Cooking Assistant API", version="0.1.0")

@app.get("/")
async def root():
    return {"message": "Cooking Assistant API", "status": "running"}