import pandas as pd
import os
from typing import Tuple

def load_sample_data() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Charge les données d'exemple"""
    try:
        # Chemin relatif depuis la racine du projet
        ratings_path = 'test_data/sample_ratings.csv'
        movies_path = 'test_data/sample_movies.csv'
        
        ratings_df = pd.read_csv(ratings_path)
        movies_df = pd.read_csv(movies_path)
        
        print(f"📊 Données chargées: {len(ratings_df)} ratings, "
              f"{ratings_df['user_id'].nunique()} utilisateurs, "
              f"{ratings_df['movie_id'].nunique()} films")
        
        return ratings_df, movies_df
        
    except FileNotFoundError as e:
        print(f"❌ Fichier non trouvé: {e}")
        print("💡 Exécutez 'python create_sample_data.py' pour créer les données d'exemple")
        raise

def load_ratings_only() -> pd.DataFrame:
    """Charge uniquement les ratings"""
    ratings_df, _ = load_sample_data()
    return ratings_df[['user_id', 'movie_id', 'rating']]