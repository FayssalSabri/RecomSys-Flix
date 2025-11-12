from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.api.endpoints import router as api_router
from app.api.database_endpoints import router as database_router
from config.database import engine, Base
import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print(" Starting RecomSys-Flix API...")
    
    # Créer les tables de la base de données (synchrone)
    try:
        Base.metadata.create_all(bind=engine)
        print(" Database tables created successfully")
    except Exception as e:
        print(f" Database error: {e}")
    
    yield  # L'application tourne ici
    
    # Shutdown
    print(" Shutting down RecomSys-Flix API...")

# Création de l'application FastAPI
app = FastAPI(
    title="RecomSys-Flix API",
    description="Intelligent Movie Recommendation System",
    version="2.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclure les routers
app.include_router(api_router, prefix="/api/v1")
app.include_router(database_router, prefix="/api/v1/database")

@app.get("/")
async def root():
    return {
        "message": "RecomSys-Flix API", 
        "version": "2.0.0",
        "status": "healthy",
        "database": "PostgreSQL integrated"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "recommendation_engine",
        "database": "postgresql",
        "cache": "redis"
    }

# Lancement de l'API
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
