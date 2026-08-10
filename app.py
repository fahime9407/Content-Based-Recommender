import tkinter as tk
import pandas as pd

# -----------------------
# Main window
# -----------------------


window = tk.Tk() # Create a window

movieDf = pd.read_csv("movies.csv")

window.title("Movie Recommender") # Title of the window
window.geometry("700x600") # Size of the window

def search_movie(event):
    search_text = search_entry.get().strip() # Read the input text
    movie_listbox.delete(0, tk.END) # Clear the listbox before adding the new movie results

    if search_text: # Check that the input is not empty
        results = movieDf[movieDf.title.str.contains(search_text, case=False, na=False)] # Check the movie titles and select the ones that contain the entered text

        for movie in results["title"].head(20): # Display only the first 20 movies from the search results
            movie_listbox.insert(tk.END, movie)

def say_hello():
    movie = search_entry.get().strip() # Read the input text

    if movie: # Check that the input is not empty
        movie_listbox.insert(tk.END, movie) # Add it to the list
        search_entry.delete(0, tk.END) # Clear the input field

title_label = tk.Label(window, text="Movie Recommendation System", font=("Arial", 20), fg="navy") # Add title as a label
title_label.grid(row=0, column=0)

search_label = tk.Label(window, text="Search Movie", font=("Arial"))
search_label.grid(row=1, column=0)

search_entry = tk.Entry(window, width=40)
search_entry.grid(row=1, column=1)
search_entry.bind("<KeyRelease>", search_movie) # Call the 'search_movie' function when a key is released in the search entry

# This button adds the entered movie and rating to the list, then clears the input fields for the next movie and rating
add_button = tk.Button(window, text="Add Movie", command=say_hello)
add_button.grid(row=2, column=1)

# When the user clicks the "Add Movie" button, the entered movie and rating are added to this list
movie_listbox = tk.Listbox(window, width=50, height=8)
movie_listbox.grid(row=3, column=0)


window.mainloop() # Wait for user

