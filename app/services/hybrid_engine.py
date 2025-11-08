import pandas as pd
from typing import List
from .collaborative_filtering import CollaborativeFiltering
from .neural_embeddings import NeuralRecommendation

class HybridEngine:
    def __init__(self):
        self.cf_engine = CollaborativeFiltering()
        self.neural_engine = NeuralRecommendation()
        self.is_fitted = False
        
    def fit(self, ratings_df: pd.DataFrame):
        """Entraîne les deux moteurs"""
        print(" Début de l'entraînement du moteur hybride...")
        
        print("1. Entraînement du filtrage collaboratif...")
        self.cf_engine.fit(ratings_df)
        
        print("2. Entraînement du modèle neuronal...")
        self.neural_engine.train(ratings_df, epochs=5)
        
        self.is_fitted = True
        print(" Entraînement terminé!")
    
    def hybrid_recommend(self, user_id: int, n_recommendations: int = 10) -> List[int]:
        """Combine les recommandations des deux moteurs"""
        if not self.is_fitted:
            raise ValueError("Le moteur doit être entraîné avant de faire des recommandations")
        
        print(f"🔍 Génération de recommandations pour user {user_id}...")
        
        cf_recs = self.cf_engine.recommend_for_user(user_id, n_recommendations)
        print(f"   Collaborative: {cf_recs}")
        
        neural_recs = self.neural_engine.recommend(user_id, n_recommendations)
        print(f"   Neural: {neural_recs}")
        
        combined_recs = []
        
        for movie_id in cf_recs:
            if movie_id not in combined_recs:
                combined_recs.append(movie_id)
            if len(combined_recs) >= n_recommendations:
                break
        
        if len(combined_recs) < n_recommendations:
            for movie_id in neural_recs:
                if movie_id not in combined_recs:
                    combined_recs.append(movie_id)
                if len(combined_recs) >= n_recommendations:
                    break
        
        if len(combined_recs) < n_recommendations:
            pass
        
        print(f" Recommandations hybrides finales: {combined_recs}")
        return combined_recs[:n_recommendations]