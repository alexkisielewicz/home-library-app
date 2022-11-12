import utils.utils
from utils.utils import *


default_sorting_method = CONFIG.acell("B1").value  # either "by title" or "by author"
print("default method is set to: ", default_sorting_method)  # will be removed
optional_sorting_method = CONFIG.acell("B2").value  # always opposite value to default_sorting_method
print("optional method is set to: ", optional_sorting_method)  # will be removed

def add_book():
    print("To finish...")

def remove_book():
    """
    Function allows user to remove database entry for selected book.
    Entry deletion is followed by renumbering book's ID values to keep numeration in order without the gaps.
    """
    database_check()

    print(constants.REMOVE_BOOK)
    show_all_books()
    allowed_input = LIBRARY.col_values(1)[1:]
    how_many_books()

    while True:
        user_choice = input("Please select a book to remove (#ID): ")

        if user_choice in allowed_input:

            db_row = int(user_choice) + 1
            row_str = str(db_row)
            # book_id = LIBRARY.row_values(db_row)
            delete_title = LIBRARY.acell("B" + row_str).value
            delete_author = LIBRARY.acell("C" + row_str).value
            delete_status = LIBRARY.acell("E" + row_str).value
            clear_terminal()
            confirm = f'The book "{delete_title.title()}" by {delete_author.title()} will be removed. ' \
                      f'The book is {delete_status.lower()}.'
            wrap_text(confirm)

            while True:
                are_you_sure = input("\nAre you sure you want to delete this book? Y/N: ")
                if validate_yes_no(are_you_sure):

                    if "y" in are_you_sure or "Y" in are_you_sure:
                        LIBRARY.delete_rows(db_row)
                        clear_terminal()
                        print("Removing book, please wait...")
                        renumber_id_column()  # to keep numeration in order after entry deletion.
                        print("Book removed. Database updated successfully.")
                        menu.show_menu()
                        break
                    elif "n" in are_you_sure or "N" in are_you_sure:
                        clear_terminal()
                        print("Aborting... Database hasn't been changed.")
                        menu.show_menu()
                        break
                else:
                    clear_terminal()
                    print("Wrong input, please select \"Y\" or \"N\"...")

        else:
            clear_terminal()
            if how_many_books() is True:
                print("Not much of a choice, you have only one book, please select it...\n")
            elif how_many_books() is False:
                print(f"No such record! Please select #ID from 1 to {utils.utils.last_book_id}.\n")
            remove_book()


def show_all_books():
    """
     Prints to terminal a list of all books stored in the database.
    """
    database_check()
    print(constants.VIEW_ALL_BOOKS)
    print(constants.LINE)
    print_all_database()
    print(constants.LINE)

def edit_book():
    print("To finish...")

def change_sorting_method():
    print("To finish....")

def show_book_details():
    """
    Prints to the terminal a single book entry selected by the user.
    Takes user input and looks up the database for selected book,
    extracts and assigns all the information to variables and print
    detailed info as a table.
    """
    database_check()
    show_all_books()  # shows user all the books
    allowed_input = LIBRARY.col_values(1)[1:]

    while True:
        user_choice = input("Which book details would you like to see?: ")

        if user_choice in allowed_input:
            db_row = int(user_choice) + 1  # because of list's zero notation
            book_id = LIBRARY.row_values(db_row)
            book_to_display = book_id[:-1]  # find last row in the database
            book_description = str(book_id[-1])  # extract selected book's description from all values

            x = PrettyTable()
            x.field_names = constants.HEADERS_NO_DESC
            x.add_rows([book_to_display])
            clear_terminal()
            print(constants.SHOW_BOOK_DETAILS)
            print(constants.LINE)
            print(x)
            print(f"\n{constants.DESCRIPTION}: ")
            wrap_text(book_description)
            print(constants.LINE)
        else:
            clear_terminal()
            if how_many_books() is True:
                print("Not much of a choice, you have only one book, please select it...\n")
            elif how_many_books() is False:
                print(f"No such record! Please select #ID from 1 to {utils.utils.last_book_id}.\n")
            show_book_details()

        break


def change_sorting_method():
    """
    Changes sorting method
    """
    database_check()
    show_all_books()
    while True:
        print(f"Books are displayed in alphabetical order and sorted {default_sorting_method}.")
        print("How would you like to sort them?")
        if default_sorting_method == "by title":
            print(f"""
                    1. {optional_sorting_method.capitalize()}
                    2. Return
                    """)
        elif default_sorting_method == "by author":
            print(f"""
                    1. {optional_sorting_method.capitalize()}
                    2. Return
                    """)
        user_choice = input("Select 1 or 2: ")
        clear_terminal()
        validate_num_range(user_choice, 1, 2)
        if user_choice == "1":
            sort(optional_sorting_method)
            show_all_books()
            break
        elif user_choice == "2":
            clear_terminal()
            show_all_books()
            break


def quit_app():
    """
     This function prints goodbye message to the user
    """
    while True:
        print("Why not add another book...?:)")
        are_you_sure = input("\nAre you sure you want to quit? Y/N: ")
        validate_yes_no(are_you_sure)

        if "y" in are_you_sure or "Y" in are_you_sure:
            clear_terminal()
            print(f"Thank you for using {constants.APP} app!")
            print(constants.END_SCREEN)
            random_not_read()
            print("\nTerminating...")
            break
        else:
            menu.show_menu()
            break