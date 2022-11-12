"""
Home screen consists of logo and main menu.
"""
import constants

def logo():
    print("""
    ██   ██  ██████  ███    ███ ███████     ██      ██ ██████  ██████   █████  ██████  ██    ██ 
    ██   ██ ██    ██ ████  ████ ██          ██      ██ ██   ██ ██   ██ ██   ██ ██   ██  ██  ██  
    ███████ ██    ██ ██ ████ ██ █████       ██      ██ ██████  ██████  ███████ ██████    ████   
    ██   ██ ██    ██ ██  ██  ██ ██          ██      ██ ██   ██ ██   ██ ██   ██ ██   ██    ██    
    ██   ██  ██████  ██      ██ ███████     ███████ ██ ██████  ██   ██ ██   ██ ██   ██    ██                                                                           
    """)
    print(f"Welcome to {constants.APP} app, you can manage all your books here. Please select option 1-7 to continue.")


logo()

def menu():
    print("""
    1. Add book
    2. Edit book
    3. Remove book
    4. View all books
    5. Change sorting method
    6. Show #book details
    7. Quit
    """)

def show_menu():
    while True:
        menu()  # prints menu
        user_choice = input("Please select a number from 1 to 7 to continue: ")
        clear_terminal()

        if user_choice == "1":
            clear_terminal()
            add_book()
        elif user_choice == "2":
            clear_terminal()
            edit_book()
        elif user_choice == "3":
            clear_terminal()
            remove_book()
        elif user_choice == "4":
            clear_terminal()
            show_all_books()
        elif user_choice == "5":
            clear_terminal()
            change_sorting_method()
        elif user_choice == "6":
            clear_terminal()
            show_book_details()
        elif user_choice == "7":
            clear_terminal()
            quit_app()
            break