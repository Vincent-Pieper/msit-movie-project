import json


def get_movies() -> dict:
    """Loads database.json into movies_db and converts IDs from str back to int."""
    with open("database.json", "r") as database_r:
        raw_data = json.loads(database_r.read())
        movies_db = {}
        for movie_id, movie_data in raw_data.items():
            movies_db[int(movie_id)] = movie_data

    return movies_db


def save_movies(movies_db: dict):
    """Dumps movies_db into database.json, IDs are converted from int to str"""
    with open("database.json", "w") as database_w:
        database_w.write(json.dumps(movies_db))


def add_movie(new_movie: tuple[int, str, int, float]):
    """loads the movies_db, updates the dict
    and dumps it back into database.json"""
    new_id, new_title, new_release, new_rating = new_movie
    movies_db = get_movies()
    movies_db[new_id] = {
        "title": new_title,
        "year of release": new_release,
        "rating": new_rating
    }
    save_movies(movies_db)


def delete_movie(delete_id: int):
    """loads the movies_db, deletes the corresponding movie(id)
    and dumps it back into database.json"""
    movies_db = get_movies()
    del movies_db[delete_id]
    save_movies(movies_db)


def update_movie(update_id: int, new_rating: float):
    """loads the movies_db, updates the movie/dict
    and dumps it back into database.json"""
    movies_db = get_movies()
    movies_db[update_id]["rating"] = new_rating
    save_movies(movies_db)


def get_deleted_movies() -> list:
    """Loads deleted_movies.json into deleted_movies."""
    with open("deleted_movies.json", "r") as data_r:
        deleted_movies = json.loads(data_r.read())
    return deleted_movies


def save_deleted_movies(deleted_movies: list):
    with open("deleted_movies.json", "w") as data_w:
        data_w.write(json.dumps(deleted_movies))


def delete_deleted_movie(delete_index: int):
    """Loads deleted_movies, deletes the movie at the given index,
    and saves the updated list back to deleted_movies.json."""
    deleted_movies = get_deleted_movies()
    del deleted_movies[delete_index]
    save_deleted_movies(deleted_movies)