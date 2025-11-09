```markdown
#  Recommendation Algorithms Documentation

## Overview

RecomSys-Flix implements a sophisticated hybrid recommendation system combining multiple machine learning approaches for optimal movie recommendations.

##  Collaborative Filtering

### Algorithm Description
Collaborative filtering predicts user preferences by analyzing patterns from many users.

### Mathematical Foundation

#### User-Item Matrix
```
Users vs Movies Matrix:
        Movie1  Movie2  Movie3  ...  MovieN
User1    5.0     4.5     -          3.0
User2    -       4.0     2.5        -
User3    3.0     -       5.0        4.5
...
```

#### Similarity Calculation
**Cosine Similarity:**
```
similarity(u,v) = (u · v) / (||u|| * ||v||)
```

**Pearson Correlation:**
```
correlation(u,v) = Σ[(u_i - ū)(v_i - v̄)] / √[Σ(u_i - ū)² Σ(v_i - v̄)²]
```

### Implementation Details

```python
class CollaborativeFiltering:
    def fit(self, ratings_df):
        # Create user-item matrix
        self.user_item_matrix = ratings_df.pivot_table(
            index='user_id', 
            columns='movie_id', 
            values='rating'
        ).fillna(0)
        
        # Compute user similarities
        self.user_similarity = cosine_similarity(self.user_item_matrix)
        
        # Dimensionality reduction
        self.svd = TruncatedSVD(n_components=min(50, n_movies-1))
        self.svd_matrix = self.svd.fit_transform(self.user_item_matrix)
```

### Strengths
-  No content information needed
-  Discovers complex patterns
-  Works well with explicit ratings

### Limitations
-  Cold start problem for new users/items
-  Sparsity issues
-  Popularity bias

##  Neural Network Embeddings

### Architecture Overview

```
Input Layer
    ↓
User Embedding (50 dim) + Movie Embedding (50 dim)
    ↓
Concatenate → [100 dimensions]
    ↓
Dense Layer (128 units) + ReLU + Dropout
    ↓
Dense Layer (64 units) + ReLU + Dropout  
    ↓
Dense Layer (32 units) + ReLU + Dropout
    ↓
Output Layer (1 unit) → Predicted Rating
```

### Mathematical Model

#### Embedding Layers
```
user_embedding = Embedding(num_users, embedding_dim)
movie_embedding = Embedding(num_movies, embedding_dim)

user_vector = user_embedding(user_id)
movie_vector = movie_embedding(movie_id)
```

#### Neural Network
```
combined = concatenate([user_vector, movie_vector])
hidden1 = ReLU(Dense(128)(combined))
hidden2 = ReLU(Dense(64)(hidden1))  
hidden3 = ReLU(Dense(32)(hidden2))
output = Dense(1)(hidden3)
```

### Implementation

```python
class NeuralEmbeddingModel(nn.Module):
    def __init__(self, n_users, n_movies, embedding_dim=50):
        super().__init__()
        self.user_embedding = nn.Embedding(n_users, embedding_dim)
        self.movie_embedding = nn.Embedding(n_movies, embedding_dim)
        self.layers = nn.Sequential(
            nn.Linear(embedding_dim * 2, 128),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(128, 64),
            nn.ReLU(), 
            nn.Dropout(0.2),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(32, 1)
        )
```

### Training Process
- **Loss Function**: Mean Squared Error (MSE)
- **Optimizer**: Adam (lr=0.001)
- **Batch Size**: 32
- **Epochs**: 10-50 (early stopping)
- **Validation Split**: 20%

### Strengths
-  Captures complex non-linear patterns
-  Handles sparse data better
-  Continuous learning capability

### Limitations
-  Computationally intensive
-  Requires substantial data
-  Black box interpretation

##  Content-Based Filtering

### Feature Engineering

#### Text Processing Pipeline
```
Movie Metadata → TF-IDF Vectorization → Similarity Matrix
```

#### TF-IDF Calculation
```
TF(t,d) = frequency of term t in document d
IDF(t) = log(N / documents containing t)  
TF-IDF(t,d) = TF(t,d) * IDF(t)
```

### Implementation

```python
class ContentBasedFiltering:
    def fit(self, movies_df):
        # Combine genres into text features
        movies_df['content'] = movies_df['genres'].fillna('')
        
        # TF-IDF Vectorization
        tfidf = TfidfVectorizer(stop_words='english', max_features=5000)
        self.tfidf_matrix = tfidf.fit_transform(movies_df['content'])
        
        # Cosine similarity
        self.cosine_sim = linear_kernel(self.tfidf_matrix, self.tfidf_matrix)
```

### Similarity Calculation
```
similarity(movie_i, movie_j) = cosine_similarity(TFIDF(movie_i), TFIDF(movie_j))
```

### Strengths
-  No cold start for new items
-  Transparent recommendations
-  Works with minimal user data

### Limitations  
-  Limited to content features
-  Overspecialization
-  Requires good metadata

##  Hybrid Approach

### Weighted Combination Strategy

```
Final Score = w1 * CF_Score + w2 * NN_Score + w3 * CB_Score
where w1 + w2 + w3 = 1
```

### Default Weights
```python
weights = {
    'collaborative': 0.4,  # 40% weight
    'neural': 0.4,         # 40% weight  
    'content': 0.2         # 20% weight
}
```

### Adaptive Weighting
Weights can be dynamically adjusted based on:
- User history length
- Data sparsity
- Time of day
- Device type

### Implementation

```python
class AdvancedHybridEngine:
    def recommend(self, user_id, user_ratings=None, n_recommendations=10):
        # Get recommendations from all engines
        cf_recs = self.cf_engine.recommend(user_id, n_recommendations*2)
        neural_recs = self.neural_engine.recommend(user_id, n_recommendations*2)
        content_recs = self.get_content_recommendations(user_ratings, n_recommendations)
        
        # Weighted combination
        combined_scores = self.combine_scores(cf_recs, neural_recs, content_recs)
        
        return self.rank_recommendations(combined_scores, n_recommendations)
```

##  Performance Optimizations

### Caching Strategy
- Redis cache for user recommendations
- 1-hour TTL for fresh results
- Cache invalidation on new ratings

### Parallel Processing
```python
async def batch_recommendations(user_ids):
    tasks = [get_recommendations(user_id) for user_id in user_ids]
    return await asyncio.gather(*tasks)
```

### Memory Optimization
- Sparse matrix operations
- Incremental learning
- Model quantization

##  Algorithm Selection Guide

### Use Case Matrix

| Scenario | Recommended Algorithm | Why |
|----------|---------------------|------|
| New User | Content-Based | No rating history available |
| Power User | Hybrid | Maximizes accuracy with rich data |
| Real-time | Collaborative | Fast inference, pre-computed |
| Cold Start | Neural + Content | Handles sparse data well |
| Diversity | Hybrid with high content weight | Reduces filter bubbles |

### Parameter Tuning

#### Collaborative Filtering
```python
optimal_params = {
    'n_components': 'auto',  # Based on matrix size
    'min_similarity': 0.1,   # Minimum user similarity
    'neighborhood_size': 20  # Number of similar users
}
```

#### Neural Network
```python
training_params = {
    'embedding_dim': 50,     # Balance of performance/memory
    'learning_rate': 0.001,  # Adam optimizer default
    'dropout_rate': 0.2,     # Regularization
    'batch_size': 32,        # Memory constraints
    'early_stopping': True   # Prevent overfitting
}
```

##  Evaluation Metrics

### Accuracy Metrics
- **RMSE**: Root Mean Square Error
- **MAE**: Mean Absolute Error  
- **Precision@K**: % of relevant items in top K
- **Recall@K**: % of all relevant items found in top K

### Beyond Accuracy
- **Coverage**: % of items that can be recommended
- **Diversity**: Variety of recommendations
- **Novelty**: Recommendation of less popular items
- **Serendipity**: Unexpected but relevant recommendations

---

*Last Updated: 2025 | Fayssal Sabri*
```

