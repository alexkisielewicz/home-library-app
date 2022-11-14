"""
Main project file to run application
"""

import app_menu as menu


def main():
    """
    Main function of the program. Shows app menu, from where user can start
    and further use all the app functionalities.
    """
    menu.logo()
    menu.show_menu()


main()


# TODO
# * Validate User input in BOOK ADD and BOOK EDIT fn
# * Exception handling PROJECT CRITERIA: "Write code that handles empty or invalid input data"
# * Criteria: Implement exception/error handling to optimise the user experience
# * PrettyTable colour? Where?
# * Write type hinting
