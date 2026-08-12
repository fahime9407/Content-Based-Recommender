import tkinter as tk
import pandas as pd

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

    if movie: # Check that the input is not empty
        selected_listbox.insert(tk.END, movie) # Add it to the list
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

