import streamlit as st
import pandas as pd
import random
import altair as alt

# ---------------- About Netflix ----------------
st.markdown("## ℹ️ About Netflix")
st.markdown(
    """
    Netflix is the world’s leading streaming entertainment service, offering a wide variety of TV shows, movies, anime,
    documentaries, and more on thousands of internet-connected devices. Members can watch as much as they want,
    anytime, anywhere – all for one low monthly price.
    """,
    unsafe_allow_html=True
)

# --- Title and Banner ---
st.markdown('<h1 style="color: red; background-color:white; text-align: center">Netflix Dashboard</h1>', unsafe_allow_html=True)
st.image('Assets/netflix.jpg', use_column_width=True)

# --- Overview Section ---
st.markdown("## 📊 Overview")

# Load your dataset
df = pd.read_csv(r'C:\Users\anamika\OneDrive\Desktop\Netflix\Data Analysis\netflix_titles.csv')

# KPI Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Titles", len(df))
col2.metric("Movies", df[df['type'] == 'Movie'].shape[0])
col3.metric("TV Shows", df[df['type'] == 'TV Show'].shape[0])

st.markdown("---")

# --- Popular Titles Section ---
st.markdown("## 🎞️ Popular Titles on Netflix")

# Pick 6 random unique titles
movie_titles = df[['title', 'type']].drop_duplicates().sample(6, random_state=42)

# Dictionary to store your own movie poster links
# Add your own image URLs here
# Dictionary with poster path + movie description
custom_posters = {
    "Game Over, Man!": {
        "poster": "Assets/Game over man.jpg",
        "desc": "Three friends must save the day when terrorists take over their hotel."
    },
    "Arsenio Hall: Smart & Classy": {
        "poster": "Assets/Arsenio Hall Smart & Classy.jpg",
        "desc": "Stand-up comedy special full of charm and sharp humor."
    },
    "Kazoops!": {
        "poster": "Assets/Kazoops!.jpg",
        "desc": "A curious boy and his pet pig challenge the world’s preconceptions."
    },
    "We Are the Champions": {
        "poster": "Assets/We Are the Champions.jpg",
        "desc": "Exploring the world’s most unique and quirky competitions."
    },
    "Pablo Escobar, el patrón del mal": {
        "poster": "Assets/Pablo Escobar, el patrón del mal.jpg",
        "desc": "The life story of the infamous Colombian drug lord."
    },
    "Saint Seiya: The Lost Canvas": {
        "poster": "Assets/Saint Seiya The Lost Canvas.jpg",
        "desc": "Epic battles of knights defending the goddess Athena."
    }
}

# Function to get poster + description or placeholder
def get_movie_data(title):
    if title in custom_posters:
        data = custom_posters[title]
        return data["poster"].replace("\\", "/").strip(), data["desc"]
    else:
        return f"https://via.placeholder.com/300x450?text={title.replace(' ', '+')}", "No description available."

# Display posters with name + description
cols = st.columns(3)
for i, (_, row) in enumerate(movie_titles.iterrows()):
    with cols[i % 3]:
        poster_url, description = get_movie_data(row['title'])
        
        st.image(poster_url, use_column_width=True)
        st.markdown(
            f"<p style='text-align:center; font-weight:bold; margin-top:8px;'>{row['title']}</p>"
            f"<p style='text-align:center; font-size:14px; color:gray;'>{description}</p>",
            unsafe_allow_html=True
        )

# ---------------- KPI Section ----------------
col1, col2, col3 = st.columns(3)
col1.metric("Total Titles", len(df))
col2.metric("Movies", df[df['type'] == 'Movie'].shape[0])
col3.metric("TV Shows", df[df['type'] == 'TV Show'].shape[0])

st.markdown("---")

# ---------------- Top Genres Chart ----------------
st.markdown("## 📈 Most Popular Genres on Netflix")
df_genres = df['listed_in'].str.split(',').explode().str.strip()
genre_counts = df_genres.value_counts().reset_index()
genre_counts.columns = ['Genre', 'Count']

chart = alt.Chart(genre_counts.head(10)).mark_bar().encode(
    x='Count',
    y=alt.Y('Genre', sort='-x'),
    color=alt.Color('Genre', legend=None)
).properties(height=400)
st.altair_chart(chart, use_container_width=True)

st.markdown("---")

# ---------------- Recently Added Section ----------------
st.markdown("## 🆕 Recently Added Titles")
recent = df[['title', 'release_year', 'description']].dropna().sample(5)
for _, row in recent.iterrows():
    st.markdown(
        f"""
        <div style="padding:10px; border-radius:8px; background-color:#1f1f1f; margin-bottom:10px;">
            <h4 style="color:red;">{row['title']} ({row['release_year']})</h4>
            <p style="color:white; font-size:14px;">{row['description']}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("---")

# ---------------- Fun Fact Section ----------------
fun_facts = [
    "Netflix started as a DVD rental service in 1997.",
    "Netflix has over 230 million subscribers worldwide.",
    "The first Netflix original was 'House of Cards' in 2013.",
    "Binge-watching is a term popularized because of Netflix."
]
st.markdown(
    f"<p style='background-color:#ff4b4b; padding:10px; color:white; text-align:center; border-radius:5px;'>💡 Fun Fact: {random.choice(fun_facts)}</p>",
    unsafe_allow_html=True
)

st.markdown("---")
