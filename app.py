import tkinter as tk
from tkinter import ttk
import pandas as pd


selected_movies = [] # This list is used to store the movies and the user's ratings for them


# -----------------------
# Main window
# -----------------------

window = tk.Tk() # Create a window
window.title("Movie Recommender") # Title of the window
window.geometry("800x500") # Size of the window

movie_df = pd.read_csv("movies.csv")


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

        movie_found = False

        for selected_movie in selected_movies: # If the user rates a previously rated movie again, the new rating replaces the old one;

            if selected_movie["title"] == movie:

                selected_movie["rating"] = int(rating)
                movie_found = True
        
        if not movie_found: # otherwise, the new movie and its rating are added to 'selected_movies'

            selected_movies.append({"title": movie, "rating": int(rating)})
        
        selected_listbox.delete(0, tk.END) # Clear the 'selected_listbox' to update it

        # This part of code displays the movie title and rating in the 'selected_listbox' and updates the listbox
        for selected_movie in selected_movies:

            display_text = f"{selected_movie["title"]} ({selected_movie["rating"]})"
            selected_listbox.insert(tk.END, display_text) # Add it to the list

        search_entry.delete(0, tk.END) # Clear the input field


def select_movie(event):

    selcted = search_listbox.curselection() # Get the index of the selected item

    if selcted: # If the tuple is not empty

        selcted_index = selcted[0]
        selected_title = search_listbox.get(selcted_index) # Get the item at the specified index

        search_entry.delete(0, tk.END) # Clear the input field
        search_entry.insert(0, selected_title) # Insert the selected movie title at index 0 of the entry


title_label = tk.Label(window, text="Movie Recommendation System", font=("Arial", 20), fg="navy") # Add title as a label
title_label.grid(row=0, column=0)

search_label = tk.Label(window, text="Search Movie", font=("Arial"))
search_label.grid(row=1, column=0)

search_entry = tk.Entry(window, width=40)
search_entry.grid(row=1, column=1)
search_entry.bind("<KeyRelease>", search_movie) # Call the 'search_movie' function when a key is released in the search entry

rating_label = tk.Label(window, text="Rating", font="Arial")
rating_label.grid(row=2, column=0)

# The user cannot type in this combobox and must select one of the available options
rating_combobox = ttk.Combobox(window, values=[1, 2, 3, 4, 5], width=5, state="readonly")
rating_combobox.grid(row=2, column=1)
rating_combobox.current(0) # If the user does not enter a rating for the selected movie, assign a default rating of 1

# This button adds the entered movie and rating to the selected list, then clears the input fields for the next movie and rating
add_button = tk.Button(window, text="Add Movie", command=add_movie)
add_button.grid(row=1, column=2)

# As the user types in the search entry, continuously search the movie dataset and display the search results in the listbox
search_listbox = tk.Listbox(window, width=50, height=8)
search_listbox.grid(row=3, column=1)
search_listbox.bind("<<ListboxSelect>>", select_movie)

# When the user clicks the "Add Movie" button, the entered movie and rating are added to this list
selected_listbox = tk.Listbox(window, width=50, height=8)
selected_listbox.grid(row=3, column=0)


window.mainloop() # Wait for user

