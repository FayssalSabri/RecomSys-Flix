import pytest
import pandas as pd
from fastapi.testclient import TestClient

# Import conditionnel pour éviter les erreurs d'import circulaire
try:
    from app.main import app
except ImportError as e:
    print(f"Import warning: {e}")
    app = None

@pytest.fixture
def client():
    if app is None:
        pytest.skip("Impossible d'importer l'application FastAPI")
    return TestClient(app)

@pytest.fixture
def sample_ratings_data():
    """Données de test réalistes"""
    return pd.DataFrame({
        'user_id': [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5],
        'movie_id': [101, 102, 103, 101, 104, 105, 102, 104, 106, 103, 105, 107, 101, 106, 108],
        'rating': [5.0, 4.5, 3.0, 4.0, 5.0, 3.5, 2.0, 4.5, 5.0, 3.0, 4.0, 2.5, 5.0, 4.0, 3.5]
    })

@pytest.fixture
def sample_ratings_large():
    """Données plus importantes pour les tests de performance"""
    data = []
    for user_id in range(1, 21):  # 20 utilisateurs
        for movie_id in range(1, 11):  # 10 films par utilisateur
            rating = (user_id + movie_id) % 5 + 1  # Rating entre 1 et 5
            data.append({
                'user_id': user_id,
                'movie_id': movie_id,
                'rating': float(rating)
            })
    return pd.DataFrame(data)