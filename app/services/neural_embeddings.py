import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import pandas as pd
from typing import List, Tuple

class NeuralEmbeddingModel(nn.Module):
    def __init__(self, n_users: int, n_movies: int, embedding_dim: int = 20):  # Réduit la dimension
        super(NeuralEmbeddingModel, self).__init__()
        self.user_embedding = nn.Embedding(n_users, embedding_dim)
        self.movie_embedding = nn.Embedding(n_movies, embedding_dim)
        self.fc_layers = nn.Sequential(
            nn.Linear(embedding_dim * 2, 64),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(32, 1)
        )
        
    def forward(self, user_ids, movie_ids):
        user_embed = self.user_embedding(user_ids)
        movie_embed = self.movie_embedding(movie_ids)
        x = torch.cat([user_embed, movie_embed], dim=1)
        return self.fc_layers(x).squeeze()

class NeuralRecommendation:
    def __init__(self):
        self.model = None
        self.user_id_map = {}
        self.movie_id_map = {}
        self.reverse_movie_map = {}  # Map inverse pour retrouver les vrais IDs
        
    def train(self, ratings_df: pd.DataFrame, epochs: int = 5):  # Réduit les epochs
        """Entraîne le modèle neuronal"""
        # Préparation des données
        unique_users = sorted(ratings_df['user_id'].unique())
        unique_movies = sorted(ratings_df['movie_id'].unique())
        
        self.user_id_map = {uid: idx for idx, uid in enumerate(unique_users)}
        self.movie_id_map = {mid: idx for idx, mid in enumerate(unique_movies)}
        self.reverse_movie_map = {idx: mid for mid, idx in self.movie_id_map.items()}
        
        n_users = len(unique_users)
        n_movies = len(unique_movies)
        
        print(f" Entraînement neural: {n_users} users, {n_movies} movies")
        
        # Initialisation du modèle
        self.model = NeuralEmbeddingModel(n_users, n_movies, embedding_dim=20)
        criterion = nn.MSELoss()
        optimizer = optim.Adam(self.model.parameters(), lr=0.001)
        
        # Conversion des données
        user_indices = [self.user_id_map[uid] for uid in ratings_df['user_id']]
        movie_indices = [self.movie_id_map[mid] for mid in ratings_df['movie_id']]
        
        users_tensor = torch.tensor(user_indices, dtype=torch.long)
        movies_tensor = torch.tensor(movie_indices, dtype=torch.long)
        ratings_tensor = torch.tensor(ratings_df['rating'].values, dtype=torch.float32)
        
        # Entraînement
        self.model.train()
        for epoch in range(epochs):
            optimizer.zero_grad()
            predictions = self.model(users_tensor, movies_tensor)
            loss = criterion(predictions, ratings_tensor)
            loss.backward()
            optimizer.step()
            
            if epoch % 2 == 0:
                print(f"Epoch {epoch}, Loss: {loss.item():.4f}")
    
    def recommend(self, user_id: int, n_recommendations: int = 10) -> List[int]:
        """Génère des recommandations avec le modèle neuronal"""
        if user_id not in self.user_id_map:
            print(f"⚠️ Utilisateur {user_id} non trouvé dans le modèle neural")
            return []
            
        user_idx = self.user_id_map[user_id]
        
        # Films déjà notés par l'utilisateur (à exclure)
        # Pour l'instant, on recommande tous les films non notés
        
        # Prédire les ratings pour tous les films
        user_tensor = torch.tensor([user_idx] * len(self.movie_id_map), dtype=torch.long)
        movie_tensors = torch.tensor(list(self.movie_id_map.values()), dtype=torch.long)
        
        self.model.eval()
        with torch.no_grad():
            predictions = self.model(user_tensor, movie_tensors)
        
        # Convertir les indices internes en vrais IDs de films
        top_indices = torch.argsort(predictions, descending=True)[:n_recommendations]
        recommended_movies = [
            int(self.reverse_movie_map[idx.item()])  # Conversion explicite en int
            for idx in top_indices
        ]
        
        print(f" Recommandations neurales pour user {user_id}: {recommended_movies}")
        return recommended_movies