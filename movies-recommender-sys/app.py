import streamlit as st
from PIL import Image  # Import Pillow for resizing
import pickle
import requests

def fetch_poster(movie_id):
    try:
        response = requests.get(
            f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'
        )
        response.raise_for_status()
        data = response.json()
        if 'poster_path' in data and data['poster_path']:
            return f"http://image.tmdb.org/t/p/w500/{data['poster_path']}"
        else:
            return "https://via.placeholder.com/500x750?text=No+Poster+Available"
    except requests.exceptions.RequestException:  # Catch any request-related error
        return "https://via.placeholder.com/500x750?text=Error"  # Return a default error image
    except Exception as e:
        return "https://via.placeholder.com/500x750?text=Error"  # Handle any other errors

def recommend(movie):
    try:
        movie_index = movies[movies['title'] == movie].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

        recommended_movies = []
        recommended_movies_posters = []
        for i in movies_list:
            movie_id = movies.iloc[i[0]].movie_id
            recommended_movies.append(movies.iloc[i[0]].title)
            recommended_movies_posters.append(fetch_poster(movie_id))
        return recommended_movies, recommended_movies_posters
    except Exception as e:
        st.error(f"Error generating recommendations: {e}")
        return [], []

# Load data
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies_list = movies['title'].values

# Streamlit app
# Load and resize the banner image
banner_image = Image.open("gread.png")
banner_image = banner_image.resize((banner_image.width, 300))  # Increased height to 300px

# Display the resized banner image
st.image(banner_image, use_container_width=True)

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Select a movie to get recommendations:',
    movies_list
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    if names and posters:
        # Create columns dynamically based on the number of movies to be displayed
        cols = st.columns(len(names))

        for i, (name, poster) in enumerate(zip(names, posters)):
            with cols[i]:
                st.text(name)
                st.image(poster, caption=name, width=150)

# Footer
st.write("---")
st.write("Project developed by: Kambhampati Ranga Sai")
