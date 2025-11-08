import pytest
from fastapi.testclient import TestClient
import sys
import os

# Ajouter le chemin parent pour les imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app
from app.api.endpoints import initialize_engine

client = TestClient(app)

def test_root_endpoint():
    """Test du endpoint racine"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "RecomSys-Flix API"
    assert data["status"] == "healthy"

def test_health_endpoint():
    """Test du endpoint health"""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "recommendation_engine"

def test_recommendation_endpoint():
    """Test du endpoint de recommandation"""
    # Initialiser le moteur avant le test
    from app.api.endpoints import engine
    from app.api.endpoints import create_sample_data
    
    ratings_df = create_sample_data()
    engine.fit(ratings_df)
    
    request_data = {
        "user_id": 1,
        "n_recommendations": 5,
        "include_rated": False
    }
    
    response = client.post("/api/v1/recommend", json=request_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["user_id"] == 1
    assert "recommendations" in data
    assert "scores" in data
    assert "engine_type" in data
    assert data["engine_type"] == "hybrid"
    assert isinstance(data["recommendations"], list)

def test_recommendation_different_users():
    """Test avec différents utilisateurs"""
    # Initialiser le moteur avant le test
    from app.api.endpoints import engine
    from app.api.endpoints import create_sample_data
    
    ratings_df = create_sample_data()
    engine.fit(ratings_df)
    
    users = [1, 2, 3]
    
    for user_id in users:
        request_data = {
            "user_id": user_id,
            "n_recommendations": 3
        }
        
        response = client.post("/api/v1/recommend", json=request_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["user_id"] == user_id
        assert len(data["recommendations"]) <= 3

def test_recommendation_validation():
    """Test de validation des données"""
    # Test avec mauvais type de user_id
    invalid_request = {
        "user_id": "not_an_integer",
        "n_recommendations": 5
    }
    
    response = client.post("/api/v1/recommend", json=invalid_request)
    assert response.status_code == 422  # Validation error