import streamlit as st
import pandas as pd
import requests
import time
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Page configuration
st.set_page_config(
    page_title="RecomSys-Flix",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Advanced custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3.5rem;
        background: linear-gradient(45deg, #E50914, #B81D24);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 900;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .movie-card {
        padding: 1.5rem;
        border-radius: 15px;
        border: none;
        margin: 1rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .movie-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 35px rgba(0,0,0,0.2);
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #2c3e50 0%, #3498db 100%);
    }
    .stButton>button {
        background: linear-gradient(45deg, #E50914, #B81D24);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(229, 9, 20, 0.4);
    }
    .tab-content {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
    }
    .engine-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin: 0.25rem;
    }
    .hybrid-badge { background: linear-gradient(45deg, #FF6B6B, #4ECDC4); color: white; }
    .collab-badge { background: linear-gradient(45deg, #45B7D1, #96C93D); color: white; }
    .neural-badge { background: linear-gradient(45deg, #B06AB3, #4568DC); color: white; }
    .content-badge { background: linear-gradient(45deg, #F093FB, #F5576C); color: white; }
</style>
""", unsafe_allow_html=True)

# Session state initialization
if 'recommendation_history' not in st.session_state:
    st.session_state.recommendation_history = []
if 'user_feedback' not in st.session_state:
    st.session_state.user_feedback = {}
if 'favorite_movies' not in st.session_state:
    st.session_state.favorite_movies = {}
if 'similar_mode' not in st.session_state:
    st.session_state.similar_mode = False
if 'random_mode' not in st.session_state:
    st.session_state.random_mode = False

# Main header with animation
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown('<div class="main-header">🎬 RecomSys-Flix</div>', unsafe_allow_html=True)
    st.markdown("### 🍿 Your Personal Movie Recommendation Expert")

# Enhanced sidebar
with st.sidebar:
    st.markdown("""
    <style>
    .sidebar-header {
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-header"><h1>⚙️ Configuration</h1></div>', unsafe_allow_html=True)
    
    # User Section
    st.subheader("👤 User Profile")
    user_id = st.number_input(
        "User ID", 
        min_value=1, 
        max_value=1000, 
        value=1,
        help="Unique user identifier"
    )
    
    # Advanced mode
    with st.expander("🎛️ Advanced Settings", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            diversity = st.slider("Diversity", 0.1, 1.0, 0.7, 
                                help="Balance between popularity and discovery")
        with col2:
            novelty = st.slider("Novelty", 0.1, 1.0, 0.5,
                              help="Preference for recent movies")
    
    # Recommendation Section
    st.subheader(" Recommendation Settings")
    n_recommendations = st.slider(
        "Number of recommendations",
        min_value=1,
        max_value=20,
        value=10,
        help="Number of movies to recommend"
    )
    
    engine_type = st.radio(
        "Engine type",
        ["Hybrid 🤝🧠", "Collaborative 🤝", "Neural 🧠", "Content 🎭"],
        index=0,
        help="Choose recommendation algorithm"
    )
    
    # Recommendation button with style
    get_recommendations = st.button(
        " Get Personalized Recommendations",
        width='stretch',
        type="primary"
    )
    
    st.markdown("---")
    
    # Real-time statistics
    st.subheader(" Live Statistics")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Users", "1.2K", "+15%")
    with col2:
        st.metric("Movies", "5.6K", "+8%")
    with col3:
        st.metric("Accuracy", "87%", "+2.1%")
    
    # Quick actions
    st.markdown("---")
    st.subheader(" Quick Actions")
    
    if st.button(" Similar Recommendations", width='stretch'):
        st.session_state.similar_mode = True
        st.rerun()
    
    if st.button(" Random Discovery", width='stretch'):
        st.session_state.random_mode = True
        st.rerun()

# Extended movie database
def get_extended_movie_database():
    """Extended database with more movies"""
    return {
        101: {"title": "Inception", "genre": "Sci-Fi", "year": 2010, "rating": 8.8, 
              "director": "Christopher Nolan", "duration": 148, "poster": "🎭", "description": "A thief who steals corporate secrets through dream-sharing technology."},
        102: {"title": "The Dark Knight", "genre": "Action", "year": 2008, "rating": 9.0,
              "director": "Christopher Nolan", "duration": 152, "poster": "🦇", "description": "Batman faces the Joker, a criminal mastermind seeking to create chaos."},
        103: {"title": "Pulp Fiction", "genre": "Crime", "year": 1994, "rating": 8.9,
              "director": "Quentin Tarantino", "duration": 154, "poster": "💉", "description": "Various interconnected stories of criminals in Los Angeles."},
        104: {"title": "Forrest Gump", "genre": "Drama", "year": 1994, "rating": 8.8,
              "director": "Robert Zemeckis", "duration": 142, "poster": "🏃", "description": "The presidencies of Kennedy and Johnson through the eyes of an Alabama man."},
        105: {"title": "The Matrix", "genre": "Sci-Fi", "year": 1999, "rating": 8.7,
              "director": "The Wachowskis", "duration": 136, "poster": "💊", "description": "A computer hacker learns about the true nature of reality."},
        106: {"title": "Goodfellas", "genre": "Crime", "year": 1990, "rating": 8.7,
              "director": "Martin Scorsese", "duration": 146, "poster": "🔫", "description": "The story of Henry Hill and his life in the mob."},
        107: {"title": "The Godfather", "genre": "Crime", "year": 1972, "rating": 9.2,
              "director": "Francis Ford Coppola", "duration": 175, "poster": "🎩", "description": "The aging patriarch of an organized crime dynasty transfers control to his son."},
        108: {"title": "Fight Club", "genre": "Drama", "year": 1999, "rating": 8.8,
              "director": "David Fincher", "duration": 139, "poster": "👊", "description": "An insomniac office worker forms an underground fight club."},
        109: {"title": "Interstellar", "genre": "Sci-Fi", "year": 2014, "rating": 8.6,
              "director": "Christopher Nolan", "duration": 169, "poster": "", "description": "A team of explorers travel through a wormhole in space."},
        110: {"title": "Parasite", "genre": "Thriller", "year": 2019, "rating": 8.6,
              "director": "Bong Joon-ho", "duration": 132, "poster": "🏠", "description": "Greed and class discrimination threaten the newly formed symbiotic relationship."},
        111: {"title": "The Shawshank Redemption", "genre": "Drama", "year": 1994, "rating": 9.3,
              "director": "Frank Darabont", "duration": 142, "poster": "⛓️", "description": "Two imprisoned men bond over a number of years, finding solace and eventual redemption."},
        112: {"title": "The Lord of the Rings: The Return of the King", "genre": "Fantasy", "year": 2003, "rating": 8.9,
              "director": "Peter Jackson", "duration": 201, "poster": "💍", "description": "Gandalf and Aragorn lead the World of Men against Sauron's army."},
        113: {"title": "Spirited Away", "genre": "Animation", "year": 2001, "rating": 8.6,
              "director": "Hayao Miyazaki", "duration": 125, "poster": "🐉", "description": "During her family's move to the suburbs, a girl wanders into a world ruled by gods."},
        114: {"title": "La La Land", "genre": "Musical", "year": 2016, "rating": 8.0,
              "director": "Damien Chazelle", "duration": 128, "poster": "🎵", "description": "While navigating their careers in Los Angeles, a pianist and an actress fall in love."},
        115: {"title": "Get Out", "genre": "Horror", "year": 2017, "rating": 7.7,
              "director": "Jordan Peele", "duration": 104, "poster": "😨", "description": "A young African-American visits his white girlfriend's parents for the weekend."}
    }

def get_recommendations_from_api(user_id, n_recommendations, engine_type):
    """Calls recommendation API with enhanced error handling"""
    try:
        engine_map = {
            "Hybrid 🤝🧠": "hybrid",
            "Collaborative 🤝": "collaborative", 
            "Neural 🧠": "neural",
            "Content 🎭": "content"
        }
        
        # Simulate data if API is not available
        if not is_api_available():
            return simulate_recommendations(user_id, n_recommendations, engine_type)
        
        response = requests.post(
            "http://localhost:8000/api/v1/recommend",
            json={
                "user_id": user_id,
                "n_recommendations": n_recommendations,
                "engine_type": engine_map.get(engine_type, "hybrid"),
                "diversity": diversity,
                "novelty": novelty
            },
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"❌ API Error {response.status_code}: {response.text}")
            return simulate_recommendations(user_id, n_recommendations, engine_type)
            
    except requests.exceptions.ConnectionError:
        st.warning("🌐 API unavailable - Using simulation mode")
        return simulate_recommendations(user_id, n_recommendations, engine_type)
    except Exception as e:
        st.error(f"❌ Unexpected error: {str(e)}")
        return simulate_recommendations(user_id, n_recommendations, engine_type)

def is_api_available():
    """Checks if API is available"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def simulate_recommendations(user_id, n_recommendations, engine_type):
    """Simulates recommendations when API is unavailable"""
    import random
    movie_db = get_extended_movie_database()
    all_movies = list(movie_db.keys())
    
    # Simulation based on user and engine type
    random.seed(user_id + hash(engine_type))
    recommendations = random.sample(all_movies, min(n_recommendations, len(all_movies)))
    
    return {
        "user_id": user_id,
        "recommendations": recommendations,
        "scores": [round(random.uniform(0.7, 0.95), 2) for _ in recommendations],
        "engine_type": engine_type.split(" ")[0].lower(),
        "simulated": True
    }

def create_movie_card(movie, rank, score, engine_type):
    """Creates an attractive movie card"""
    movie_db = get_extended_movie_database()
    movie_info = movie_db.get(movie, {
        "title": f"Movie {movie}", "genre": "Unknown", "year": "N/A", 
        "rating": "N/A", "director": "Unknown", "duration": "N/A", "poster": "🎬",
        "description": "No description available"
    })
    
    with st.container():
        st.markdown(f"""
        <div class="movie-card">
            <div style="display: flex; justify-content: space-between; align-items: start;">
                <div style="flex: 1;">
                    <h3 style="margin: 0; color: white;">#{rank} {movie_info['poster']} {movie_info['title']} ({movie_info['year']})</h3>
                    <p style="margin: 0.5rem 0; color: #e0e0e0;">
                        <strong>Genre:</strong> {movie_info['genre']} • 
                        <strong>Director:</strong> {movie_info['director']} • 
                        <strong>Duration:</strong> {movie_info['duration']} min
                    </p>
                    <p style="margin: 0.5rem 0; color: #e0e0e0; font-style: italic;">
                        {movie_info['description']}
                    </p>
                    <div style="display: flex; gap: 1rem; align-items: center;">
                        <span style="background: rgba(255,255,255,0.2); padding: 0.25rem 0.75rem; border-radius: 15px;">
                            ⭐ {movie_info['rating']}/10
                        </span>
                        <span style="background: rgba(255,255,255,0.2); padding: 0.25rem 0.75rem; border-radius: 15px;">
                             Score: {score}
                        </span>
                    </div>
                </div>
                <div style="text-align: right;">
                    <span class="engine-badge {engine_type.lower()}-badge">
                        {engine_type}
                    </span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # User actions
        col1, col2, col3, col4 = st.columns([2,1,1,1])
        with col1:
            if st.button(f"❤️ Add to Favorites", key=f"fav_{movie}_{rank}", width='stretch'):
                st.session_state.favorite_movies[movie] = movie_info
                st.success(f"❤️ {movie_info['title']} added to favorites!")
        with col2:
            if st.button("👁️ Details", key=f"detail_{movie}_{rank}", width='stretch'):
                st.session_state.selected_movie = movie_info
        with col3:
            if st.button("👍", key=f"like_{movie}_{rank}", width='stretch'):
                st.session_state.user_feedback[movie] = "like"
                st.rerun()
        with col4:
            if st.button("👎", key=f"dislike_{movie}_{rank}", width='stretch'):
                st.session_state.user_feedback[movie] = "dislike"
                st.rerun()

def create_analytics_dashboard():
    """Creates an advanced analytics dashboard"""
    st.header(" Advanced Analytics")
    
    # Main metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Recommendations Today", "142", "+12%")
    with col2:
        st.metric("Avg Response Time", "0.23s", "-5%")
    with col3:
        st.metric("Satisfaction Rate", "89%", "+3.2%")
    with col4:
        st.metric("New Users", "24", "+8%")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Genre distribution
        genre_data = pd.DataFrame({
            'Genre': ['Action', 'Drama', 'Comedy', 'Sci-Fi', 'Thriller', 'Crime', 'Fantasy'],
            'Recommendations': [25, 20, 18, 15, 12, 8, 2]
        })
        fig = px.pie(genre_data, values='Recommendations', names='Genre', 
                     title=' Recommended Genre Distribution',
                     color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig, width='stretch')
    
    with col2:
        # Engine performance
        engine_data = pd.DataFrame({
            'Engine': ['Hybrid', 'Collaborative', 'Neural', 'Content'],
            'Accuracy': [87, 82, 79, 75],
            'Speed (ms)': [230, 180, 450, 320]
        })
        fig = px.bar(engine_data, x='Engine', y=['Accuracy', 'Speed (ms)'],
                    title=' Algorithm Performance',
                    barmode='group')
        st.plotly_chart(fig, width='stretch')
    
    # Activity heatmap
    st.subheader("🌡️ Activity Heatmap")
    activity_data = pd.DataFrame({
        'Hour': [f'{h:02d}:00' for h in range(24)],
        'Monday': [10,8,5,3,2,4,15,45,67,89,78,65,70,68,72,80,85,90,95,88,75,60,40,25],
        'Tuesday': [12,9,6,4,3,5,18,48,70,92,82,68,73,70,75,83,88,93,98,90,78,63,42,28]
    }).melt(id_vars=['Hour'], var_name='Day', value_name='Activity')
    
    fig = px.density_heatmap(activity_data, x='Hour', y='Day', z='Activity',
                            title='User Activity by Hour and Day',
                            color_continuous_scale='Viridis')
    st.plotly_chart(fig, width='stretch')

# Tab navigation
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    " Recommendations", 
    " Analytics", 
    " Favorites", 
    " History",
    " About"
])

with tab1:
    st.header("🎬 Personalized Recommendations")
    
    if get_recommendations or st.session_state.get('similar_mode') or st.session_state.get('random_mode'):
        with st.spinner("🔍 Analyzing your preferences and finding the best movies..."):
            start_time = time.time()
            
            # Determine query type
            current_engine_type = engine_type
            if st.session_state.get('similar_mode'):
                current_engine_type = "Hybrid 🤝🧠"
                st.info("🔍 Finding movies similar to your favorites...")
            elif st.session_state.get('random_mode'):
                current_engine_type = "Content 🎭"
                st.info(" Exploring diverse movies for you...")
            
            recommendations_data = get_recommendations_from_api(
                user_id, n_recommendations, current_engine_type
            )
            
            response_time = time.time() - start_time
            
            # Reset modes
            st.session_state.similar_mode = False
            st.session_state.random_mode = False
            
            if recommendations_data:
                # Results header
                col1, col2 = st.columns([3,1])
                with col1:
                    st.success(f" {len(recommendations_data['recommendations'])} recommendations generated in {response_time:.2f}s")
                with col2:
                    if recommendations_data.get('simulated'):
                        st.warning(" Simulation Mode Active")
                
                # Performance metrics
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("👤 User", user_id)
                with col2:
                    st.metric(" Recommendations", len(recommendations_data["recommendations"]))
                with col3:
                    st.metric(" Engine", current_engine_type.split(" ")[0])
                with col4:
                    st.metric(" Time", f"{response_time:.2f}s")
                
                # Display recommendations
                st.subheader("🎭 Movies Recommended For You")
                
                movie_ids = recommendations_data["recommendations"]
                scores = recommendations_data.get("scores", [1.0] * len(movie_ids))
                
                for i, (movie_id, score) in enumerate(zip(movie_ids, scores), 1):
                    create_movie_card(movie_id, i, score, current_engine_type.split(" ")[0])
                
                # Score chart
                if len(scores) > 1:
                    st.subheader(" Confidence Score Analysis")
                    scores_df = pd.DataFrame({
                        'Movie': [f"Movie {i+1}" for i in range(len(scores))],
                        'Score': scores
                    })
                    fig = px.bar(scores_df, x='Movie', y='Score', 
                                title='Confidence Score Distribution',
                                color='Score', color_continuous_scale='Viridis')
                    st.plotly_chart(fig, width='stretch')
                
                # Save to history
                history_entry = {
                    'timestamp': datetime.now(),
                    'user_id': user_id,
                    'engine_type': current_engine_type,
                    'recommendations': movie_ids,
                    'response_time': response_time
                }
                st.session_state.recommendation_history.append(history_entry)
    
    else:
        # Welcome screen
        st.info("""
         **Welcome to RecomSys-Flix!**
        
        To get started:
        1.  Configure your preferences in the sidebar
        2.  Click *"Get Personalized Recommendations"*
        3.  Discover movies tailored to your taste!
        
        **Available Features:**
        - 🤝 **Collaborative Filtering**: Based on similar users
        - 🧠 **Neural Networks**: Advanced artificial intelligence  
        - 🎭 **Content Filtering**: Based on movie characteristics
        - 🌟 **Hybrid Approach**: The best of all three worlds!
        """)

with tab2:
    create_analytics_dashboard()

with tab3:
    st.header("❤️ Your Favorite Movies")
    
    if st.session_state.favorite_movies:
        st.success(f"🎉 You have {len(st.session_state.favorite_movies)} movies in your favorites!")
        
        for i, (movie_id, movie_info) in enumerate(st.session_state.favorite_movies.items(), 1):
            with st.container():
                st.markdown(f"""
                <div style="padding: 1rem; border-radius: 10px; background: #f0f2f6; margin: 0.5rem 0;">
                    <h4>#{i} {movie_info['poster']} {movie_info['title']} ({movie_info['year']})</h4>
                    <p><strong>Genre:</strong> {movie_info['genre']} • <strong>Director:</strong> {movie_info['director']}</p>
                    <p>⭐ <strong>Rating:</strong> {movie_info['rating']}/10</p>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns([1, 4])
                with col1:
                    if st.button("🗑️ Remove", key=f"remove_{movie_id}"):
                        del st.session_state.favorite_movies[movie_id]
                        st.rerun()
                with col2:
                    if st.button(" Similar movies", key=f"similar_{movie_id}"):
                        st.session_state.similar_mode = True
                        st.rerun()
    else:
        st.info(" You don't have any favorite movies yet. Add some by clicking ❤️!")

with tab4:
    st.header(" Recommendation History")
    
    if st.session_state.recommendation_history:
        # History chart
        history_df = pd.DataFrame(st.session_state.recommendation_history)
        history_df['date'] = history_df['timestamp'].dt.date
        
        if len(history_df) > 1:
            fig = px.line(history_df, x='timestamp', y='response_time',
                         title=' Response Time Evolution',
                         labels={'response_time': 'Time (s)', 'timestamp': 'Date'})
            st.plotly_chart(fig, width='stretch')
        
        # History details
        for i, entry in enumerate(reversed(st.session_state.recommendation_history[-10:]), 1):
            with st.expander(f"📅 Session {i} - {entry['timestamp'].strftime('%m/%d/%Y %H:%M')}"):
                st.write(f"**User:** {entry['user_id']}")
                st.write(f"**Engine:** {entry['engine_type']}")
                st.write(f"**Response time:** {entry['response_time']:.2f}s")
                st.write(f"**Movies recommended:** {len(entry['recommendations'])}")
    else:
        st.info(" No history available. Make your first recommendation!")

with tab5:
    st.header(" About RecomSys-Flix")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ###  What is RecomSys-Flix?
        
        **RecomSys-Flix** is an intelligent movie recommendation system that uses 
        artificial intelligence to discover your next favorite movies.
        
        ### 🧠 How It Works
        
        Our system combines several advanced approaches:
        
        **🤝 Collaborative Filtering**
        - Analyzes similarities between users
        - "People like you also enjoyed..."
        
        **🧠 Neural Networks** 
        - Deep learning of preferences
        - Complex pattern detection
        
        **🎭 Content-Based Filtering**
        - Analyzes movie characteristics
        - Recommendations by content similarity
        
        **🌟 Hybrid Approach**
        - Intelligent combination of methods
        - Better accuracy and diversity
        
        ###  Performance
        
        -  **Speed**: Responses in under one second
        -  **Accuracy**: 87% satisfaction rate
        -  **Scalability**: Supports 1000+ concurrent users
        -  **Adaptive**: Improves with your feedback
        """)
    
    with col2:
        st.image("https://img.icons8.com/color/200/000000/cinema-.png", width=150)
        st.markdown("""
        ###  Architecture
        
        - **Backend**: FastAPI + Python
        - **Machine Learning**: PyTorch + Scikit-learn
        - **Frontend**: Streamlit
        - **Cache**: Redis
        - **Data**: MovieLens + TMDB
        
        ###  Key Metrics
        
        -  19 automated tests
        -  100% containerized
        -  Responsive interface
        -  Secure and private
        """)
    
    # Contact section
    st.markdown("---")
    st.subheader("📞 Support & Contact")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**Report a Bug**")
        st.write("Open an issue on GitHub")
    with col2:
        st.markdown("**Suggestion**")
        st.write("Share your improvement ideas")
    with col3:
        st.markdown("**Development**")
        st.write("Contribute to the open source project")

# Enhanced footer
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>🎬 <strong>RecomSys-Flix</strong> - Intelligent Movie Recommendation System</p>
        <p>Developed with ❤️ by Fayssal Sabri</p>
        <p style='font-size: 0.8rem;'>© 2024 RecomSys-Flix Team - All rights reserved</p>
    </div>
    """, unsafe_allow_html=True)

# JavaScript for interactions
st.markdown("""
<script>
// Animation for movie cards
document.addEventListener('DOMContentLoaded', function() {
    const cards = document.querySelectorAll('.movie-card');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
    });
});
</script>
""", unsafe_allow_html=True)