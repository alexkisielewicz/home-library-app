import app_menu as menu


def main():
    """
    Main function of the program. Shows app menu, from where user can start
    and use all the app functionalities.
    """
    menu.logo()
    menu.show_menu()


main()


# TODO
# * Validate User input in BOOK ADD and BOOK EDIT fn
# * Exception handling
# * PrettyTable colour? Where?
# * Write type hinting
# * Add docstrings and inline comments
