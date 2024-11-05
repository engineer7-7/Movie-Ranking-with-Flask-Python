# Movie Ratings and Ranking Web App

A web application built with Flask and SQLAlchemy to manage and display a list of movies with ratings. The application allows users to view movie details, edit ratings and reviews, and displays a ranking of movies based on their ratings.

## Features

- **Display Movies**: Shows a list of movies with their titles, ratings, descriptions, and rankings.
- **Edit Movie Details**: Allows users to edit the rating and review of each movie.
- **Automatic Ranking**: The movies are ranked automatically based on their ratings.
- **TMDb API Integration**: Fetch movie details from The Movie Database (TMDb) API by selecting movies from a list.

## Project Structure

- `app.py`: Main application file containing the Flask routes and database logic.
- `templates/`: Folder containing HTML templates for the web app.
  - `index.html`: Homepage displaying the list of movies with rankings.
  - `edit.html`: Page for editing movie details.
  - `select.html`: Page for selecting movies from TMDb API search results.
- `static/`: Folder containing static files like CSS for styling.
- `README.md`: This file, providing an overview of the project.

## Prerequisites

- Python 3.x
- A TMDb API Key. You can get it by signing up at [The Movie Database (TMDb)](https://www.themoviedb.org/).
