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
        pass
    elif main_menu_choice == "5":
        pass
    elif main_menu_choice == "6":
        pass
    elif main_menu_choice == "7":
        pass
    elif main_menu_choice == "8":
        pass
    else:
        print(
            "\n"
            "Please make sure your answer matches the numbers displayed in the main menu\n"
            "...Returning to main menu..."
            "\n"
        )


def returning_to_main():
    print()
    input("Press enter to continue")
    print()


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
        returning_to_main()
    else:
        print(f"Movie {deletion_choice} doesn't exist!")
        returning_to_main()


def main():
    movies = create_database()
    print("********** My Movies Database **********")
    while True:
        main_menu_choice = choose_from_main_menu()
        forwarding_main_menu(main_menu_choice, movies)


if __name__ == "__main__":
    main()
