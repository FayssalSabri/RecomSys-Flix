import time
import requests
from app.services.hybrid_engine import HybridEngine
import pandas as pd

def create_performance_data():
    """Crée des données plus importantes pour les tests de performance"""
    data = []
    for user_id in range(1, 51):  # 50 utilisateurs
        for movie_id in range(1, 21):  # 20 films par utilisateur
            rating = (user_id + movie_id) % 5 + 1  # Rating entre 1 et 5
            data.append({
                'user_id': user_id,
                'movie_id': movie_id + 100,  # IDs à partir de 100
                'rating': float(rating)
            })
    return pd.DataFrame(data)

def test_engine_performance():
    """Test de performance du moteur avec plus de données"""
    print(" Test de performance avec données étendues...")
    
    # Créer des données plus importantes
    performance_data = create_performance_data()
    print(f" Données: {len(performance_data)} ratings, "
          f"{performance_data['user_id'].nunique()} users, "
          f"{performance_data['movie_id'].nunique()} movies")
    
    engine = HybridEngine()
    
    # Test d'entraînement
    start_time = time.time()
    engine.fit(performance_data)
    training_time = time.time() - start_time
    
    print(f" Temps d'entraînement: {training_time:.2f}s")
    
    # Test de recommandation en batch
    users_to_test = [1, 5, 10, 15, 20]
    total_time = 0
    successful_recommendations = 0
    
    for user_id in users_to_test:
        start_time = time.time()
        recommendations = engine.hybrid_recommend(user_id=user_id, n_recommendations=10)
        response_time = time.time() - start_time
        total_time += response_time
        
        if recommendations:
            successful_recommendations += 1
        
        print(f"👤 User {user_id}: {len(recommendations)} recs, temps: {response_time:.3f}s")
    
    avg_response_time = total_time / len(users_to_test)
    success_rate = successful_recommendations / len(users_to_test) * 100
    
    print(f" Temps de réponse moyen: {avg_response_time:.3f}s")
    print(f" Taux de succès: {success_rate:.1f}%")
    
    # Vérifications de performance
    assert training_time < 30, f"Entraînement trop long: {training_time:.2f}s"
    assert avg_response_time < 1.0, f"Temps de réponse trop long: {avg_response_time:.3f}s"
    assert success_rate > 80, f"Taux de succès trop bas: {success_rate:.1f}%"
    
    return True

def test_api_performance():
    """Test de performance de l'API"""
    print("\ Test de performance API...")
    
    # L'API doit être démarrée pour ce test
    try:
        # Test de requête unique
        url = "http://localhost:8000/api/v1/recommend"
        data = {
            "user_id": 1,
            "n_recommendations": 10,
            "include_rated": False
        }
        
        start_time = time.time()
        response = requests.post(url, json=data, timeout=10)
        end_time = time.time()
        
        if response.status_code == 200:
            single_request_time = end_time - start_time
            print(f" Requête unique: {single_request_time:.3f}s")
            print(f" Réponse: {response.json()}")
            return single_request_time < 2.0
        else:
            print(f" API erreur: {response.status_code} - {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("⚠️ API non démarrée, test de performance API ignoré")
        return False
    except requests.exceptions.Timeout:
        print("⚠️ Timeout API, test de performance API ignoré")
        return False
    except Exception as e:
        print(f"⚠️ Erreur API: {e}")
        return False

if __name__ == "__main__":
    print(" Lancement des tests de performance RecomSys-Flix...")
    
    # Test du moteur
    engine_success = test_engine_performance()
    
    # Test de l'API
    api_success = test_api_performance()
    
    if engine_success and api_success:
        print("\n TOUS LES TESTS DE PERFORMANCE ONT RÉUSSI !")
    else:
        print("\n Certains tests de performance ont échoué")