import json
from json import JSONDecodeError


def get_movies() -> dict:
    """Loads database.json and converts movie IDs from strings to integers."""
    try:
        with open("database.json", "r") as database_r:
            raw_data = json.loads(database_r.read())
            movies_db = {}

            for movie_id, movie_data in raw_data.items():
                movies_db[int(movie_id)] = movie_data

    except (FileNotFoundError, JSONDecodeError):
        movies_db = {}

    return movies_db


def save_movies(movies_db: dict):
    """Saves the movie database to database.json."""
    with open("database.json", "w") as database_w:
        database_w.write(json.dumps(movies_db, indent=4))


def add_movie(new_movie: tuple[int, str, int, float]):
    """Adds a movie and saves the updated movie database."""
    new_id, new_title, new_release, new_rating = new_movie
    movies_db = get_movies()

    movies_db[new_id] = {
        "title": new_title,
        "year of release": new_release,
        "rating": new_rating
    }

    save_movies(movies_db)


def delete_movie(delete_id: int):
    """Deletes a movie and saves the updated movie database."""
    movies_db = get_movies()
    del movies_db[delete_id]
    save_movies(movies_db)


def update_movie(update_id: int, new_rating: float):
    """Updates a movie rating and saves the updated movie database."""
    movies_db = get_movies()
    movies_db[update_id]["rating"] = new_rating
    save_movies(movies_db)


def get_deleted_movies() -> list:
    """Loads deleted movies from deleted_movies.json."""
    try:
        with open("deleted_movies.json", "r") as data_r:
            deleted_movies = json.loads(data_r.read())

    except (FileNotFoundError, JSONDecodeError):
        deleted_movies = []

    return deleted_movies


def save_deleted_movies(deleted_movies: list):
    """Saves the deleted-movie list to deleted_movies.json."""
    with open("deleted_movies.json", "w") as data_w:
        data_w.write(json.dumps(deleted_movies, indent=4))


def delete_deleted_movie(delete_index: int):
    """Deletes a movie from the trash and saves the updated list."""
    deleted_movies = get_deleted_movies()
    del deleted_movies[delete_index]
    save_deleted_movies(deleted_movies)