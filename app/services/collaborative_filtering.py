import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD
import pickle
import os

class CollaborativeFiltering:
    def __init__(self):
        self.user_similarity = None
        self.item_similarity = None
        self.user_item_matrix = None
        self.svd_model = None
        
    def fit(self, ratings_df: pd.DataFrame):
        """Entraîne le modèle de filtrage collaboratif"""
        # Création matrice utilisateur-item
        self.user_item_matrix = ratings_df.pivot(
            index='user_id', 
            columns='movie_id', 
            values='rating'
        ).fillna(0)
        
        print(f" Matrice utilisateur-item: {self.user_item_matrix.shape}")
        
        # Similarité entre utilisateurs
        self.user_similarity = cosine_similarity(self.user_item_matrix)
        
        # SVD adaptatif - nombre de composants basé sur le nombre de films
        n_movies = self.user_item_matrix.shape[1]
        n_components = min(20, n_movies - 1)  # Maximum 20 composants ou n_movies-1
        
        if n_components < 2:
            n_components = 2  # Minimum 2 composants
            
        print(f" SVD avec {n_components} composants sur {n_movies} films")
        
        self.svd_model = TruncatedSVD(n_components=n_components, random_state=42)
        self.svd_matrix = self.svd_model.fit_transform(self.user_item_matrix)
        
        return self
    
    def recommend_for_user(self, user_id: int, n_recommendations: int = 10):
        """Génère des recommandations pour un utilisateur"""
        if user_id not in self.user_item_matrix.index:
            print(f"⚠️ Utilisateur {user_id} non trouvé")
            return []
            
        user_idx = list(self.user_item_matrix.index).index(user_id)
        user_ratings = self.user_item_matrix.iloc[user_idx]
        
        # Films déjà notés par l'utilisateur
        rated_movies = user_ratings[user_ratings > 0].index.tolist()
        
        # Trouver les utilisateurs similaires (exclure l'utilisateur lui-même)
        similar_users = np.argsort(self.user_similarity[user_idx])[::-1][1:6]  # Top 5
        
        # Calcul des scores de recommandation
        recommendations = {}
        for similar_user_idx in similar_users:
            similarity_score = self.user_similarity[user_idx][similar_user_idx]
            similar_user_id = self.user_item_matrix.index[similar_user_idx]
            similar_user_ratings = self.user_item_matrix.iloc[similar_user_idx]
            
            for movie_id in similar_user_ratings.index:
                # Ne recommander que les films non notés et avec rating > 3
                if (movie_id not in rated_movies and 
                    similar_user_ratings[movie_id] > 3 and 
                    movie_id not in recommendations):
                    
                    recommendations[movie_id] = similar_user_ratings[movie_id] * similarity_score
        
        # Trier et retourner les meilleures recommandations
        sorted_recs = sorted(recommendations.items(), 
                           key=lambda x: x[1], reverse=True)[:n_recommendations]
        
        result = [movie_id for movie_id, score in sorted_recs]
        print(f" Recommandations pour user {user_id}: {result}")
        return result