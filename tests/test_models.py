import pytest
from app.models.recommendation import UserRating, RecommendationRequest, RecommendationResponse

def test_user_rating_model():
    """Test du modèle UserRating"""
    rating = UserRating(
        user_id=1,
        movie_id=101,
        rating=4.5
    )
    
    assert rating.user_id == 1
    assert rating.movie_id == 101
    assert rating.rating == 4.5

def test_recommendation_request():
    """Test du modèle RecommendationRequest"""
    request = RecommendationRequest(
        user_id=1,
        n_recommendations=5
    )
    
    assert request.user_id == 1
    assert request.n_recommendations == 5
    assert request.include_rated == False  # valeur par défaut

def test_recommendation_response():
    """Test du modèle RecommendationResponse"""
    response = RecommendationResponse(
        user_id=1,
        recommendations=[101, 102, 103],
        scores=[0.9, 0.8, 0.7],
        engine_type="hybrid"
    )
    
    assert len(response.recommendations) == 3
    assert response.engine_type == "hybrid"