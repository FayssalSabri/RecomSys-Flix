import pytest
import time
from app.services.hybrid_engine import HybridEngine
import pandas as pd

def test_hybrid_engine_integration():
    """Test d'intégration complet du moteur hybride"""
    # Données de test
    sample_data = pd.DataFrame({
        'user_id': [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5],
        'movie_id': [101, 102, 103, 101, 104, 105, 102, 104, 106, 103, 105, 107, 101, 106, 108],
        'rating': [5.0, 4.5, 3.0, 4.0, 5.0, 3.5, 2.0, 4.5, 5.0, 3.0, 4.0, 2.5, 5.0, 4.0, 3.5]
    })
    
    engine = HybridEngine()
    
    # Test d'entraînement
    start_time = time.time()
    engine.fit(sample_data)
    training_time = time.time() - start_time
    
    print(f"⏱️ Temps d'entraînement: {training_time:.2f}s")
    assert training_time < 10  # Doit être rapide
    
    # Test de recommandation pour différents utilisateurs
    test_users = [1, 2, 3]
    
    for user_id in test_users:
        start_time = time.time()
        recommendations = engine.hybrid_recommend(user_id=user_id, n_recommendations=5)
        response_time = time.time() - start_time
        
        print(f"👤 User {user_id}: {recommendations} (temps: {response_time:.3f}s)")
        
        assert isinstance(recommendations, list)
        assert len(recommendations) <= 5
        assert all(isinstance(movie_id, int) for movie_id in recommendations)
        assert response_time < 2.0  # Doit être rapide

def test_engine_with_unknown_user():
    """Test avec un utilisateur inconnu"""
    sample_data = pd.DataFrame({
        'user_id': [1, 1, 2, 2],
        'movie_id': [101, 102, 101, 103],
        'rating': [5.0, 4.0, 3.0, 4.5]
    })
    
    engine = HybridEngine()
    engine.fit(sample_data)
    
    # Utilisateur qui n'existe pas dans les données d'entraînement
    recommendations = engine.hybrid_recommend(user_id=999, n_recommendations=3)
    
    # Doit retourner une liste (potentiellement vide) sans erreur
    assert isinstance(recommendations, list)