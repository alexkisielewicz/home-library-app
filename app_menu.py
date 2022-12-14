"""
Home screen consists of logo and main menu.
"""

import constants
from scripts import functions as fn
from utils.utils import clear_terminal, validate_num_range
from colorama import Fore, Style


def logo():
    """
     http://patorjk.com/software/taag/#p=display&f=Graffiti&t=Type%20Something%20
    """
    print(Fore.LIGHTCYAN_EX + """
   _   _                        _     _ _                          
  | | | |                      | |   (_) |                         
  | |_| | ___  _ __ ___   ___  | |    _| |__  _ __ __ _ _ __ _   _ 
  |  _  |/ _ \| '_ ` _ \ / _ \ | |   | | '_ \| '__/ _` | '__| | | |
  | | | | (_) | | | | | |  __/ | |___| | |_) | | | (_| | |  | |_| |
  \_| |_/\___/|_| |_| |_|\___| \_____/_|_.__/|_|  \__,_|_|   \__, |
                                                              __/ |
                                                             |___/                                                                                                                      
    """ + Style.RESET_ALL)
    print(Fore.LIGHTYELLOW_EX
          + f"Welcome to {constants.APP}, you can manage all your books here."
            f"\nPlease use menu below to continue." + Style.RESET_ALL)


def menu():
    print(Fore.LIGHTGREEN_EX + """
    1. Add book
    2. Edit book
    3. Remove book
    4. View all books
    5. Change sorting method
    6. Show book details
    7. Quit
    """ + Style.RESET_ALL)


def show_menu():
    while True:
        menu()  # prints menu
        user_choice = input(Fore.LIGHTYELLOW_EX
                            + "Please select a number from 1 to 7 "
                              "to continue: "
                            + Style.RESET_ALL)
        clear_terminal()
        # validates user input, only values from 1 to 7 are allowed
        validate_num_range(user_choice, 1, 7)
        if user_choice == "1":
            fn.add_book()
        elif user_choice == "2":
            fn.edit_book()
        elif user_choice == "3":
            fn.remove_book()
        elif user_choice == "4":
            fn.show_all_books()
        elif user_choice == "5":
            fn.change_sorting_method()
        elif user_choice == "6":
            fn.show_book_details()
        elif user_choice == "7":
            fn.quit_app()
            break
