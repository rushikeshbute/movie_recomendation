#!/usr/bin/env python
# coding: utf-8

# In[13]:


import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# import the movie dataset
movie = pd.read_csv('movies_data.csv')
movie['index']=movie.index


movie_df = movie.head(10000)
print(movie_df)


# select the features to predict and covert to string datatype
features=["genres","overview","title"]
movie_df['genres']= movie_df['genres'].astype(str)
movie_df['overview']= movie_df['overview'].astype(str)
movie_df['title']= movie_df['title'].astype(str)

# combine features to form one sting
def combine_features(row):
    return row['genres']+" "+row['overview']+" "+row['title']

movie_df['combine_features']=movie_df.apply(combine_features,axis=1)


# In[14]:


# The CountVectorizer provides a simple way to both tokenize a collection of text documents and build a vocabulary of known words
cv= CountVectorizer()
count_matrix =cv.fit_transform(movie_df['combine_features'])
count_matrix


# In[15]:


# Compute cosine similarity between samples
cosine_sim = cosine_similarity(count_matrix)
print(cosine_sim.shape)

# covert similarity into ratings
def rating_function(num):
  if num >= 0.9:
    return 5
  if num >= 0.8 and num<0.9 :
    return 4.5
  if num >= 0.7 and num<0.8:
    return 4
  if num >= 0.6 and num<0.7:
    return 3.5
  if num >= 0.5 and num<0.6:
    return 3
  if num >= 0.4 and num<0.5:
    return 2.5
  if num >= 0.3 and num<0.4 :
    return 2
  if num >= 0.2 and num<0.3:
    return 1.5
  if num >= 0.1 and num<0.2:
    return 1
  if num >= 0.0 and num<0.1:
    return 0.5  
# making rating matrix on similarities
for i in range(cosine_sim.shape[0]):
  for j in range(cosine_sim.shape[1]):
    cosine_sim[i][j] = rating_function(cosine_sim[i][j])



# In[18]:



# converting num array into data frame
cosine_sim_df=pd.DataFrame(data=cosine_sim,columns=movie_df['index'])
cosine_sim_df.shape


# In[19]:


# import user rating dataset
rating_df = pd.read_csv('ratings.csv')

# making null dataframe
rating_predicted=pd.DataFrame(data= None ,index= cosine_sim_df.index)

# search for the rating which user can give to other movies based on above prediction matrix
for index in range(0,10000) :
  # store user_id,movie_id,movie_rating
  user_id=rating_df.loc[index,'userId']
  movie_id=rating_df.loc[index,'movieId']
  movie_rating=rating_df.loc[index,'rating']

  # finding the index value of movie_id from movies_data
  ind = movie[movie['id']==movie_id].index.values
  if len(ind)!=0 :
    if ind[0]<10000 :
      # storing best fitted ratings to variable rat
      rat= cosine_sim_df[cosine_sim_df[ind[0]]==movie_rating].median(axis=0).values
      

      # adding column to null dataset created above
      rating_predicted[user_id]= rat


# lastly added movie ids and title of the movie to respected row
rating_predicted['movieId']=movie_df['id']
rating_predicted['title']=movie_df['title']
rating_predicted.set_index('title')

# print(rating_predicted)

# storing csv file to memory
rating_predicted.to_csv('predicted_ratings.csv')


      

