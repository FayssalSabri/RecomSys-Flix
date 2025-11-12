<div align="center">

# RecomSys-Flix

### AI-Powered Movie Recommendation System

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104%2B-009688?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-FF4B4B?style=flat-square&logo=streamlit)](https://streamlit.io)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.1%2B-EE4C2C?style=flat-square&logo=pytorch)](https://pytorch.org)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)
[![Supabase](https://img.shields.io/badge/Supabase-Database-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)](https://supabase.com)

**Hybrid recommendation engine combining collaborative filtering and neural networks**

[Quick Start](#installation) • [Demo](#demo) • [Architecture](#architecture) • [API](#api) • [Documentation](#documentation)

</div>

---

## Overview

RecomSys-Flix is a movie recommendation system that combines three AI approaches to achieve 87% precision. Designed for easy deployment with Docker, it provides a RESTful API and modern user interface.

### Key Features

**Triple AI Engine** - Collaborative filtering + Neural networks + Hybrid approach  
**Response Time** - < 500ms average  
**Precision** - 87% with hybrid engine  
**RESTful API** - Interactive documentation with FastAPI  
**Modern Interface** - Streamlit dashboard with interactive visualizations  
**Docker Ready** - One-command deployment

---

## Demo

<div align="center">

### User Interface
![RecomSys-Flix Interface](img/RecomSys-Flix.png)

### Analytics Dashboard
![Analytics](img/RecomSys-Flix-Analytics.png)

### Personalized Recommendations
![Results](img/RecomSys-Flix-Results.png)

</div>

---

## Installation

### Prerequisites

- Python 3.8+
- Docker (optional)
- 4GB RAM minimum

### Quick Start

```bash
# Clone repository
git clone https://github.com/FayssalSabri/RecomSys-Flix.git
cd RecomSys-Flix

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
pip install -r requirements_streamlit.txt
```

### Launch

**Option 1: Manual (development)**

```bash
# Terminal 1 - API Backend
uvicorn app.main:app --reload

# Terminal 2 - Web Interface
streamlit run streamlit_app/main.py
```

**Option 2: Docker (production)**

```bash
docker-compose up --build
```
---

## Architecture

```
┌─────────────────┐
│  Streamlit UI   │
└────────┬────────┘
         │
┌────────▼────────┐      ┌──────────────┐
│   FastAPI       │◄─────┤  Redis Cache │
└────────┬────────┘      └──────────────┘
         │
┌────────▼────────┐      ┌──────────────┐
│  Hybrid Engine  │◄─────┤  PostgreSQL  │
└────────┬────────┘      └──────────────┘
         │
    ┌────┴────┬────────┐
    ▼         ▼        ▼
┌────────┐ ┌──────┐ ┌─────────┐
│Collab. │ │Neural│ │Content  │
│Filter  │ │  Net │ │  Based  │
└────────┘ └──────┘ └─────────┘
```

### Technologies

| Component | Technology | Role |
|-----------|------------|------|
| **Backend** | FastAPI | RESTful API |
| **Frontend** | Streamlit | User interface |
| **ML Collaborative** | scikit-learn | User similarity, SVD |
| **ML Neural** | PyTorch | Deep embeddings |
| **Cache** | Redis | Performance |
| **Database** | PostgreSQL/Supabase | Persistent storage |

### Database Schema

<img src="img/database_demo.gif" width="600" alt="Database schema" />

---

## Performance

| Method | Precision | Recall | F1-Score | Time | Best Use Case |
|---------|-----------|--------|----------|-------|---------------|
| Collaborative | 82% | 78% | 80% | 0.3s | Established users |
| Neural | 79% | 81% | 80% | 0.5s | Complex patterns |
| **Hybrid** | **87%** | **85%** | **86%** | **0.4s** | **All scenarios** |

**Key Metrics**
- Capacity: 1000+ requests/minute
- Memory: < 1GB for 100K users
- Scalability: Horizontal via Docker

---

## API

### Basic Request

```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/recommend",
    json={
        "user_id": 1,
        "n_recommendations": 5,
        "engine_type": "hybrid"
    }
)

print(response.json())
```

### JSON Response

```json
{
  "user_id": 1,
  "recommendations": [103, 107, 104],
  "movie_titles": ["Interstellar", "The Godfather", "Pulp Fiction"],
  "scores": [0.95, 0.87, 0.82],
  "engine_type": "hybrid",
  "processing_time_ms": 387
}
```

### Available Endpoints

| Route | Method | Description |
|-------|---------|-------------|
| `/api/v1/recommend` | POST | Get recommendations |
| `/api/v1/health` | GET | Service status |
| `/api/v1/models` | GET | List models |
| `/api/v1/metrics` | GET | Performance metrics |
| `/docs` | GET | Interactive documentation |

---

## Testing

```bash
# Full suite
pytest tests/ -v --cov=app

# Specific tests
pytest tests/test_services.py -v     # AI engines
pytest tests/test_api.py -v          # API
pytest tests/test_performance.py -v  # Performance

# Coverage report
pytest tests/ --cov=app --cov-report=html
```

---

## Deployment

### Docker (recommended)

```bash
docker-compose up -d
```

### AWS EC2

```bash
# Connect
ssh -i key.pem ubuntu@ec2-ip

# Install
git clone https://github.com/FayssalSabri/RecomSys-Flix.git
cd RecomSys-Flix
chmod +x deploy.sh
./deploy.sh production
```

### Environment Variables

```bash
ENVIRONMENT=production
API_HOST=0.0.0.0
API_PORT=8000
STREAMLIT_PORT=8501
LOG_LEVEL=INFO
```

---

## Customization

### Adjust Hybrid Weights

```python
from app.services.hybrid_engine import HybridEngine

engine = HybridEngine()
recommendations = engine.hybrid_recommend(
    user_id=1,
    n_recommendations=5,
    collaborative_weight=0.7,  # More collaborative weight
    neural_weight=0.3
)
```

### Modify Hyperparameters

**Collaborative Filtering**
```python
# app/services/collaborative_filtering.py
self.svd_model = TruncatedSVD(
    n_components=50,  # Increase for more precision
    n_iter=10
)
```

**Neural Networks**
```python
# app/services/neural_embeddings.py
self.model = NeuralEmbeddingModel(
    embedding_dim=64,
    hidden_layers=[128, 64, 32],
    dropout=0.2
)
```

---

## Documentation

- [Algorithm Details](docs/algorithms.md)
- [API Reference](http://localhost:8000/docs)
- [Performance Benchmarks](docs/benchmarks.md)

### Learning Resources

- [Collaborative Filtering](https://en.wikipedia.org/wiki/Collaborative_filtering)
- [Neural Collaborative Filtering](https://arxiv.org/abs/1708.05031)
- [Hybrid Systems](https://dl.acm.org/doi/10.1145/371920.372071)

---

## Roadmap

**v2.0 (Q1 2025)**
- Real-time learning
- A/B testing framework
- Explainable AI

**v2.5 (Q2 2025)**
- Content-based filtering
- Social recommendations
- Mobile application

**v3.0 (Q3 2025)**
- Distributed processing (Spark)
- Graph Neural Networks
- Multi-modal recommendations

---

## Contributing

Contributions are welcome!

1. Fork the project
2. Create a branch (`git checkout -b feature/improvement`)
3. Commit (`git commit -m 'Add feature'`)
4. Push (`git push origin feature/improvement`)
5. Open a Pull Request

---

## Support

- **Bugs**: [GitHub Issues](https://github.com/FayssalSabri/RecomSys-Flix/issues)
- **Ideas**: [Discussions](https://github.com/FayssalSabri/RecomSys-Flix/discussions)
- **Contact**: fayssal.sabri.pro@gmail.com

---

## License

MIT License - Free to use, modify and distribute.

---

## Acknowledgments

**MovieLens** • **FastAPI** • **Streamlit** • **PyTorch** • **scikit-learn** • **Supabase**

---

<div align="center">

**RecomSys-Flix** - Making every movie night perfect 🍿🎥

[Back to top](#recomsys-flix)

</div>