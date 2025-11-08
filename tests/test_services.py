import pytest
import pandas as pd
from app.services.collaborative_filtering import CollaborativeFiltering
from app.services.neural_embeddings import NeuralRecommendation

def test_collaborative_filtering_fit(sample_ratings_data):
    """Test de l'entraînement du filtrage collaboratif"""
    cf = CollaborativeFiltering()
    cf.fit(sample_ratings_data)
    
    assert cf.user_similarity is not None
    assert cf.user_item_matrix is not None
    assert cf.svd_model is not None
    # Vérifier que la matrice de similarité a la bonne forme
    n_users = sample_ratings_data['user_id'].nunique()
    assert cf.user_similarity.shape == (n_users, n_users)

def test_collaborative_filtering_recommend(sample_ratings_data):
    """Test des recommandations collaboratives"""
    cf = CollaborativeFiltering()
    cf.fit(sample_ratings_data)
    
    recommendations = cf.recommend_for_user(user_id=1, n_recommendations=3)
    
    assert isinstance(recommendations, list)
    assert len(recommendations) <= 3
    
    # Vérifier que les recommandations sont des integers
    if recommendations:
        assert all(isinstance(movie, int) for movie in recommendations)
    
    # Vérifier que les films recommandés ne sont pas ceux déjà notés par l'utilisateur 1
    user_1_rated = sample_ratings_data[sample_ratings_data['user_id'] == 1]['movie_id'].tolist()
    for movie in recommendations:
        assert movie not in user_1_rated

def test_neural_recommendation_train(sample_ratings_data):
    """Test de l'entraînement du modèle neuronal"""
    neural_rec = NeuralRecommendation()
    neural_rec.train(sample_ratings_data, epochs=2)
    
    assert neural_rec.model is not None
    assert len(neural_rec.user_id_map) > 0
    assert len(neural_rec.movie_id_map) > 0
    assert len(neural_rec.reverse_movie_map) > 0

def test_neural_recommendation_recommend(sample_ratings_data):
    """Test des recommandations neuronales"""
    neural_rec = NeuralRecommendation()
    neural_rec.train(sample_ratings_data, epochs=2)
    
    recommendations = neural_rec.recommend(user_id=1, n_recommendations=3)
    
    assert isinstance(recommendations, list)
    assert len(recommendations) == 3
    # Vérification CRUCIALE : s'assurer que ce sont des integers
    assert all(isinstance(movie, int) for movie in recommendations), f"Recommandations: {recommendations}"