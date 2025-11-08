"""
Script pour tester les composants un par un
"""

def test_components():
    print(" Test des composants RecomSys-Flix...")
    
    # 1. Test des modèles
    print("1. Test des modèles Pydantic...")
    try:
        from app.models.recommendation import UserRating, RecommendationRequest
        rating = UserRating(user_id=1, movie_id=101, rating=4.5)
        request = RecommendationRequest(user_id=1, n_recommendations=5)
        print("   ✅ Modèles OK")
    except Exception as e:
        print(f"   ❌ Erreur modèles: {e}")
        return False
    
    # 2. Test des services
    print("2. Test des services...")
    try:
        from app.services.collaborative_filtering import CollaborativeFiltering
        from app.services.neural_embeddings import NeuralRecommendation
        print("   ✅ Services OK")
    except Exception as e:
        print(f"   ❌ Erreur services: {e}")
        return False
    
    # 3. Test des données
    print("3. Test des données...")
    try:
        import pandas as pd
        df = pd.DataFrame({
            'user_id': [1, 2, 3],
            'movie_id': [101, 102, 103],
            'rating': [5.0, 4.0, 3.0]
        })
        print("   ✅ Pandas OK")
    except Exception as e:
        print(f"   ❌ Erreur données: {e}")
        return False
    
    # 4. Test de l'API (sans lancer le serveur)
    print("4. Test de l'API...")
    try:
        from app.api.endpoints import router
        print("   ✅ API Router OK")
    except Exception as e:
        print(f"   ❌ Erreur API: {e}")
        return False
    
    print(" Tous les composants sont fonctionnels!")
    return True

if __name__ == "__main__":
    test_components()