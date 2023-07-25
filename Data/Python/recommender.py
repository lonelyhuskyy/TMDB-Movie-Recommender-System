import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pickle
import ast
import nltk
from nltk.stem.porter import PorterStemmer
from sklearn.metrics.pairwise import cosine_similarity

movies = pd.read_csv('/Users/ragha/Desktop/Desktop/Visual Studio/ML_DS/Projects/Movie Recommender System/Data/tmdb_5000_movies.csv')
credit = pd.read_csv('/Users/ragha/Desktop/Desktop/Visual Studio/ML_DS/Projects/Movie Recommender System/Data/tmdb_5000_credits.csv')

#to merge both df
movies = movies.merge(credit,on='title')

#necessary data
movies = movies[['movie_id','title','overview','genres','keywords','cast','crew']]

"""we will create a dataframe with three columns only:
1. movie id
2. title
3. tags (includes overview,genres,keywords,cast and crew)
   To only include the word that matters from given columns, keep top 3 cast and crew and create a paragraph for each movie."""

movies.dropna(inplace=True)

#convert input string to List
def convert(obj):
    L = []
    for i in ast.literal_eval(obj):
        L.append(i['name'])
    return L

#apply convert function to movies['genres']
movies['genres'] = movies['genres'].apply(convert)

#apply convert function to movies['keywords']
movies['keywords'] = movies['keywords'].apply(convert)

#To make a list of top 3 cast and crew
def convert_cast(obj):
    L = []
    counter = 0
    for i in ast.literal_eval(obj):
        if counter != 3:
            L.append(i['name'])
            counter += 1
        else:
            break

    return L

movies['cast'] = movies['cast'].apply(convert_cast)

def convert_crew(obj):
    L = []
    for i in ast.literal_eval(obj):
        if i['job'] == 'Director':
            L.append(i['name'])
            break
    return L
    
movies['crew'] = movies['crew'].apply(convert_crew)

# split the overview para in words
movies['overview'] = movies['overview'].apply(lambda x:x.split())

# we should remove spaces between words and names of cast and crew to treat them as one entity rather than different words
func_rem = lambda x:[i.replace(" ","") for i in x]

movies['genres'] = movies['genres'].apply(func_rem)
movies['keywords'] = movies['keywords'].apply(func_rem)
movies['cast'] = movies['cast'].apply(func_rem)
movies['crew'] = movies['crew'].apply(func_rem)

# concatenate the rest of the columns into new column tags
movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']

new_df = movies[['movie_id','title','tags']]

#convert tags column into string
new_df['tags'] = new_df['tags'].apply(lambda x:" ".join(x))


# Apply stemming
ps = PorterStemmer()

def stem(text):
    y = []
    for i in text.split():
        y.append(ps.stem(i))
    return " ".join(y)

new_df['tags'] = new_df['tags'].apply(stem)

"""
Now, we have to vectorize the tags column. For this
we will use sklearn library CountVectorizer class which will
automatically calculate the most occuring words in whole tag column
and generate a vector with word count appearing for each movie
"""

# we will exclude stop words and select most occuring 5000 words
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=5000,stop_words='english')

vectors = cv.fit_transform(new_df['tags']).toarray()
words = cv.get_feature_names()

similarity = cosine_similarity(vectors)

def recommend(movie):
    movie_index = new_df[new_df['title'] == movie].index[0]
    distances = similarity[movie_index]
    results = sorted(list(enumerate(distances)),reverse=True,key=lambda x: x[1])[1:6]

    for i in results:
        print(new_df.iloc[i[0]].title)

#dump the dataframe in pickle file
with open('new_df.pickle','wb') as f:
    pickle.dump(new_df,f)