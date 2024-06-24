import streamlit as st
import pandas as pd
import pickle
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry



def fetch_poster(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=770e15dd197156c37843f6929842ae65&language=en-US'
    
    # Retry mechanism
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retries)
    session = requests.Session()
    session.mount('https://', adapter)
    
    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return None  # Handle case where poster_path is missing
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching poster for movie {movie_id}: {e}")
        return None

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)) , reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters =[]
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_posters
    

movies_dict = pickle.load(open('movie_dict.pkl' , 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl' , 'rb'))


st.title('Movie Recommendation System')

Selected_movie_name = st.selectbox('Enter a movie name ', movies['title'].values)

if st.button('Recommend'):
    names,posters = recommend(Selected_movie_name)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])
    

    

  


