import tkinter as tk

# -----------------------
# Main window
# -----------------------

window = tk.Tk() # Create a window

window.title("Movie Recommender") # Title of the window
window.geometry("700x600") # Size of the window

title_label = tk.Label(window, text="Movie Recommendation System", font=("Arial", 20, "bold"), fg="navy") # Add title as a label
title_label.pack()

search_label = tk.Label(window, text="Search Movie", font=("Arial"))
search_label.pack()

window.mainloop() # Wait for user