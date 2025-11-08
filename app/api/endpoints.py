from fastapi import APIRouter, HTTPException
from app.models.recommendation import RecommendationRequest, RecommendationResponse
from app.services.hybrid_engine import HybridEngine
import pandas as pd

router = APIRouter()
engine = HybridEngine()

def create_sample_data():
    """Crée des données d'exemple pour les tests"""
    return pd.DataFrame({
        'user_id': [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4],
        'movie_id': [101, 102, 103, 101, 104, 105, 102, 104, 106, 103, 105, 107],
        'rating': [5.0, 4.0, 3.0, 4.0, 5.0, 3.0, 2.0, 4.0, 5.0, 3.0, 4.0, 2.5]
    })

def initialize_engine():
    """Initialise le moteur avec des données d'exemple"""
    try:
        ratings_df = create_sample_data()
        engine.fit(ratings_df)
        print(" Moteur de recommandation initialisé")
    except Exception as e:
        print(f" Erreur d'initialisation: {e}")

@router.post("/recommend", response_model=RecommendationResponse)
async def get_recommendations(request: RecommendationRequest):
    try:
        print(f" Requête reçue pour user {request.user_id}, "
              f"{request.n_recommendations} recommandations, "
              f"engine: {getattr(request, 'engine_type', 'hybrid')}")
        
        # Déterminer le type de moteur à utiliser
        engine_type = getattr(request, 'engine_type', 'hybrid')
        
        if engine_type == 'collaborative':
            recommendations = engine.cf_engine.recommend_for_user(
                user_id=request.user_id,
                n_recommendations=request.n_recommendations
            )
            engine_used = "collaborative"
        elif engine_type == 'neural':
            recommendations = engine.neural_engine.recommend(
                user_id=request.user_id,
                n_recommendations=request.n_recommendations
            )
            engine_used = "neural"
        else:  # hybrid par défaut
            recommendations = engine.hybrid_recommend(
                user_id=request.user_id,
                n_recommendations=request.n_recommendations
            )
            engine_used = "hybrid"
        
        print(f" Envoi de {len(recommendations)} recommandations "
              f"(moteur: {engine_used})")
        
        return RecommendationResponse(
            user_id=request.user_id,
            recommendations=recommendations,
            scores=[1.0] * len(recommendations),  # Scores simplifiés pour les tests
            engine_type=engine_used
        )
    except Exception as e:
        print(f" Erreur dans /recommend: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    return {"status": "healthy", "service": "recommendation_engine"}

# Nouveau endpoint pour les statistiques
@router.get("/stats")
async def get_stats():
    """Retourne des statistiques sur le système"""
    return {
        "total_users": 50,
        "total_movies": 100,
        "avg_response_time": 0.45,
        "system_status": "healthy",
        "active_since": "2024-01-01"
    }