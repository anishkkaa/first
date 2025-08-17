import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("🎬 Netflix Dashboard")
st.write("Explore Netflix content by type, country, release year, genre, and more.")

# Load the dataset
df = pd.read_csv(r'C:\\Users\\anamika\\OneDrive\\Desktop\\Netflix\\Data Analysis\\netflix_titles.csv')

# Clean data
df['release_year'] = pd.to_numeric(df['release_year'], errors='coerce')
df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
df['month_added'] = df['date_added'].dt.month
df['main_genre'] = df['listed_in'].str.split(',').str[0]
df['duration_mins'] = df['duration'].str.extract('(\d+)').astype(float)
df['seasons'] = df['duration'].str.extract('(\d+)').astype(float)

# Sidebar filters
st.sidebar.header("📌 Filter Options")

selected_type = st.sidebar.multiselect("Select Type", df['type'].dropna().unique(), default=df['type'].dropna().unique())
selected_country = st.sidebar.multiselect("Select Country", df['country'].dropna().unique(), default=df['country'].dropna().unique())

min_year = int(df['release_year'].min())
max_year = int(df['release_year'].max())
selected_years = st.sidebar.slider("Select Release Year Range", min_value=min_year, max_value=max_year, value=(min_year, max_year))

# Filter the data
filtered_df = df[
    (df['type'].isin(selected_type)) &
    (df['country'].isin(selected_country)) &
    (df['release_year'] >= selected_years[0]) &
    (df['release_year'] <= selected_years[1])
]

st.subheader("🎯 Filtered Dataset Preview")
st.dataframe(filtered_df)

# ==========================
# CHARTS using filtered_df
# ==========================
st.markdown("**Insight:** ...")

# 1. Bar: Content Type by Rating
fig1 = px.bar(filtered_df, x='type', color='rating', title="Content Type Distribution by Rating")
st.plotly_chart(fig1, use_container_width=True)
st.markdown("**Insight:** Most content is Movies and rated TV-MA or TV-14, indicating mature audiences.")

# 2. Histogram: Release Years
fig2 = px.histogram(filtered_df, x='release_year', nbins=20, title="Releases by Year")
st.plotly_chart(fig2, use_container_width=True)
st.markdown("**Insight:** Releases increased steadily after 2010 and peaked around 2018–2020.")

# 3. Pie Chart: Movie vs TV Show
fig3 = px.pie(filtered_df, names='type', title='Share of Movies vs TV Shows')
st.plotly_chart(fig3, use_container_width=True)
st.markdown("**Insight:** Movies significantly outnumber TV Shows on Netflix.")

# 4. Bar: Top 10 Countries
top_countries = filtered_df['country'].value_counts().nlargest(10).reset_index()
top_countries.columns = ['Country', 'Count']
fig4 = px.bar(top_countries, x='Country', y='Count', title='Top 10 Countries by Content Count')
st.plotly_chart(fig4, use_container_width=True)
st.markdown("**Insight:** The USA and India are the leading content producers on Netflix.")

# 5. Bar: Top 10 Genres
top_genres = filtered_df['listed_in'].str.split(', ').explode().value_counts().nlargest(10).reset_index()
top_genres.columns = ['Genre', 'Count']
fig5 = px.bar(top_genres, x='Genre', y='Count', title='Top 10 Genres')
st.plotly_chart(fig5, use_container_width=True)
st.markdown("**Insight:** Drama dominates Netflix's genre catalog, followed by Comedy and Documentaries.")

# 6. Pie: Ratings Distribution
rating_counts = filtered_df['rating'].value_counts().reset_index()
rating_counts.columns = ['Rating', 'Count']
fig6 = px.pie(rating_counts, names='Rating', values='Count', title='Ratings Distribution')
st.plotly_chart(fig6, use_container_width=True)
st.markdown("**Insight:** TV-MA is the most common rating, showing focus on mature content.")

# 7. Line Chart: Yearly Releases
yearly_release = filtered_df['release_year'].value_counts().sort_index().reset_index()
yearly_release.columns = ['Year', 'Count']
fig7 = px.line(yearly_release, x='Year', y='Count', title='Content Released Over Time')
st.plotly_chart(fig7, use_container_width=True)
st.markdown("**Insight:** Yearly releases show rapid growth from 2015 onward.")

# 8. TV Show Season Distribution
tv_shows = filtered_df[filtered_df['type'] == 'TV Show']
fig8 = px.histogram(tv_shows, x='seasons', nbins=10, title='TV Show Season Count Distribution')
st.plotly_chart(fig8, use_container_width=True)
st.markdown("**Insight:** Most TV Shows have 1 to 3 seasons, indicating limited series formats.")

# 9. Movie Duration Distribution
movies = filtered_df[filtered_df['type'] == 'Movie']
fig9 = px.histogram(movies, x='duration_mins', nbins=20, title='Movie Duration Distribution (in Minutes)')
st.plotly_chart(fig9, use_container_width=True)
st.markdown("**Insight:** Majority of movies are between 80 to 120 minutes in duration.")

# 10. Top 10 Directors
top_directors = filtered_df['director'].dropna().value_counts().nlargest(10).reset_index()
top_directors.columns = ['Director', 'Count']
fig10 = px.bar(top_directors, x='Director', y='Count', title='Top 10 Directors')
st.plotly_chart(fig10, use_container_width=True)
st.markdown("**Insight:** A few directors have contributed multiple titles to Netflix.")

# 11. Sunburst: Type > Rating > Genre
sunburst_df = filtered_df.dropna(subset=['type', 'rating', 'main_genre'])
sunburst_df = sunburst_df[~sunburst_df['rating'].str.contains('min', na=False)]
fig11 = px.sunburst(sunburst_df, path=['type', 'rating', 'main_genre'], title='Sunburst: Type → Rating → Genre')
st.plotly_chart(fig11, use_container_width=True)
st.markdown("**Insight:** Drama is widespread across both Movies and TV Shows in multiple rating categories.")

# 12. Treemap: Country > Type
fig12 = px.treemap(filtered_df.dropna(subset=['country']), path=['country', 'type'], title='Treemap: Country → Type')
st.plotly_chart(fig12, use_container_width=True)
st.markdown("**Insight:** The USA produces a high amount of both Movies and TV Shows.")

# 13. Scatter: Movie Duration vs Year
fig13 = px.scatter(movies, x='release_year', y='duration_mins', trendline='ols', title='Movie Duration vs Release Year')
st.plotly_chart(fig13, use_container_width=True)
st.markdown("**Insight:** Movie durations have stayed fairly consistent over the years.")

# 14. Yearly Type Comparison
year_type_df = filtered_df.groupby(['release_year', 'type']).size().reset_index(name='Count')
fig14 = px.line(year_type_df, x='release_year', y='Count', color='type', title='Movies vs TV Shows Over Years')
st.plotly_chart(fig14, use_container_width=True)
st.markdown("**Insight:** Both Movies and TV Shows increased post-2015, but Movies remain dominant.")

# 15. Donut: Movie vs TV Show Share
fig15 = px.pie(filtered_df, names='type', hole=0.4, title='Donut: Content Type Distribution')
st.plotly_chart(fig15, use_container_width=True)
st.markdown("**Insight:** Movies represent a significantly larger portion than TV Shows.")

# 16. Box Plot: Movie Duration by Year
fig16 = px.box(movies.dropna(subset=['duration_mins']), x='release_year', y='duration_mins',
               title='Movie Durations by Year')
st.plotly_chart(fig16, use_container_width=True)
st.markdown("**Insight:** There's a consistent duration spread with few outliers over the years.")

# 17. Top 10 Years
top_years = filtered_df['release_year'].value_counts().nlargest(10).sort_index().reset_index()
top_years.columns = ['Year', 'Count']
fig17 = px.bar(top_years, x='Year', y='Count', title='Top 10 Years by Content Released')
st.plotly_chart(fig17, use_container_width=True)
st.markdown("**Insight:** 2018–2020 were the most active years for content release.")

# 18. Pie Chart: Top 5 Countries
top_5 = filtered_df['country'].value_counts().nlargest(5).reset_index()
top_5.columns = ['Country', 'Count']
fig18 = px.pie(top_5, names='Country', values='Count', title='Top 5 Producing Countries')
st.plotly_chart(fig18, use_container_width=True)
st.markdown("**Insight:** The USA alone contributes nearly half of the top 5 countries' total content.")

# 19. Treemap: Type > Genre
fig19 = px.treemap(filtered_df.dropna(subset=['main_genre']), path=['type', 'main_genre'], title='Treemap: Type → Genre')
st.plotly_chart(fig19, use_container_width=True)
st.markdown("**Insight:** Drama dominates across both Movies and TV Shows.")

# 20. Releases Per Month
monthly = filtered_df.dropna(subset=['month_added'])
fig20 = px.histogram(monthly, x='month_added', nbins=12, title='Content Releases by Month')
st.plotly_chart(fig20, use_container_width=True)
st.markdown("**Insight:** Most content is added between July and October, with dips in early months.")
