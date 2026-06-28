import random


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
    print(
        "Menu:\n"
        "1. List movies\n"
        "2. Add movie\n"
        "3. Delete movie\n"
        "4. Update movie\n"
        "5. Stats\n"
        "6. Random movie\n"
        "7. Search movie\n"
        "8. Movies sorted by rating\n"
    )
    return input("Enter choice (1-8): ")


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
        pass
    else:
        print(
            "\n"
            "Please make sure your answer matches the numbers displayed in the main menu\n"
            "...Returning to main menu..."
            "\n"
        )


def list_movies(movies):
    print()
    print(f"{len(movies)} movies in total")
    for movie, rating in movies.items():
        print(f"{movie}: {rating}")
    returning_to_main()


def add_movie(movies):
    print()
    new_movie_title = input("Enter new movie name: ")
    new_movie_rating = float(input("Enter new movie rating (0-10): "))
    movies[new_movie_title] = new_movie_rating
    print(f"Movie {new_movie_title} successfully added")
    returning_to_main()


def delete_movie(movies):
    print()
    deletion_choice = input("Enter movie name to delete: ")
    if deletion_choice in movies:
        del movies[deletion_choice]
        print(f"Movie {deletion_choice} successfully deleted")
    else:
        print(f"Movie {deletion_choice} doesn't exist!")
    returning_to_main()


def update_movie(movies):
    print()
    update_choice = input("Enter movie name to update: ")
    if update_choice in movies:
        update_movie_rating =  float(input("Enter new movie rating (0-10): "))
        movies[update_choice] = update_movie_rating
        print(f"Movie {update_choice} successfully updated")
    else:
        print(f"Movie {update_choice} doesn't exist!")
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
    print(f"Average rating: {average_rating:.2f}")
    print(f"Median rating: {median_rating:.2f}")
    if len(best_movies) > 1:
        print(f"{len(best_movies)} Movies share the category best movie with a rating of {best_movies[0][1]}")
        for movie in best_movies:
            print(f"-{movie[0]}")
    else:
        print(f"Best movie: {best_movies[0][0]}, {best_movies[0][1]}")
    if len(worst_movies) > 1:
        print(f"{len(worst_movies)} Movies share the category worst movie with a rating of {worst_movies[0][1]}")
        for movie in worst_movies:
            print(f"- {movie[0]}")
    else:
        print(f"Worst movie: {worst_movies[0][0]}, {worst_movies[0][1]}")


def random_movie(movies):
    print()
    r_movie, r_rating = random.choice(list(movies.items()))
    print(f"Your movie for tonight: {r_movie}, it's rated {r_rating}")
    returning_to_main()


def search_movie(movies):
    print()
    search_input = input("Enter part of movie name: ").lower()
    counter = 0
    for movie, rating in movies.items():
        if search_input in movie.lower():
            print(f"{movie}: {rating}")
            counter += 1
    if counter == 0:
        print(f"No movie containing '{search_input}' found.")
    returning_to_main()


#def movies_sorted_ratings(movies):





def returning_to_main():
    print()
    input("Press enter to continue")
    print()


def main():
    movies = create_database()
    print("********** My Movies Database **********")
    while True:
        main_menu_choice = choose_from_main_menu()
        forwarding_main_menu(main_menu_choice, movies)


if __name__ == "__main__":
    main()
