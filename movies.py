import random
import sys
from datetime import date

import matplotlib.pyplot as plt
from colorama import Fore, init

import movie_storage


init(autoreset=True)


# Console colors
INPUT_C = Fore.LIGHTGREEN_EX
ERROR_C = Fore.RED
OUTPUT_C = Fore.CYAN
SYSTEM_C = Fore.LIGHTMAGENTA_EX


# Supported keys for automatically identifying a name or title field.
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


def validate_number_input(
        user_input: str,
        expected_type: type,
        choice_range: tuple[int, int] | None = None) -> bool:
    """Validates that the input has the expected numeric type
    and is within the given range."""
    if choice_range is not None:
        lowest_number, biggest_number = choice_range
        try:
            if ((expected_type == int or expected_type == float)
                    and lowest_number <= expected_type(user_input) <= biggest_number):
                return True
            else:
                print(ERROR_C +
                      f"only use numbers between {lowest_number} and {biggest_number}")
        except ValueError:
            print(ERROR_C +
                  f"only use numbers between {lowest_number} and {biggest_number}")

    return False


def choose_from_options(options: list) -> str:
    """Displays a numbered options menu and returns the selected option."""
    check = False
    while not check:
        counter = 0
        print((OUTPUT_C +"\nChoose one option:"))
        for option in options:
            counter += 1
            print(OUTPUT_C +f"{counter}: {option}")
        print(ERROR_C + f"{counter + 1}: shut down")
        print()
        choice = input(INPUT_C +f"Enter choice (1-{counter + 1}) : ")
        check = validate_number_input(choice, int, (1, counter + 1))
        if check and int(choice) == (counter + 1):
            terminate_program()
    return options[int(choice) - 1]


def create_database() -> tuple[dict, dict]:
    """Loads the movie database and builds a title-to-ID lookup dictionary."""
    movies_db = movie_storage.get_movies()
    id_finder = create_id_finder(movies_db)
    return movies_db, id_finder


def create_id_finder(movies_db: dict) -> dict[str, int]:
    """Builds a lookup dictionary that maps movie titles to their IDs."""
    if not movies_db:
        return {}

    id_finder = {}
    id_key = find_lookup_key(movies_db)

    if id_key is None:
        print(ERROR_C + "No suitable lookup key could be found.")
        return {}

    for data_id, data in movies_db.items():
        id_finder[data[id_key]] = data_id

    return id_finder


def find_lookup_key(database: dict[int, dict]) -> str | None:
    """Returns a suitable lookup key or gets one from the user."""
    # We assume all data sets use the same keys, so checking one is enough.
    for values in database.values():
        lookup_key = find_automatic_lookup_key(values)

        if lookup_key:
            return lookup_key
        return get_lookup_key_input(values)
    return None


def find_automatic_lookup_key(values: dict) -> str | None:
    """Returns the first supported lookup key found in a data set."""
    for lookup_key in ID_KEYS:
        if lookup_key in values:
            return lookup_key
    return None


def get_lookup_key_input(values: dict) -> str:
    """Gets a valid lookup key from the user."""
    keys = []

    for key in values:
        keys.append(key)

    # This optional feature allows different lookup keys for other data sets.
    new_lookup_key = input(INPUT_C +
                           "\nplease provide the 'lookup_key' to find ids: ")

    if new_lookup_key not in keys:
        print(ERROR_C + "This key does not exist!")
        new_lookup_key = choose_from_options(keys)

    ID_KEYS.append(new_lookup_key)
    return new_lookup_key


def find_available_id(movies_db: dict) -> int:
    """Returns the lowest ID unused by active and deleted movies."""
    id_list = []
    deleted_movies = movie_storage.get_deleted_movies()

    for used_id in movies_db:
        id_list.append(used_id)
    for deleted_movie in deleted_movies:
        id_list.append(deleted_movie["id"])
    id_list.sort()

    new_id = 1
    for check_id in id_list:
        if check_id == new_id:
            new_id += 1
        elif check_id != new_id:
            break
    return new_id


def handle_empty_db():
    """Requires the user to add a movie while the active database is empty."""
    movies_db = movie_storage.get_movies()
    while len(movies_db) == 0:
        add_movie()
        movies_db = movie_storage.get_movies()


def choose_from_main_menu() -> str:
    """Prints the main menu and returns the user's menu choice."""
    check = False
    while not check:
        print(OUTPUT_C +
            "\n"
            "Menu:\n"
            " 0. Exit\n"
            " 1. List movies\n"
            " 2. Add movie\n"
            " 3. Delete movie\n"
            " 4. Update movie\n"
            " 5. Stats\n"
            " 6. Random movie\n"
            " 7. Search movie\n"
            " 8. Movies sorted by rating\n"
            " 9. Movies sorted by year of release\n"
            "10. Movies filtered\n"
            "11. Create Rating Histogram\n"
            "12. Recover Deleted Movie\n"
        )
        user_choice = input(INPUT_C + "Enter choice (0-12): ")
        check = validate_number_input(user_choice, int, (0, 12))
    return user_choice


def forwarding_main_menu(main_menu_choice: str) -> bool:
    """Forwards the user's menu choice to the matching menu function."""
    if main_menu_choice == "0":
        return terminate_program()
    if main_menu_choice == "1":
        list_movies()
    elif main_menu_choice == "2":
        add_movie()
    elif main_menu_choice == "3":
        delete_movie()
    elif main_menu_choice == "4":
        update_movie()
    elif main_menu_choice == "5":
        stats_movies()
    elif main_menu_choice == "6":
        random_movie()
    elif main_menu_choice == "7":
        search_movie()
    elif main_menu_choice == "8":
        movies_sorted_category("rating")
    elif main_menu_choice == "9":
        movies_sorted_category("year of release")
    elif main_menu_choice == "10":
        filter_movies()
    elif main_menu_choice == "11":
        rating_histogram()
    elif main_menu_choice == "12":
        restore_deleted_movies()
    return True


def terminate_program():
    """Prints the exit message and stops the main program loop."""
    print(SYSTEM_C + "************ See you soon! *************")
    sys.exit()


def list_movies():
    """Prints all movies from the movie database."""
    movies_db = movie_storage.get_movies()
    print()
    print(Fore.CYAN + f"{len(movies_db)} movies in total")

    for entry in movies_db.values():
        print_movie(entry['title'])
    returning_to_main()


def add_movie(new_title = False):
    """Adds a new movie to persistent storage."""
    movies_db, _ = create_database()
    # Requests a title unless one was provided by another menu flow.
    if not new_title:
        print()
        new_title = get_and_check_title_input("add")

    if isinstance(new_title, str):
        new_id = find_available_id(movies_db)
        new_release = get_new_release()
        new_rating = get_new_rating()

        print()
        movie_storage.add_movie((new_id, new_title, int(new_release), float(new_rating)))
        print(OUTPUT_C + f"Movie '{new_title}' successfully added as:")
        print_movie(new_title)

    returning_to_main()


def get_new_release():
    """Prompts until a valid movie release year is entered."""
    check = False
    while not check:
        new_release = input(INPUT_C + "Enter movie year: ")
        check = validate_number_input(new_release, int, (1888, get_current_year()))
    return new_release


def get_new_rating():
    """Prompts until a valid movie rating between 0 and 10 is entered."""
    check = False
    while not check:
        new_rating = input(INPUT_C + "Enter movie rating (0-10): ")
        check = validate_number_input(new_rating, float, (0, 10))
    return new_rating


def get_current_year():
    """Returns the current calendar year."""
    current_date = date.today()
    return current_date.year


def delete_movie():
    """Moves a selected movie to the trash and removes it from the active database."""
    _, id_finder = create_database()
    print()
    deletion_choice = get_and_check_title_input("delete")

    if deletion_choice:  # Python treats non-empty strings as True
        delete_id = id_finder[deletion_choice]
        handle_deleted_movies(delete_id)
        movie_storage.delete_movie(delete_id)
        print()
        print(OUTPUT_C + f"Movie '{deletion_choice}' successfully deleted")

    returning_to_main()


def handle_deleted_movies(delete_id: int):
    """Moves a movie to the trash and limits the trash to 50 entries."""
    movies_db = movie_storage.get_movies()
    deleted_movies = movie_storage.get_deleted_movies()
    movie = movies_db[delete_id]
    deleted_movies.append(
        {"id": delete_id,
         "title": movie["title"],
         "rating": movie["rating"],
         "year of release": movie["year of release"]
         }
    )
    movie_storage.save_deleted_movies(deleted_movies)
    if len(deleted_movies) > 50:
        movie_storage.delete_deleted_movie(0)


def update_movie(update_choice = False):
    """This function updates the rating of an existing film."""
    _, id_finder = create_database()
    if not update_choice:
        print()
        update_choice = get_and_check_title_input("update")

    if update_choice:
        print()
        update_id = id_finder[update_choice]
        check = False
        while not check:
            new_rating = input(INPUT_C + "Enter new movie rating (0-10): ")
            check = validate_number_input(new_rating, float, (0, 10))

        movie_storage.update_movie(update_id, float(new_rating))
        print()
        print(OUTPUT_C + f"Movie {update_choice} successfully updated to:")
        print_movie(update_choice)

    returning_to_main()


def stats_movies():
    """Calculates and prints movie statistics."""
    movies_db = movie_storage.get_movies()
    print()
    ratings = get_ratings(movies_db)
    average_rating = get_average_movies_rating(ratings)
    median_rating = get_median_movies_rating(ratings)
    # Each result contains a list of movie title(s) and the matching rating.
    best_movies = get_rating_bounds(movies_db, ratings, max)
    worst_movies = get_rating_bounds(movies_db, ratings, min)
    printing_stats(average_rating, median_rating, best_movies, worst_movies)
    returning_to_main()


def get_ratings(movies_db: dict) -> list[float]:
    """Returns all movie ratings as a list."""
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


def get_rating_bounds(movies_db: dict, ratings: list, method
                      ) -> tuple[list, float]:
    """Returns the movie titles sharing the minimum or maximum rating and the rating itself."""
    rating = method(ratings)
    movies = []
    for movie in movies_db.values():
        if movie["rating"] == rating:
            movies.append(movie["title"])
    return movies, rating


def printing_stats( average_rating: float,
                    median_rating: float,
                    best_movies: tuple[list, float],
                    worst_movies: tuple[list, float]
                    ):
    """Prints average, median, best movie, and worst movie statistics."""
    print(OUTPUT_C + f"Average rating: {average_rating:.1f}")
    print(OUTPUT_C + f"Median rating: {median_rating:.1f}")

    print_rating_bound(
        best_movies,
        "highest",
        "Best"
    )
    print_rating_bound(
        worst_movies,
        "lowest",
        "Worst"
    )


def print_rating_bound( movies_and_rating: tuple[list, float],
                        rating_description: str,
                        movie_description: str
                        ):
    """Prints one minimum or maximum movie-rating result."""
    movies, rating = movies_and_rating

    if len(movies) > 1:
        print(
            OUTPUT_C
            + f"{len(movies)} movies share the "
              f"{rating_description} rating of {rating}"
        )

        for movie in movies:
            print(OUTPUT_C + f"- {movie}")

    else:
        print(
            OUTPUT_C
            + f"{movie_description} movie: "
              f"{movies[0]}, {rating}"
        )


def random_movie():
    """Prints a random movie recommendation from the movie database."""
    movies_db = movie_storage.get_movies()

    movies = []
    for movie in movies_db.values():
        movies.append(movie)

    r_movie = random.choice(movies)
    print()
    print(OUTPUT_C + f"Your movie for tonight:")
    print_movie(r_movie['title'])
    returning_to_main()


def search_movie():
    """Searches titles by substring and falls back to fuzzy search."""
    movies_db, _ = create_database()
    print()
    search_word = input(INPUT_C + "Enter part of movie name: ").lower()
    counter = 0

    for movie in movies_db.values():
        if search_word in movie["title"].lower():
            if counter == 0:
                print()

            print_movie(movie["title"])
            counter += 1

    if counter == 0:
        fuzzy_hits = fuzzy_search(search_word, movies_db)

        if fuzzy_hits:
            print()

            for hit in fuzzy_hits:
                print_movie(hit)

    returning_to_main()


def movies_sorted_category(category: str):
    """Prints movies sorted by the selected category and direction."""
    movies_db = movie_storage.get_movies()

    option = choose_from_options(["Ascending (low to high)", "Descending (high to low)"])
    if option == "Ascending (low to high)":
        reverse_order = False
    else:
        reverse_order = True
    # In Movie Project 1, this sorting was done manually.
    # During the refactor, it was replaced with sorted() and a lambda function.
    sorted_movies = sorted(
        movies_db.values(),
        key=lambda movie: movie[category],
        reverse=reverse_order
    )
    print()
    for movie in sorted_movies:
        print_movie(movie["title"])

    returning_to_main()


def filter_movies():
    """Collects filter criteria and prints all matching movies."""
    movies_db = movie_storage.get_movies()
    filter_choices = get_filter_settings()
    filters = get_filter_input(filter_choices)
    filtered_movies = applying_filters(movies_db, filters)
    print_filtered_movies(filtered_movies, filters)
    returning_to_main()


def get_filter_settings():
    """Returns the configuration for rating and release-year filters."""
    return [
        {
            "prompt": "Enter minimum rating(leave blank for no minimum rating): ",
            "min": 0.0,
            "max": 10.0,
            "type": float
        },
        {
            "prompt": "Enter start year (leave blank for no start year): ",
            "min": 0,
            "max": get_current_year(),
            "type": int
        },
        {
            "prompt": "Enter End year (leave blank for no end year): ",
            "min": 0,
            "max": get_current_year(),
            "type": int
        }
    ]


def get_filter_input(filter_choices):
    """Collects and validates the user's movie filter values."""
    filters = []
    print()
    for filter_settings in filter_choices:
        checked = False
        while not checked:
            user_input = input(INPUT_C + filter_settings["prompt"]).strip()
            # Blank inputs disable the corresponding filter by using boundary values.
            if filter_settings == filter_choices[0] and user_input == "":
                user_input = "0.0"
            if filter_settings == filter_choices[1] and user_input == "":
                user_input = "0"
            if filter_settings == filter_choices[2] and user_input == "":
                user_input = str(get_current_year())
            checked = validate_number_input(
                                user_input,
                                filter_settings["type"],
                    (filter_settings["min"], filter_settings["max"])
                                )
            # The end year cannot be earlier than the selected start year.
            if (checked and filter_settings == filter_choices[2] and
                    filters[1] > int(user_input)):
                print(ERROR_C + f"Answer must be at least '{str(filters[1])}'.\n")
                checked = False

            if checked:
                filters.append(filter_settings["type"](user_input))
    print()

    return filters


def applying_filters(movies_db: dict, filters: list[float | int]) -> list:
    """Returns movie titles matching the selected rating and year filters."""
    min_rating, start_year, end_year = filters
    filtered_movies = []
    for movie in movies_db.values():
        if movie["rating"] >= min_rating and start_year <= movie["year of release"] <= end_year:
            filtered_movies.append(movie["title"])

    return filtered_movies


def print_filtered_movies(filtered_movies: list, filters: list[float | int]):
    """Prints filtered movies or a message when no matches are found."""
    min_rating, start_year, end_year = filters
    if len(filtered_movies) == 0:
        print(OUTPUT_C + f"no matches found for a minimum rating of '{min_rating}', "
                         f"between the years '{start_year}' and '{end_year}'. ")
    else:
        print(OUTPUT_C + "Filtered Movies:")
        for filtered_movie in filtered_movies:
            print_movie(filtered_movie)


def rating_histogram():
    """Creates, saves, and displays a histogram of all movie ratings."""
    movies_db = movie_storage.get_movies()
    print()
    movie_values = []

    for movie in movies_db.values():
        movie_values.append(movie["rating"])

    file_name = input(INPUT_C + "Enter file name or path to save the histogram: ")
    # The number of columns is tied to the number of films.
    plt.hist(movie_values, bins=max(5, min(len(movies_db) // 2 + 5, 50)))
    plt.xlabel("Rating")
    plt.ylabel("Number of movies")
    plt.title("Distribution of movie ratings")
    plt.savefig(file_name)
    plt.show()
    plt.close()
    returning_to_main()


def restore_deleted_movies():
    """Lets the user select and restore movies from the trash."""
    deleted_movies = movie_storage.get_deleted_movies()

    if not deleted_movies:
        print(ERROR_C + "No deleted movies found.")
        returning_to_main()
        return

    deleted_index_finder = create_deleted_index_finder(deleted_movies)
    choice_of_action = choose_restore_action()

    if choice_of_action == "look for a deleted movie":
        restore_choice, fuzzy_choices = (
            look_for_deleted_movie(deleted_movies)
        )

        if not restore_choice:
            returning_to_main()
            return
    # for readability no else but full string
    elif choice_of_action == "choose from all deleted movies":
        restore_choice = choose_from_all_deleted_movies(
            deleted_index_finder
        )
        fuzzy_choices = []

    # Converts the selected option into a list of movie titles to restore.
    restore_choices = handle_all_above_choice(
        restore_choice,
        fuzzy_choices
    )

    restore_indices = []
    for movie_title in restore_choices:
        restore_index = deleted_index_finder[movie_title]
        restore_indices.append(restore_index)

    restore_movies(restore_indices, deleted_movies)
    delete_restored_movies(restore_indices)

    print()
    print(OUTPUT_C + "The following movie(s) have been restored:")

    for movie_title in restore_choices:
        print_movie(movie_title)

    returning_to_main()


def choose_restore_action() -> str:
    """Displays the restore-action menu and returns the selected action."""
    return choose_from_options(
        [
            "look for a deleted movie",
            "choose from all deleted movies"
        ]
    )


def look_for_deleted_movie(deleted_movies: list[dict]
                           ) -> tuple[str | None, list]:
    """Searches the trash by title and returns the selected title and fuzzy matches."""
    # Converts the deleted-movie list to the dictionary format expected by fuzzy_search().
    transformed_deleted_movies = (transform_deleted_movies_for_fuzzy_search(deleted_movies))

    print()
    search_title = input(INPUT_C + "Enter deleted movie title to recover: "
                         ).strip().lower()

    fuzzy_choices = fuzzy_search(search_title,transformed_deleted_movies)

    if not fuzzy_choices:
        return None, []

    if len(fuzzy_choices) > 1:
        fuzzy_choices.append("_ all above _")

    restore_choice = choose_from_options(fuzzy_choices)

    return restore_choice, fuzzy_choices


def choose_from_all_deleted_movies(deleted_index_finder: dict[str, int]
                                   ) -> str:
    """Displays all deleted movie titles and returns the selected title."""
    return choose_from_options(list(deleted_index_finder))


def handle_all_above_choice(restore_choice: str,fuzzy_choices: list
                            ) -> list[str]:
    """Converts the restore selection into a list of movie titles."""
    if restore_choice == "_ all above _":
        fuzzy_choices.remove("_ all above _")
        return fuzzy_choices

    return [restore_choice]


def restore_movies(restore_indices: list[int], deleted_movies: list[dict]):
    """Adds the selected deleted movies back to the active database."""
    for restore_index in restore_indices:
        movie = deleted_movies[restore_index]

        movie_storage.add_movie(
            (
                movie["id"],
                movie["title"],
                movie["year of release"],
                movie["rating"]
            )
        )


def delete_restored_movies(restore_indices: list[int]):
    """Removes restored movies from the trash without shifting pending indices."""
    restore_indices.sort(reverse=True)
    for restore_index in restore_indices:
        movie_storage.delete_deleted_movie(restore_index)


def create_deleted_index_finder(deleted_movies: list[dict]
                                ) -> dict[str, int]:
    """Builds a mapping from deleted movie titles to their list indices."""
    deleted_index_finder = {}

    for index, movie in enumerate(deleted_movies):
        deleted_index_finder[movie["title"]] = index

    return deleted_index_finder


def transform_deleted_movies_for_fuzzy_search(deleted_movies: list[dict]
                                              ) -> dict[int, dict]:
    """Converts the deleted-movie list into a dictionary for fuzzy search."""
    transformed_deleted_movies = {}

    for index, movie in enumerate(deleted_movies):
        transformed_deleted_movies[index] = movie

    return transformed_deleted_movies


def get_and_check_title_input(method: str) -> None | str | bool:
    """Requests a movie title and forwards its handling based on whether it exists."""
    movies_db, id_finder = create_database()
    title = input(INPUT_C + f"Enter movie name to {method}: ").strip()
    title_exists = title in id_finder

    if title_exists:
        return handle_existing_title(title, method)

    return handle_missing_title(title, method, movies_db)


def handle_existing_title( title: str, method: str
                           ) -> None | str | bool:
    """Handles a movie title that already exists in the active database."""
    # if title is a match for "delete", "update", "search"
    if method in ("delete", "update", "search"):
        return title

    # if title already exists, offers to update
    if method == "add":
        print(ERROR_C + f"Movie '{title}' already exists!")
        print()
        print(INPUT_C + f"Would you like to update {title} instead?")
        update_choice = choose_from_options(["Yes", "No"])

        if update_choice == "Yes":
            update_movie(title)
        return False

    return None


def handle_missing_title( title: str, method: str, movies_db: dict
                          ) -> None | str | bool:
    """Handles a movie title that does not exist in the active database."""
    # if direct hit doesn't yield anything, tries fuzzy search instead
    # if nothing hits, offers to add new movie instead
    if method in ("delete", "update", "search"):
        print(ERROR_C + f"Movie '{title}' doesn't exist!")
        fuzzy_choice = fuzzy_search(title, movies_db)

        if fuzzy_choice:
            return choose_from_options(fuzzy_choice)

        print()
        print(INPUT_C + f"Would you like to add {title} instead?")
        update_choice = choose_from_options(["Yes", "No"])

        if update_choice == "Yes":
            add_movie(title)

        return False

    if title != "" and method == "add":
        return title

    return None


def print_movie(title: str):
    """Prints one movie in the same format throughout the program."""
    movies_db, id_finder = create_database()
    movie = movies_db[id_finder[title]]
    print(OUTPUT_C + f'{movie["title"]} ({movie["year of release"]}): {movie["rating"]}')


def returning_to_main():
    """Waits for the user before returning to the main menu."""
    print()
    input(INPUT_C + "Press enter to continue")


def fuzzy_search(search_word, movies_db: dict):
    """Returns similar movie titles using word and full-title edit-distance comparisons."""
    fuzzy_hits = []
    word_max_errors = max_deviation_error_value(search_word, "word")
    title_max_errors = max_deviation_error_value(search_word, "title")

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
            if edit_distance <= word_max_errors:
                fuzzy_hits.append(movie["title"])
                found_match = True
                break

        # If no single word matched, compare against the full title.
        # This gives better chances for longer inputs.
        if not found_match:
            edit_distance = calculate_edit_distance(search_word, compare_title)
            if edit_distance <= title_max_errors:
                fuzzy_hits.append(movie["title"])

    if len(fuzzy_hits) > 0:
        return fuzzy_hits
    else:
        print(ERROR_C + f"No movie containing '{search_word}' found.")
        return False


def max_deviation_error_value(
        search_word: str,
        comparison_type: str
) -> int:
    """Returns the allowed edit distance for a word or full-title comparison."""

    if comparison_type == "word":
        if len(search_word) <= 4:
            max_errors = 0
        elif len(search_word) <= 7:
            max_errors = 1
        elif len(search_word) <= 10:
            max_errors = 2
        else:
            max_errors = 3

        return max_errors

    # Full-title comparisons allow more errors than single-word comparisons.
    # Makes sure Star Wars Episode 'x' does not match a single input.
    if len(search_word) <= 2:
        max_errors = 0
    # Creates adaptive leniency for spelling errors.
    elif len(search_word) <= 4:
        max_errors = 1
    # Prevents inputs like 'gdfthr' from returning half the movie base.
    elif len(search_word) <= 7:
        max_errors = 2
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
        matrix[row][0] = row  # Initializes deletion costs.
    for column in range(columns):
        matrix[0][column] = column  # Initializes insertion costs.
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


def main():
    """Runs the main program loop."""
    print()
    print(Fore.LIGHTMAGENTA_EX + "********** My Movies Database **********")
    running = True

    while running:
        handle_empty_db()
        main_menu_choice = choose_from_main_menu()
        running = forwarding_main_menu(main_menu_choice)


if __name__ == "__main__":
    main()
