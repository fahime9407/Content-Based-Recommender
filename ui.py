import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pandas as pd
from recommender import recommend_movies, movie_df


selected_movies = [] # This list is used to store the movies and the user's ratings for them


# -----------------------
# Main window
# -----------------------

window = tk.Tk() # Create a window
window.title("Movie Recommender") # Title of the window
window.geometry("1100x600") # Size of the window


def search_movie(event):

    search_text = search_entry.get().strip() # Read the input text
    search_listbox.delete(0, tk.END) # Clear the listbox before adding the new movie results

    if search_text: # Check that the input is not empty

        results = movie_df[movie_df.title.str.contains(search_text, case=False, na=False)] # Check the movie titles and select the ones that contain the entered text

        for movie in results["title"].head(20): # Display only the first 20 movies from the search results

            search_listbox.insert(tk.END, movie)


def add_movie():

    movie = search_entry.get().strip() # Read the input text
    rating = rating_combobox.get() # Read the rating

    # This part of the code adds the movie title and rating to the 'selected_movies' list, which is used by the model
    if movie and rating: # Check that the inputs are not empty

        # If the entered movie title is invalid or not found in 'movie_df', show a warning and dont add it to 'selected_movies'
        if movie not in movie_df["title"].values:

            messagebox.showwarning(
                "Movie Not Found",
                "Please select a movie from the search results."
            )
            return

        movie_found = False # Check for duplicate movie titles
        is_selection_full = len(selected_movies) >= 5 # Limit the number of selected movies to 5

        for selected_movie in selected_movies: # If the user rates a previously rated movie again, the new rating replaces the old one.

            if selected_movie["title"] == movie:

                selected_movie["rating"] = int(rating)
                movie_found = True
                # Updating an existing rating invalidates the previous recommendations
                recommendation_listbox.delete(0, tk.END)
        
        # If the movie title is not a duplicate
        if not movie_found:

            if not is_selection_full: # If 'selected_movies' contains fewer than 5 movies

                selected_movies.append({"title": movie, "rating": int(rating)}) # add the new movie to the list
                # Adding a new movie invalidates the previous recommendations
                recommendation_listbox.delete(0, tk.END)

            else: # If 5 movies have already been selected

                messagebox.showwarning(
                    "Maximum Movies Reached",
                    "You can select a maximum of 5 movies."
                ) #Show this warning to the user
        
        selected_listbox.delete(0, tk.END) # Clear the 'selected_listbox' to update it

        # This part of code displays the movie title and rating in the 'selected_listbox' and updates the listbox
        for selected_movie in selected_movies:

            display_text = f"{selected_movie['title']} ({selected_movie['rating']})"
            selected_listbox.insert(tk.END, display_text) # Add it to the list

        search_entry.delete(0, tk.END) # Clear the input field


def select_movie(event):

    selcted = search_listbox.curselection() # Get the index of the selected item

    if selcted: # If the tuple is not empty

        selcted_index = selcted[0]
        selected_title = search_listbox.get(selcted_index) # Get the item at the specified index

        search_entry.delete(0, tk.END) # Clear the input field
        search_entry.insert(0, selected_title) # Insert the selected movie title at index 0 of the entry


def remove_movie():

    selected = selected_listbox.curselection() # Get the index of the selected item

    if selected: # If the tuple is not empty

        selected_index = selected[0]
        ''' Since 'selected_movies' and 'selected_listbox' have the same item order,
         we can use the index from 'selected_listbox' to locate the corresponding item in 'selected_movies' '''
        selected_movies.pop(selected_index)
        # Remove a movie invalidates the previous recommendations
        recommendation_listbox.delete(0, tk.END)

        selected_listbox.delete(0, tk.END)  # Clear the 'selected_listbox' to update it

        for selected_movie in selected_movies: # To rewrite 'selected_listbox' from 'selected_movies'

            display_text = f"{selected_movie["title"]} ({selected_movie["rating"]})"
            selected_listbox.insert(tk.END, display_text)


def connect_to_recommender():

    ''' If fewer than 5 movies have been selected and the user clicks the "Recommend" button,
        show this warning and exit the function '''
    if len(selected_movies) < 5:

        messagebox.showwarning(
            "Not enough movies!",
            "please select and rate 5 movies first."
        )
        return

    user_movies_df = pd.DataFrame(selected_movies) # The purpose of creating the GUI was to generate this DataFrame for training the model

    recommendations = recommend_movies(user_movies_df) # Recieve recommended movies from recommender.py

    recommendation_listbox.delete(0, tk.END) # To rewrite 'recommendation_listbox' from recommended movies

    for movie in recommendations.head(8)["title"]:

        recommendation_listbox.insert(tk.END, movie)


def show_movie_details(event):
    
    selected = recommendation_listbox.curselection()

    if selected:

        selected_index = selected[0]
        selected_title = recommendation_listbox.get(selected_index)

        info = movie_df[movie_df["title"] == selected_title].iloc[0]

        title, year, genres = info["title"], info["year"], " | ".join(info["genres"])

        messagebox.showinfo(
            "Movie details",
            f"Title: {title}\n"
            f"Year: {year}\n"
            f"Genres: {genres}"
        )


title_label = tk.Label(window, text="Movie Recommendation System", font=("Arial", 20), fg="navy") # Add title as a label
title_label.grid(row=0, column=1)

search_label = tk.Label(window, text="Search Movie", font=("Arial"))
search_label.grid(row=1, column=0)

# As the user types in the search entry, continuously search the movie dataset and display the search results in the search listbox
search_entry = tk.Entry(window, width=40)
search_entry.grid(row=1, column=1)
search_entry.bind("<KeyRelease>", search_movie) # Call the 'search_movie' function when a key is released in the search entry

rating_label = tk.Label(window, text="Rating", font="Arial")
rating_label.grid(row=2, column=0)

# The user cannot type in this combobox and must select one of the available options
rating_combobox = ttk.Combobox(window, values=[1, 2, 3, 4, 5], width=5, state="readonly")
rating_combobox.grid(row=2, column=1)
rating_combobox.current(2) # If the user does not enter a rating for the selected movie, assign a default rating of 3

# This button adds the entered movie and rating to the selected list, then clears the input fields for the next movie and rating
add_button = tk.Button(window, text="Add Movie", command=add_movie)
add_button.grid(row=1, column=2)

# This button removes the selected movie from both 'selected_listbox' and 'selected_movies' list
remove_button = tk.Button(window, text="Remove Movie", command=remove_movie)
remove_button.grid(row=5, column=1)

# When this button is clicked, the program trains the model and provides movie recommendations
recommend_button = tk.Button(window, text="Recommend", command=connect_to_recommender)
recommend_button.grid(row=5, column=2)

search_result_label = tk.Label(window, text="Search Results", font=("Arial", 12))
search_result_label.grid(row=3, column=0)

# When the user clicks a movie title in the search listbox, the full title is displayed in the search entry
search_listbox = tk.Listbox(window, width=50, height=8)
search_listbox.grid(row=4, column=0)
search_listbox.bind("<<ListboxSelect>>", select_movie)

selected_movie_label = tk.Label(window, text="Selected Movies", font=("Arial", 12))
selected_movie_label.grid(row=3, column=1)

# When the user clicks the "Add Movie" button, the entered movie and rating are added to this list
selected_listbox = tk.Listbox(window, width=50, height=8)
selected_listbox.grid(row=4, column=1)

recommendation_label = tk.Label(window, text="Recommended Movies", font=("Arial", 12))
recommendation_label.grid(row=3, column=2)

# This listbox is used to display the movies recommended by the model
recommendation_listbox = tk.Listbox(window, width=50, height=8)
recommendation_listbox.grid(row=4, column=2)
recommendation_listbox.bind("<<ListboxSelect>>", show_movie_details)

window.mainloop() # Wait for user