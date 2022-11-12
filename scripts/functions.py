import utils.utils
from utils.utils import *

def add_book():

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

def change_sorting_method():

def show_book_details():

def quit_app():