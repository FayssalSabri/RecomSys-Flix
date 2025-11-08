"""Tests basiques pour vérifier que l'environnement fonctionne"""

def test_environment():
    """Test que l'environnement de test fonctionne"""
    assert 1 + 1 == 2

def test_imports():
    """Test que les imports principaux fonctionnent"""
    try:
        import pandas as pd
        from app.models.recommendation import RecommendationRequest
        assert True
    except ImportError as e:
        assert False, f"Import failed: {e}"

def test_dataframe_creation():
    """Test la création de DataFrames pandas"""
    import pandas as pd
    df = pd.DataFrame({
        'user_id': [1, 2, 3],
        'movie_id': [101, 102, 103],
        'rating': [5.0, 4.0, 3.0]
    })
    assert len(df) == 3
    assert list(df.columns) == ['user_id', 'movie_id', 'rating']