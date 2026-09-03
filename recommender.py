'''
    Anything related to the dataset and model preprocessing that does not need to be repeated
    every time the user clicks "Recommend" is written outside the function
'''

# -----------------------
# Load datasets
# -----------------------

import pandas as pd

movie_df = pd.read_csv("movies.csv") # Movie information

# -----------------------
# Data preprocessing
# -----------------------

movie_df["year"] = movie_df.title.str.extract(r"(\(\d{4}\))", expand=False) # Find '(year)' in 'title' column and store it in 'year' column
movie_df["year"] = movie_df.year.str.extract(r"(\d{4})") # remove Parenthesis from 'year' column

movie_df["title"] = movie_df.title.str.replace(r"(\(\d{4}\))", repl="", regex=True) # Remove '(year)' from 'title' column
movie_df["title"] = movie_df["title"].apply(lambda x: x.strip())

movie_df["genres"] = movie_df.genres.str.split("|") # Split the 'genres' values into a usable format


# Now, use the 'genres' column to create a one-hot encoding of the genres
movie_with_genres = movie_df.copy()

for index, row in movie_with_genres.iterrows(): # 'iterrows()' returns the index and the corresponding row as a Series in each iteration

    for genre in row["genres"]:

        movie_with_genres.at[index, genre] = 1 # Set the genre column to 1, creating it first if it does not already exist

movie_with_genres = movie_with_genres.fillna(0) # Replace NaN values with 0 for genres that a movie does not have
movie_with_genres = movie_with_genres.drop("genres", axis=1)

# -----------------------
# Recommendation function
# -----------------------

def recommend_movies(user_input):

    # Retrieve the information of the movies rated by the user from 'movie_df'
    input_id = movie_df[movie_df["title"].isin(user_input["title"].to_list())]
    # Add each movie's rating alongside its information
    user_input = pd.merge(input_id, user_input, left_on="title", right_on="title", how="inner")

    user_input = user_input.drop("genres", axis=1).drop("year", axis=1)

    # Generate one-hot-encoded genres for the movies rated by the target user to create the user profile
    user_genre_table = movie_with_genres[movie_with_genres["movieId"].isin(user_input["movieId"].to_list())]
    user_genre_table = user_genre_table.drop("movieId", axis=1).drop("title", axis=1).drop("year", axis=1)

    user_genre_table = user_genre_table.reset_index(drop=True)

    '''
    By performing matrix multiplication,
    each element of the transposed genre table is scaled by its corresponding rating,
    and summing each row yields the total score per genre.
    '''
    user_profile = user_genre_table.transpose().dot(user_input["rating"])

    # Remove movies already rated by the user to avoid recommending previously watched movies
    movie_matrix = movie_with_genres[~movie_with_genres["movieId"].isin(user_input["movieId"].to_list())]
    # Set the index as the movieId to identify each row
    movie_matrix = movie_matrix.set_index(movie_matrix["movieId"])
    # then remove unnecessary columns to create the movie matrix
    movie_matrix = movie_matrix.drop("movieId", axis=1).drop("title", axis=1).drop("year", axis=1)

    '''
    Each element of the movieMatrix is scaled by its corresponding genre score in userProfie,
    and summing each row yields the total score per film.
    '''
    recommender = ((movie_matrix * user_profile).sum(axis=1)) / user_profile.sum()
    # Sort movies by scores in descending order so that the highest-scored movies appear first
    recommender = recommender.sort_values(ascending=False)
    # Retrieve title about the 20 movies with the highest scores
    recommended_movies = movie_df[movie_df["movieId"].isin(recommender.head(20).keys())]

    return recommended_movies