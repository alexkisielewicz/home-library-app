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
    print(Fore.LIGHTBLUE_EX + """
   _   _                        _     _ _                          
  | | | |                      | |   (_) |                         
  | |_| | ___  _ __ ___   ___  | |    _| |__  _ __ __ _ _ __ _   _ 
  |  _  |/ _ \| '_ ` _ \ / _ \ | |   | | '_ \| '__/ _` | '__| | | |
  | | | | (_) | | | | | |  __/ | |___| | |_) | | | (_| | |  | |_| |
  \_| |_/\___/|_| |_| |_|\___| \_____/_|_.__/|_|  \__,_|_|   \__, |
                                                              __/ |
                                                             |___/                                                                                                                      
    """ + Style.RESET_ALL)
    print(Fore.LIGHTYELLOW_EX + f"Welcome to {constants.APP} app, you can manage all your books here. "
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
        user_choice = input(Fore.YELLOW + "Please select a number from 1 to 7 to continue: " + Style.RESET_ALL)
        clear_terminal()
        validate_num_range(user_choice, 1, 7)  # validates user input, only values from 1 to 7 are allowed
        if user_choice == "1":
            clear_terminal()
            fn.add_book()
        elif user_choice == "2":
            clear_terminal()
            fn.edit_book()
        elif user_choice == "3":
            clear_terminal()
            fn.remove_book()
        elif user_choice == "4":
            clear_terminal()
            fn.show_all_books()
        elif user_choice == "5":
            clear_terminal()
            fn.change_sorting_method()
        elif user_choice == "6":
            clear_terminal()
            fn.show_book_details()
        elif user_choice == "7":
            clear_terminal()
            fn.quit_app()
            break
