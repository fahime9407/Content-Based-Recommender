# Content-Based Movie Recommender

A simple content-based movie recommendation system built with Python.
The application allows users to rate five movies and generates personalized movie recommendations based on their preferences.

## Features

* Search for movies by title
* Select and rate up to 5 movies
* Update the rating of a previously selected movie
* Remove selected movies
* Generate personalized movie recommendations
* Display up to 8 recommended movies
* View movie details including title, year, and genres
* Simple graphical user interface built with Tkinter

## How It Works

The recommendation system uses a **content-based filtering** approach.

Movie genres are converted into one-hot encoded features. The user's ratings are then used to create a preference profile based on these genres. Movies with the highest scores based on the user's profile are recommended.

Movies that have already been rated by the user are excluded from the recommendations.

## Project Structure

```text
Content-Based-Recommender/
│
├── .gitattributes
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
├── app.py
├── movies.csv
├── recommender.py
└── ui.py
```

### Files

* **`app.py`** – Entry point of the application.
* **`ui.py`** – Contains the Tkinter graphical user interface.
* **`recommender.py`** – Handles data preprocessing and movie recommendation logic.
* **`movies.csv`** – Contains movie information such as titles, genres, and release years.
* **`requirements.txt`** – Contains the Python packages required by the project.

## Technologies

* Python
* Pandas
* Tkinter
* Git & GitHub

## Requirements

* Python 3.x
* Pandas 3.0.5

The required Python packages are listed in `requirements.txt`.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/fahime9407/Content-Based-Recommender.git
```

2. Create a virtual environment:

```bash
python -m venv myVenv
```

3. Activate the virtual environment on Windows:

```bash
myVenv\Scripts\activate
```

4. Install the required packages:

```bash
pip install -r requirements.txt
```

## Run the Application

From the project directory, run:

```bash
python app.py
```

## Usage

1. Search for a movie by typing its title.
2. Select a movie from the search results.
3. Choose a rating from 1 to 5.
4. Click **Add Movie**.
5. Repeat until five movies have been selected and rated.
6. Click **Recommend**.
7. Click a recommended movie to view its details.

## License

This project is licensed under the MIT License.

