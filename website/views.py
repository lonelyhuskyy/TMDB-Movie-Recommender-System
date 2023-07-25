from flask import Flask,Blueprint,redirect,url_for,render_template,request,send_file,flash
import pickle,json
import pandas as pd
import requests

views = Blueprint('views', __name__)

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=798816c512901b0e5dec14372fb18880&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    try:
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    except Exception as e1:
        return ""
    return full_path

@views.route('/')
def home():
    movies_df = pickle.load(open('new_df.pkl','rb'))
    movie_titles = movies_df['title'].tolist()
    return render_template("home.html",movie_titles=movie_titles,not_recommend_route = True)

@views.route('/recommend',methods=['POST'])
def recommend():
    movie = str(request.form['selectedMovie'])
    if not movie:
        flash('Movie Name is required!', category='error')
        return redirect(url_for('views.home'))
    print(movie)
    movies_df = pickle.load(open('new_df.pkl','rb'))

    movie_titles = movies_df['title'].tolist()
    similarity = pickle.load(open('similarity.pkl', 'rb'))

    movie_index = movies_df[movies_df['title'] == movie].index[0]
    distances = similarity[movie_index]
    results = sorted(list(enumerate(distances)),reverse=True,key=lambda x: x[1])[1:6]
    L = []
    poster = []
    movie_data = [(movies_df.iloc[i[0]].title, fetch_poster(movies_df.iloc[i[0]].movie_id)) for i in results]
    return render_template("recommend.html",movie=movie,movie_data= movie_data,movie_titles=movie_titles,not_recommend_route = False)