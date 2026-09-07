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
window.geometry("1100x450") # Size of the window
window.configure(bg="#f5f5f5") # Set background color of the main window


# If the window is resized, distribute the extra space equally among the three columns or shrink them equally
window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=1)
window.columnconfigure(2, weight=1)


# -----------------------
# The style
# -----------------------


style = ttk.Style() # Create a style for the widgets
style.theme_use("clam") # Use the clam theme


# Style of titles
style.configure("Title.TLabel", font=("Arial", 22, "bold"), background="#f5f5f5", foreground="#333333")
# Style of labels, Use the 'background' parameter to match the label backgrounds with the main window background
style.configure("Section.TLabel", font=("Arial", 13, "bold"), background="#f5f5f5", foreground="#444444")
# Style of buttons, use padding to set the spacing between the button text and its border
style.configure("TButton", font=("Arial", 11, "bold"), padding=(15, 8), foreground="black", background="#e0e0e0")
# When the mouse pointer is over the button, change the background color to "#d0d0d0" while keeping the text color black
style.map("TButton", background=[("active", "#d0d0d0")], foreground=[("active", "black")])



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

    selected = search_listbox.curselection() # Get the index of the selected item

    if selected: # If the tuple is not empty

        selected_index = selected[0]
        selected_title = search_listbox.get(selected_index) # Get the item at the specified index

        search_entry.delete(0, tk.END) # Clear the input field
        search_entry.insert(0, selected_title) # Insert the selected movie title at index 0 of the entry



def remove_movie():

    selected = selected_listbox.curselection() # Get the index of the selected item

    if selected: # If the tuple is not empty

        selected_index = selected[0]
        ''' Since 'selected_movies' and 'selected_listbox' have the same item order,
         we can use the index from 'selected_listbox' to locate the corresponding item in 'selected_movies' '''
        selected_movies.pop(selected_index)
        # Removing a movie invalidates the previous recommendations
        recommendation_listbox.delete(0, tk.END)

        selected_listbox.delete(0, tk.END)  # Clear the 'selected_listbox' to update it

        for selected_movie in selected_movies: # To rewrite 'selected_listbox' from 'selected_movies'

            display_text = f"{selected_movie['title']} ({selected_movie['rating']})"
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

    recommendations = recommend_movies(user_movies_df) # Receive recommended movies from recommender.py

    recommendation_listbox.delete(0, tk.END) # To rewrite 'recommendation_listbox' from recommended movies

    if recommendations.empty: # This part of the code runs when no movie recommendations are found for the user

        messagebox.showwarning(
            "No Recommendations",
            "No movie recommendations were found."
        )
        return

    for movie in recommendations["title"]:

        recommendation_listbox.insert(tk.END, movie)



def show_movie_details(event):
    
    selected = recommendation_listbox.curselection()

    if selected:

        selected_index = selected[0]
        selected_title = recommendation_listbox.get(selected_index)

        info = movie_df[movie_df["title"] == selected_title].iloc[0] # Find the movie in 'movie_df' and return the result as a Series

        title, year, genres = info["title"], info["year"], " | ".join(info["genres"])

        messagebox.showinfo(
            "Movie Details",
            f"Title: {title}\n"
            f"Year: {year}\n"
            f"Genres: {genres}"
        )




title_label = ttk.Label(window, text="Movie Recommendation System", style="Title.TLabel") # Add title as a label
title_label.grid(row=0, column=1, pady=(20, 15)) # Set 20 pixels of top padding and 15 pixels of bottom padding

search_label = ttk.Label(window, text="Search Movie", style="Section.TLabel")
search_label.grid(row=1, column=0, pady=5)

# As the user types in the search entry, continuously search the movie dataset and display the search results in the search listbox
search_entry = tk.Entry(window,
                        width=40, font=("Arial", 11),
                        bg="white", fg="black",
                        borderwidth=1, relief="solid")

search_entry.grid(row=1, column=1, pady=5)
search_entry.bind("<KeyRelease>", search_movie) # Call the 'search_movie' function when a key is released in the search entry

rating_label = ttk.Label(window, text="Rating", style="Section.TLabel")
rating_label.grid(row=2, column=0, pady=5)

# The user cannot type in this combobox and must select one of the available options
rating_combobox = ttk.Combobox(window, values=[1, 2, 3, 4, 5], width=7, state="readonly")
rating_combobox.grid(row=2, column=1, pady=5)
rating_combobox.current(2) # If the user does not enter a rating for the selected movie, assign a default rating of 3

# This button adds the entered movie and rating to the selected list, then clears the input fields for the next movie and rating
add_button = ttk.Button(window, text="Add Movie", style="TButton", command=add_movie)
add_button.grid(row=1, column=2, padx=8, pady=5)

# This button removes the selected movie from both 'selected_listbox' and 'selected_movies' list
remove_button = ttk.Button(window, text="Remove Movie", style="TButton", command=remove_movie)
remove_button.grid(row=5, column=1, padx=8, pady=8)

# When this button is clicked, the program generates movie recommendations
recommend_button = ttk.Button(window, text="Recommend", style="TButton", command=connect_to_recommender)
recommend_button.grid(row=5, column=2, padx=8, pady=8)

search_result_label = ttk.Label(window, text="Search Results", style="Section.TLabel")
search_result_label.grid(row=3, column=0, pady=8, sticky="n") # The 'sticky' parameter specifies where the widget is positioned within its cell: north, south, west, or east

# When the user clicks a movie title in the search listbox, the full title is displayed in the search entry
search_listbox = tk.Listbox(window,
                            width=35, height=8, font=("Arial", 11),
                            borderwidth=1, relief="solid", # The 'relief' parameter specifies the type of border
                            bg="white", fg="black", # The 'bg' parameter specifies the background color, and 'fg' specifies the text color
                            selectbackground="lightblue", selectforeground="black") # The 'selectbackground' parameter specifies the background color of the selected item, and 'selectforeground' specifies its text color

search_listbox.grid(row=4, column=0, padx=10, pady=5)
search_listbox.bind("<<ListboxSelect>>", select_movie)

selected_movie_label = ttk.Label(window, text="Selected Movies", style="Section.TLabel")
selected_movie_label.grid(row=3, column=1, pady=8, sticky="n")

# When the user clicks the "Add Movie" button, the entered movie and rating are added to this list
selected_listbox = tk.Listbox(window, width=35, height=8, font=("Arial", 11),
                              borderwidth=1, relief="solid",
                              bg="white", fg="black",
                              selectbackground="lightblue", selectforeground="black")

selected_listbox.grid(row=4, column=1, padx=10, pady=5)

recommendation_label = ttk.Label(window, text="Recommended Movies", style="Section.TLabel")
recommendation_label.grid(row=3, column=2, pady=8, sticky="n")

# This listbox is used to display the movies recommended by the model
recommendation_listbox = tk.Listbox(window, width=35, height=8, font=("Arial", 11),
                                    borderwidth=1, relief="solid",
                                    bg="white", fg="black",
                                    selectbackground="lightblue", selectforeground="black")

recommendation_listbox.grid(row=4, column=2, padx=10, pady=5)
recommendation_listbox.bind("<<ListboxSelect>>", show_movie_details) # When the user clicks a recommended movie, its information is displayed

window.mainloop() # Wait for user