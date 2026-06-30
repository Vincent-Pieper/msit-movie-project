import random
import matplotlib.pyplot as plt
from colorama import Fore, init
init(autoreset=True)


def create_database():
    movies = {
        "The Shawshank Redemption": 9.5,
        "Pulp Fiction": 8.8,
        "The Room": 3.6,
        "The Godfather": 9.2,
        "The Godfather: Part II": 9.0,
        "The Dark Knight": 9.0,
        "12 Angry Men": 8.9,
        "Everything Everywhere All At Once": 8.9,
        "Forrest Gump": 8.8,
        "Star Wars: Episode V": 8.7
    }
    return movies


def choose_from_main_menu():
    print(Fore.GREEN +
        "Menu:\n"
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
    return input(Fore.LIGHTGREEN_EX + "Enter choice (1-9): ")


def forwarding_main_menu(main_menu_choice, movies):
    if main_menu_choice == "1":
        list_movies(movies)
    elif main_menu_choice == "2":
        add_movie(movies)
    elif main_menu_choice == "3":
        delete_movie(movies)
    elif main_menu_choice == "4":
        update_movie(movies)
    elif main_menu_choice == "5":
        stats_movies(movies)
    elif main_menu_choice == "6":
        random_movie(movies)
    elif main_menu_choice == "7":
        search_movie(movies)
    elif main_menu_choice == "8":
        movies_sorted_ratings(movies)
    elif main_menu_choice == "9":
        rating_histogram(movies)
    else:
        print(Fore.RED +
            "\n"
            "Please make sure your answer matches the numbers displayed in the main menu\n"
            "...Returning to main menu..."
            "\n"
        )


def list_movies(movies):
    print()
    print(Fore.CYAN + f"{len(movies)} movies in total")
    for movie, rating in movies.items():
        print(Fore.CYAN + f"{movie}: {rating}")
    returning_to_main()


def add_movie(movies):
    print()
    new_movie_title = input(Fore.LIGHTGREEN_EX + "Enter new movie name: ")
    new_movie_rating = float(input(Fore.LIGHTGREEN_EX + "Enter new movie rating (0-10): "))
    movies[new_movie_title] = new_movie_rating
    print(Fore.CYAN + f"Movie {new_movie_title} successfully added")
    returning_to_main()


def delete_movie(movies):
    print()
    deletion_choice = input(Fore.LIGHTGREEN_EX + "Enter movie name to delete: ")
    if deletion_choice in movies:
        del movies[deletion_choice]
        print(Fore.CYAN + f"Movie {deletion_choice} successfully deleted")
    else:
        print(Fore.RED + f"Movie {deletion_choice} doesn't exist!")
    returning_to_main()


def update_movie(movies):
    print()
    update_choice = input(Fore.LIGHTGREEN_EX + "Enter movie name to update: ")
    if update_choice in movies:
        update_movie_rating =  float(input(Fore.LIGHTGREEN_EX + "Enter new movie rating (0-10): "))
        movies[update_choice] = update_movie_rating
        print(Fore.CYAN + f"Movie {update_choice} successfully updated")
    else:
        print(Fore.RED + f"Movie {update_choice} doesn't exist!")
    returning_to_main()


def stats_movies(movies):
    print()
    average_rating = average_movies_rating(movies)
    median_rating = median_movies_rating(movies)
    best_movies = best_movie_rating(movies) #  return list with tuple(s) (movie, rating)
    worst_movies = worst_movie_rating(movies) #  return list with tuple(s) (movie, rating)
    printing_stats(average_rating, median_rating, best_movies, worst_movies)
    returning_to_main()


def average_movies_rating(movies):
    return sum(movies.values()) / len(movies)


def median_movies_rating(movies): #  from statistics import median
    ratings_list_sorted = sorted(list(movies.values()))
    len_ratings_list = len(ratings_list_sorted)
    if len_ratings_list % 2 == 0:
        return (ratings_list_sorted[(len_ratings_list//2)] + ratings_list_sorted[(len_ratings_list//2)-1])/2
    else:
        return ratings_list_sorted[len_ratings_list//2]


def best_movie_rating(movies):
    best_rating = -1
    best_movies = []
    for movie in movies.items():
        if movie[1] > best_rating:
            best_rating = movie[1]
            best_movies = [movie]
        elif movie[1] == best_rating:
            best_movies.append(movie)
    return best_movies #  list with tuple(s) (movie, rating)


def worst_movie_rating(movies):
    worst_rating = 11
    worst_movies = []
    for movie in movies.items():
        if movie[1] < worst_rating:
            worst_rating = movie[1]
            worst_movies = [movie]
        elif movie[1] == worst_rating:
            worst_movies.append(movie)
    return worst_movies #  list with tuple(s) (movie, rating)


def printing_stats(average_rating, median_rating, best_movies, worst_movies):
    print(Fore.CYAN + f"Average rating: {average_rating:.2f}")
    print(Fore.CYAN + f"Median rating: {median_rating:.2f}")
    if len(best_movies) > 1:
        print(Fore.CYAN + f"{len(best_movies)} Movies share the category best movie with a rating of {best_movies[0][1]}")
        for movie in best_movies:
            print(Fore.CYAN + f"- {movie[0]}")
    else:
        print(Fore.CYAN + f"Best movie: {best_movies[0][0]}, {best_movies[0][1]}")
    if len(worst_movies) > 1:
        print(Fore.CYAN + f"{len(worst_movies)} Movies share the category worst movie with a rating of {worst_movies[0][1]}")
        for movie in worst_movies:
            print(Fore.CYAN + f"- {movie[0]}")
    else:
        print(Fore.CYAN + f"Worst movie: {worst_movies[0][0]}, {worst_movies[0][1]}")


def random_movie(movies):
    print()
    r_movie, r_rating = random.choice(list(movies.items()))
    print(Fore.CYAN + f"Your movie for tonight: {r_movie}, it's rated {r_rating}")
    returning_to_main()


def search_movie(movies):
    print()
    search_word = input(Fore.LIGHTGREEN_EX + "Enter part of movie name: ").lower()
    counter = 0
    for movie, rating in movies.items():
        if search_word in movie.lower():
            print(Fore.CYAN + f"{movie}: {rating}")
            counter += 1
    if counter == 0:
        print()
        fuzzy_search(search_word, movies)
    returning_to_main()


def fuzzy_search(search_word,movies ):
    fuzzy_hits = []
    max_errors = max_deviation_error_value(search_word)
    for compare_word_normal in movies: # checks every film in the database movies
        compare_words = compare_word_normal.lower().split() # splits into single words for comparing shorter entries
        compare_title = compare_word_normal.lower()
        found_match = False
        for word in compare_words: #  splits the compare_word/title into words and compares against them, better chance for short inputs / single words
            #  print(word)
            edit_distance = calculate_edit_distance(search_word, word)
            if edit_distance <= max_errors:
                fuzzy_hits.append(compare_word_normal)
                found_match = True
                break
        if found_match == False:
            edit_distance = calculate_edit_distance(search_word, compare_title) #  compares against the full title, better chance for longer inputs
            if edit_distance <= max_errors:
                fuzzy_hits.append(compare_word_normal)
    if len(fuzzy_hits) > 0:
        print(Fore.YELLOW + f"The movie '{search_word}' does not exist. Did you mean:")
        for hit in fuzzy_hits:
            print(Fore.YELLOW + f"{hit}: {movies[hit]}")
    else:
        print(Fore.RED + f"No movie containing '{search_word}' found.")


def max_deviation_error_value(search_word):
    if len(search_word) <= 2: # makes sure Star Wars Episode 'x' doesn't match a single input
        max_errors = 0
    elif len(search_word) <= 4:  # creates adaptive leniency for spelling errors.
        max_errors = 1
    elif len(search_word) <= 7: # 'gdfthr' now doesn't return half the movie base
        max_errors = 3
    elif len(search_word) <= 10: # "gudfatha" "drk knight" works
        max_errors = 4
    elif len(search_word) <= 15: # 'pulp fiktion' doesnt hit anything...implementing against the whole title again...
        max_errors = 5
    else:
        max_errors = 6
    return max_errors

def calculate_edit_distance(search_word, compare_entity):
    matrix_basic, rows, columns = build_empty_fuzzy_matrix(search_word, compare_entity)
    matrix_universal_rows = fill_first_row_column_fuzzy_matrix(matrix_basic, rows, columns)
    edit_distance = fill_fuzzy_matrix(matrix_universal_rows, rows, columns, search_word, compare_entity)
    return edit_distance


def build_empty_fuzzy_matrix(search_word = "test", compare_word = "tast"):
    matrix = []
    rows = len(search_word) + 1
    columns = len(compare_word) + 1
    for row in range(rows):
        new_row = [] # every row (len(search_word) + 1) creates an empty list
        for column in range(columns):
            new_row.append(0) # for every column (len(compare_word) + 1) in the matrix it gets a default value of 0
        matrix.append(new_row) #  the new row get added to the matrix as an additional list (each list is a row with as many default values as there are columns) - empty body is build
    return matrix, rows, columns


def fill_first_row_column_fuzzy_matrix(matrix, rows, columns):
    for row in range(rows):
        matrix[row][0] = row #  only needs to count up the row
    for column in range(columns):
        matrix[0][column] = column
    return matrix


def fill_fuzzy_matrix(matrix, rows, columns, search_word, compare_word):
    for row in range(1, rows):
        for column in range(1, columns):
            if search_word[row -1] == compare_word[column -1]: #  if the same index of both words is the same take the diagonal value as diag / -1 for the first empty column/row
                diag = matrix[row - 1][column - 1]
            elif search_word[row -1] != compare_word[column -1]: #  if the same index of both words is NOT the same take the diagonal value +1 as diag / -1 for the first empty column/row
                diag = matrix[row - 1][column - 1] +1
            left = matrix[row][column -1] +1 #  takes the value to the left and adds +1
            top = matrix[row -1][column] +1 #  takes the value to the top and adds +1
            matrix[row][column] = min(diag, left, top) # uses the smallest value to fill the cell
    return matrix[-1][-1]


def movies_sorted_ratings(movies):
    print()
    remaining_movies = movies.copy()
    sorted_movies = []
    highest_rated_movie = ("x",-1)
    while len(remaining_movies) > 0:
        for movie in remaining_movies.items():
            if movie[1] > highest_rated_movie[1]:
                highest_rated_movie = movie
        sorted_movies.append(highest_rated_movie)
        del remaining_movies[highest_rated_movie[0]]
        highest_rated_movie = ("x",-1)
    for film, rating in sorted_movies:
        print(Fore.CYAN + f"{film}: {rating}")
    returning_to_main()


def rating_histogram(movies):
    print()
    movie_values = list(movies.values())
    file_name = input(Fore.LIGHTGREEN_EX + "Enter file name or path to save the histogram: ")
    plt.hist(movie_values, bins = max(5, min(len(movies) // 2 + 5, 50))) # number of columns get tied to the number of films
    plt.xlabel("Rating")
    plt.ylabel("Number of movies")
    plt.title("Distribution of movie ratings")
    plt.savefig(file_name)
    plt.show()
    plt.close()
    returning_to_main()


def returning_to_main():
    print()
    input(Fore.LIGHTGREEN_EX + "Press enter to continue")
    print()


def main():
    movies = create_database()
    print(Fore.LIGHTMAGENTA_EX + "********** My Movies Database **********")
    while True:
        main_menu_choice = choose_from_main_menu()
        forwarding_main_menu(main_menu_choice, movies)


if __name__ == "__main__":
    main()