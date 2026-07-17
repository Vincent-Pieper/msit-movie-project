import random
import matplotlib.pyplot as plt
from colorama import Fore, init
init(autoreset=True)


# Will be pushed to another folder/file later - this is a placeholder.
ID_KEYS = [
    "name",
    "label",
    "display_name",
    "username",
    "full_name",
    "company_name",
    "product_name",
    "project_name",
    "title",
    "filename",
]


DELETED_MOVIES = [
    {"id": 11, "title": "test-film1", "rating": 7.3, "year of release": 1994},
    # {"id": 12, "title": "test-film2", "rating": 7.3, "year of release": 1994},
    {"id": 13, "title": "test-film3", "rating": 7.3, "year of release": 1994},
]


def create_database() -> tuple[dict, dict]:
    """
    creates a base dictionary AND an additional id_finder.
    Both dictionaries are accessible in a tuple database (movies_db, id_finder)
    """
    movies_db = {
        1: {"title": "The Shawshank Redemption", "rating": 9.5, "year of release": 1994},
        2: {"title": "Pulp Fiction", "rating": 8.8, "year of release": 1994},
        3: {"title": "The Room", "rating": 3.6, "year of release": 2003},
        4: {"title": "The Godfather", "rating": 9.2, "year of release": 1972},
        5: {"title": "The Godfather: Part II", "rating": 9.0, "year of release": 1974},
        6: {"title": "The Dark Knight", "rating": 9.0, "year of release": 2008},
        7: {"title": "12 Angry Men", "rating": 8.9, "year of release": 1957},
        8: {"title": "Everything Everywhere All At Once", "rating": 8.9, "year of release": 2022},
        9: {"title": "Forrest Gump", "rating": 8.8, "year of release": 1994},
        10: {"title": "Star Wars: Episode V", "rating": 8.7, "year of release": 1980}
    }

    id_finder = create_id_finder(movies_db)
    return movies_db, id_finder


def create_id_finder(database: dict[int, dict[str, object]]) -> dict[str, int]:
    """
    a function that automatically creates a corresponding
    secondary id_finder to provide title-based access to the db
    """
    id_finder = {}
    id_key = find_lookup_key(database)
    for data_id, data in database.items():
        id_finder[data[id_key]] = data_id
    return id_finder


def find_lookup_key(database: dict[int, dict]) -> str:
    """
    this function looks for an id-suitable key in the master-dictionary,
    if it cannot find one, it will prompt the user to provide one.
    """
    # we assume all data sets use the same keys, so checking one is enough
    for values in database.values():
        for lookup_key in ID_KEYS:
            if lookup_key in values:
                return lookup_key

        # This is an optional feature to create different id_finders for different tasks.
        # It can be adjusted to use different lookup keys.
        while True:
            new_lookup_key = input(Fore.LIGHTGREEN_EX +
                                   "\nplease provide the 'lookup_key' to find ids: ")
            if new_lookup_key in values:
                ID_KEYS.append(new_lookup_key)
                print()
                return new_lookup_key
            print(Fore.RED + "your input does not exist in your dictionary. try again !")
    raise ValueError("No valid lookup key found.")


def choose_from_main_menu() -> str:
    """Prints the main menu and returns the user's menu choice."""
    print(Fore.GREEN +
        "Menu:\n"
        "0. Exit\n"
        "1. List movies\n"
        "2. Add movie\n"
        "3. Delete movie\n"
        "4. Update movie\n"
        "5. Stats\n"
        "6. Random movie\n"
        "7. Search movie\n"
        "8. Movies sorted by rating\n"
        "9. Create Rating Histogram\n"
    )
    return input(Fore.LIGHTGREEN_EX + "Enter choice (0-9): ")


def forwarding_main_menu(main_menu_choice: str, database: tuple[dict, dict]) -> bool:
    """Forwards the user's menu choice to the matching menu function."""
    if main_menu_choice == "0":
        return terminate_program()
    if main_menu_choice == "1":
        list_movies(database)
    elif main_menu_choice == "2":
        add_movie(database)
    elif main_menu_choice == "3":
        delete_movie(database)
    elif main_menu_choice == "4":
        update_movie(database)
    elif main_menu_choice == "5":
        stats_movies(database)
    elif main_menu_choice == "6":
        random_movie(database)
    elif main_menu_choice == "7":
        search_movie(database)
    elif main_menu_choice == "8":
        movies_sorted_ratings(database)
    elif main_menu_choice == "9":
        rating_histogram(database)
    else:
        print(Fore.RED +
            "\n"
            "Please make sure your answer matches the numbers displayed in the main menu\n"
            "...Returning to main menu..."
            "\n"
        )
    return True


def terminate_program():
    """Prints the exit message and stops the main program loop."""
    print(Fore.LIGHTMAGENTA_EX + "************ See you soon! *************")
    return False


def list_movies(database: tuple[dict, dict]):
    """Prints all movies from the movie database."""
    movies_db, _ = database
    print()
    print(Fore.CYAN + f"{len(movies_db)} movies in total")

    for entry in movies_db.values():
        print(Fore.CYAN + f"{entry['title']}: ({entry['year of release']}): {entry['rating']}")
    returning_to_main()


def add_movie(database: tuple[dict, dict]):
    """Adds a movie and updates movie_db and id_finder"""
    movies_db, id_finder = database
    print()
    new_title = get_and_check_title_input(database, "add")

    if new_title:
        new_id = find_available_id(database)
        new_year = int(input(Fore.LIGHTGREEN_EX + "Enter movie year: "))
        new_rating = float(input(Fore.LIGHTGREEN_EX + "Enter movie rating (0-10): "))

        movies_db[new_id] = {
            "title": new_title,
            "rating": new_rating,
            "year of release": new_year
        }

        id_finder[new_title] = new_id
        print(Fore.CYAN + f"Movie '{new_title}' successfully added")

    returning_to_main()


def find_available_id(database: tuple[dict, dict]) -> int:
    """
    Searches for the lowest available id, that is not in use by either database and trash.
    """
    movies_db, _ = database
    id_list = []

    for used_id in movies_db:
        id_list.append(used_id)
    for deleted_movie in DELETED_MOVIES:
        id_list.append(deleted_movie["id"])
    id_list.sort()

    new_id = 1
    for check_id in id_list:
        if check_id == new_id:
            new_id += 1
        elif check_id != new_id:
            break
    return new_id


def delete_movie(database: tuple[dict, dict]):
    """
    This function accesses the database through the id_finder, and deletes it from database
    """
    movies_db, id_finder = database
    print()
    deletion_choice = get_and_check_title_input(database, "delete")

    if deletion_choice:  # Python treats non-empty strings as True
        delete_id = id_finder[deletion_choice]
        handle_deleted_movies(database, delete_id)
        del id_finder[deletion_choice]
        del movies_db[delete_id]
        print(Fore.CYAN + f"Movie '{deletion_choice}' successfully deleted")

    returning_to_main()


def get_and_check_title_input(database: tuple[dict, dict], method: str) -> None | str | bool:
    """
    This function checks the title against id_finder.
    Returns the 'title' if the input is valid.
    Returns False if the input is invalid.
    """
    _, id_finder = database
    title = input(Fore.LIGHTGREEN_EX + f"Enter movie name to {method}: ")
    title_exists = title in id_finder

    if title_exists and method in ("delete", "update"):
        return title
    if title_exists and (method == "add"):
        print(Fore.RED + f"Movie '{title}' already exists!")
        return False
    if not title_exists and method in ("delete", "update"):
        print(Fore.RED + f"Movie '{title}' doesn't exist!")
        return False
    if not title_exists and (method == "add"):
        return title
    return None


def handle_deleted_movies(database: tuple[dict, dict], delete_id: int):
    """
    This function moves the deleted data set into the trash.
    The trash keeps no more than 50 Items.
    IDs from deleted data cannot be reused as long as the Item remains in the trash.
    """
    movies_db, _ = database
    movie = movies_db[delete_id]
    DELETED_MOVIES.append(
        {"id": delete_id,
         "title": movie["title"],
         "rating": movie["rating"],
         "year of release": movie["year of release"]
         }
    )
    if len(DELETED_MOVIES) > 50:
        del DELETED_MOVIES[0]


def update_movie(database: tuple[dict, dict]):
    """This function updates the rating of an existing film."""
    movies_db, id_finder = database
    print()
    update_choice = get_and_check_title_input(database, "update")

    if update_choice:
        update_id = id_finder[update_choice]
        new_rating = float(input(Fore.LIGHTGREEN_EX + "Enter new movie rating (0-10): "))
        movies_db[update_id]["rating"] = new_rating
        print(Fore.CYAN + f"Movie {update_choice} successfully updated")

    returning_to_main()


def stats_movies(database: tuple[dict, dict]):
    """Calculates and prints movie statistics."""
    print()
    ratings = get_ratings(database)
    average_rating = get_average_movies_rating(ratings)
    median_rating = get_median_movies_rating(ratings)
    # Each result contains a list of movie title(s) and the matching rating.
    best_movies = get_rating_bounds(database, ratings, max)
    worst_movies = get_rating_bounds(database, ratings, min)
    printing_stats(average_rating, median_rating, best_movies, worst_movies)
    returning_to_main()


def get_ratings(database: tuple[dict, dict]) -> list[float]:
    """Returns all movie ratings as a list."""
    movies_db, _ = database
    ratings = []
    for movie in movies_db.values():
        ratings.append(movie["rating"])
    return ratings


def get_average_movies_rating(ratings: list) -> float:
    """Calculates the average movie rating."""
    return sum(ratings) / len(ratings)


# Could also be done with: from statistics import median
def get_median_movies_rating(ratings: list) -> float:
    """Calculates the median movie rating."""
    # Copying is a good habit here because sorted() does not change the original list.
    sorted_ratings = sorted(ratings)
    len_ratings = len(sorted_ratings)
    if len_ratings % 2 == 0:
        return (sorted_ratings[(len_ratings//2)] + sorted_ratings[(len_ratings//2)-1])/2
    return sorted_ratings[len_ratings//2]


def get_rating_bounds(database: tuple[dict, dict], ratings: list, method) -> tuple[list, float]:
    """
    Creates a universal function to get the max or min rating from ratings.
    The parameter method receives a function such as max or min.
    """
    movies_db, _ = database
    rating = method(ratings)
    movies = []
    for movie in movies_db.values():
        if movie["rating"] == rating:
            movies.append(movie["title"])
    return movies, rating


def printing_stats(average_rating: float,
                   median_rating: float,
                   best_movies: tuple[list, float],
                   worst_movies: tuple[list, float]):
    """Prints average, median, best movie, and worst movie statistics."""
    print(Fore.CYAN + f"Average rating: {average_rating:.2f}")
    print(Fore.CYAN + f"Median rating: {median_rating:.2f}")

    best_movies_list, best_rating = best_movies
    if len(best_movies_list) > 1:
        print(Fore.CYAN +
              f"{len(best_movies_list)} movies share the highest rating of {best_rating}")
        for movie in best_movies_list:
            print(Fore.CYAN + f"- {movie}")
    else:
        print(Fore.CYAN + f"Best movie: {best_movies_list[0]}, {best_rating}")

    worst_movies_list, worst_rating = worst_movies
    if len(worst_movies_list) > 1:
        print(Fore.CYAN +
              f"{len(worst_movies_list)} movies share the lowest rating of {worst_rating}")
        for movie in worst_movies_list:
            print(Fore.CYAN + f"- {movie}")
    else:
        print(Fore.CYAN + f"Worst movie: {worst_movies_list[0]}, {worst_rating}")


def random_movie(database: tuple[dict, dict]):
    """Prints a random movie recommendation from the movie database."""
    movies_db, _ = database

    movies = []
    for movie in movies_db.values():
        movies.append(movie)

    r_movie = random.choice(movies)
    print()
    print(Fore.CYAN + f"Your movie for tonight: {r_movie['title']}, it's rated {r_movie['rating']}")
    returning_to_main()


def search_movie(database: tuple[dict, dict]):
    """Searches for movies containing the user's search input."""
    movies_db, _ = database
    print()
    search_word = input(Fore.LIGHTGREEN_EX + "Enter part of movie name: ").lower()
    counter = 0

    for movie in movies_db.values():
        if search_word in movie["title"].lower():
            print(Fore.CYAN + f'{movie["title"]}: {movie["rating"]}')
            counter += 1

    if counter == 0:
        print()
        fuzzy_search(search_word, database)

    returning_to_main()


def fuzzy_search(search_word, database: tuple[dict, dict]):
    """Searches for similar movie titles using edit distance."""
    movies_db, _ = database
    fuzzy_hits = []
    max_errors = max_deviation_error_value(search_word)

    for movie in movies_db.values():
        # Checks every film in the movies_db and prepares title variants for comparison.
        compare_word_normal = movie["title"]
        compare_words = compare_word_normal.lower().split()
        compare_title = compare_word_normal.lower()
        found_match = False

        # Compares single title words first.
        # This gives better chances for short inputs / single words.
        for word in compare_words:
            edit_distance = calculate_edit_distance(search_word, word)
            if edit_distance <= max_errors:
                fuzzy_hits.append(movie)
                found_match = True
                break

        # If no single word matched, compare against the full title.
        # This gives better chances for longer inputs.
        if not found_match:
            edit_distance = calculate_edit_distance(search_word, compare_title)
            if edit_distance <= max_errors:
                fuzzy_hits.append(movie)

    if len(fuzzy_hits) > 0:
        print(Fore.YELLOW + f"The movie '{search_word}' does not exist. Did you mean:")
        for hit in fuzzy_hits:
            print(Fore.YELLOW + f'{hit["title"]}: {hit["rating"]}')
    else:
        print(Fore.RED + f"No movie containing '{search_word}' found.")


def max_deviation_error_value(search_word: str) -> int:
    """Returns the allowed edit distance based on the search word length."""
    # Makes sure Star Wars Episode 'x' does not match a single input.
    if len(search_word) <= 2:
        max_errors = 0
    # Creates adaptive leniency for spelling errors.
    elif len(search_word) <= 4:
        max_errors = 1
    # Prevents inputs like 'gdfthr' from returning half the movie base.
    elif len(search_word) <= 7:
        max_errors = 3
    # Makes inputs like "gudfatha" or "drk knight" work.
    elif len(search_word) <= 10:
        max_errors = 4
    # Allows longer typo-tolerant searches against full movie titles.
    elif len(search_word) <= 15:
        max_errors = 5
    else:
        max_errors = 6
    return max_errors


def calculate_edit_distance(search_word: str, compare_entity: str) -> int:
    """Calculates the edit distance between two strings."""
    matrix_basic, rows, columns = build_empty_fuzzy_matrix(search_word, compare_entity)
    matrix_universal_rows = fill_first_row_column_fuzzy_matrix(matrix_basic, rows, columns)
    edit_distance = fill_fuzzy_matrix(matrix_universal_rows,
                                      rows, columns, search_word, compare_entity)
    return edit_distance


def build_empty_fuzzy_matrix(search_word: str, compare_word: str) -> tuple[list, int, int]:
    """Builds an empty matrix for the edit distance calculation."""
    matrix = []
    rows = len(search_word) + 1
    columns = len(compare_word) + 1

    for _ in range(rows):
        # Every row creates an empty list.
        new_row = []

        for _ in range(columns):
            # Every column gets a default value of 0.
            new_row.append(0)

        # The new row is added to the matrix.
        # Each inner list represents one matrix row.
        matrix.append(new_row)

    return matrix, rows, columns


def fill_first_row_column_fuzzy_matrix(matrix: list, rows: int, columns: int) -> list:
    """Fills the first row and first column of the fuzzy matrix."""
    for row in range(rows):
        matrix[row][0] = row  # only needs to count up the row
    for column in range(columns):
        matrix[0][column] = column
    return matrix


def fill_fuzzy_matrix(matrix: list,
                      rows: int,
                      columns: int,
                      search_word: str,
                      compare_word: str) -> int:
    """Fills the fuzzy matrix and returns the final edit distance."""
    for row in range(1, rows):
        for column in range(1, columns):

            # If the characters are the same,
            # take the diagonal value.
            if search_word[row - 1] == compare_word[column - 1]:
                diag = matrix[row - 1][column - 1]

            # If the characters are different,
            # take the diagonal value + 1.
            else:
                diag = matrix[row - 1][column - 1] + 1

            left = matrix[row][column - 1] + 1  # takes the value to the left and adds +1
            top = matrix[row - 1][column] + 1  # takes the value to the top and adds +1
            matrix[row][column] = min(diag, left, top)  # uses the smallest value to fill the cell

    return matrix[-1][-1]


def movies_sorted_ratings(database: tuple[dict, dict]):
    """Prints all movies sorted by rating from highest to lowest."""
    movies_db, _ = database
    print()

    # In Movie Project 1, this sorting was done manually.
    # During the refactor, it was replaced with sorted() and a lambda function.
    sorted_movies = sorted(
        movies_db.values(),
        key=lambda movie: movie["rating"],
        reverse=True
    )

    for movie in sorted_movies:
        print(Fore.CYAN + f'{movie["title"]}: {movie["rating"]}')

    returning_to_main()


def rating_histogram(database: tuple[dict, dict]):
    """Creates and saves a histogram of all movie ratings."""
    movies_db, _ = database
    print()
    movie_values = []

    for movie in movies_db.values():
        movie_values.append(movie["rating"])

    file_name = input(Fore.LIGHTGREEN_EX + "Enter file name or path to save the histogram: ")
    # The number of columns is tied to the number of films.
    plt.hist(movie_values, bins=max(5, min(len(movies_db) // 2 + 5, 50)))
    plt.xlabel("Rating")
    plt.ylabel("Number of movies")
    plt.title("Distribution of movie ratings")
    plt.savefig(file_name)
    plt.show()
    plt.close()
    returning_to_main()


def returning_to_main():
    """Waits for the user before returning to the main menu."""
    print()
    input(Fore.LIGHTGREEN_EX + "Press enter to continue")
    print()


def main():
    """Runs the main program loop."""
    print(Fore.LIGHTMAGENTA_EX + "********** My Movies Database **********")
    database = create_database()
    running = True

    while running:
        main_menu_choice = choose_from_main_menu()
        running = forwarding_main_menu(main_menu_choice, database)


if __name__ == "__main__":
    main()
