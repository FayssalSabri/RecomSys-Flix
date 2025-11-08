from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import router as api_router, initialize_engine

app = FastAPI(
    title="RecomSys-Flix",
    description="Hybrid Recommendation Engine",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Initialise l'application au démarrage"""
    initialize_engine()

@app.get("/")
async def root():
    return {"message": "RecomSys-Flix API", "status": "healthy"}

app.include_router(api_router, prefix="/api/v1")