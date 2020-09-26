# movie_recomendation

Create a movie recommendation engine by predicting rating an user can give to a movie using 

* movies_data.csv    - The data contains 

                                         Id - which is movie id 
                                     Genres - it can contain multiple genres for a single movie.         
                                   Overview - A textual description about the movie
                                   
* ratings.csv Userid - id for user 

                                    Movieid - id for movie
                                     Rating - given by user to that movie (out of 5)
                                    
## Tasks
1. For movies containing multiple genres, select any 1 genre and assign to that movie. 
2. Build the recommendation engine using both , ‘overview’ and ‘genres’ as features i.e, model must use these 2 columns for prediction. 
3. The output will be of the form(similar to ratings.csv file) -- userid, movieid, rating(predicted).
