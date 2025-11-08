from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class EngineType(str, Enum):
    HYBRID = "hybrid"
    COLLABORATIVE = "collaborative"
    NEURAL = "neural"

class UserRating(BaseModel):
    user_id: int
    movie_id: int
    rating: float
    timestamp: Optional[int] = None

class RecommendationRequest(BaseModel):
    user_id: int
    n_recommendations: int = 10
    include_rated: bool = False
    engine_type: EngineType = EngineType.HYBRID  # Nouveau champ

class RecommendationResponse(BaseModel):
    user_id: int
    recommendations: List[int]  # movie IDs
    scores: List[float]
    engine_type: str  # "collaborative", "neural", "hybrid"

class SystemStats(BaseModel):
    total_users: int
    total_movies: int
    avg_response_time: float
    system_status: str
    active_since: str