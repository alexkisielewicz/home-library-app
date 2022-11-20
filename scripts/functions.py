"""
Main functionalities of the program.
"""

import utils.utils
from utils.utils import *
import app_menu as menu
from colorama import Fore, Style

# reads database sorting methods from CONFIG worksheet
# either "by title" or "by author"
default_sorting_method = CONFIG.acell("B1").value
# always opposite value to default_sorting_method
optional_sorting_method = CONFIG.acell("B2").value


def show_all_books():
    """
     Prints to the terminal a list of all books stored in the database.
     If database is empty database_check() prompts user to add first book.
    """
    if database_check():
        pass
    else:
        print(constants.VIEW_ALL_BOOKS)
        print(constants.LINE)
        print_all_database()
        print(constants.LINE)


def add_book():
    """
    Allows user to add new book to database using user input with following
    data: author, title, category, read status and description.
    The ID of the book is generated and added automatically for each new entry.
    Function looks up the database for first empty row and inserts new entry
    there. After adding new book the database is re-sorted and all ID values
    are renumbered to keep ascending order in the database.
    """
    print(constants.ADD_BOOK)
    print(constants.LINE)

    # initialize variable to store all book details from user input
    book_to_be_added = []

    while True:
        # user inputs title, then it's being validated, max 24 char allowed
        title = validate_string(Fore.LIGHTCYAN_EX
                                + "Please enter book's title: "
                                + Style.RESET_ALL, constants.TITLE_MAX_LEN,
                                "title")
        # checks if book title starts with "The" and returns "Title, The"
        title = check_title_prefix(title)
        # user inputs author then it's being validated, max 16 char allowed
        author = validate_string(Fore.LIGHTCYAN_EX
                                 + "Please enter book's author: "
                                 + Style.RESET_ALL, constants.AUTHOR_MAX_LEN,
                                 "author")
        # user inputs category then it's being validated, max 12 char allowed
        category = validate_string(Fore.LIGHTCYAN_EX
                                   + "Please enter book's category: "
                                   + Style.RESET_ALL, constants.CAT_MAX_LEN,
                                   "category")
        # user choose book reading status, allowed input is 1 or 2
        while True:
            status = input(Fore.LIGHTCYAN_EX
                           + "Please select \"1\" if you read that book "
                             "or \"2\" if you didn't: "
                           + Style.RESET_ALL)
            # checks if user input is digit in range 1-2
            if validate_num_range(status, 1, 2):
                if status == "1":
                    read_status = constants.READ_YES
                    break
                elif status == "2":
                    read_status = constants.READ_NO
                    break

        description = validate_string(
            Fore.LIGHTCYAN_EX + "Please enter book's description: "
                              + Style.RESET_ALL, constants.DESC_MAX_LEN,
                                "description")

        break

    # insert all collected inputs into the list
    book_to_be_added.extend([title, author, category, read_status,
                             description])

    clear_terminal()
    print(constants.LINE)
    first_empty_row = len(LIBRARY.get_all_values())
    book_to_be_added.insert(0, first_empty_row)

    # Below code iterates through two lists using zip method
    # 1st list with database headers and 2nd list with book details
    # then it prints output for each pair e.g. TITLE: "Game of Thrones"
    for header, item in zip(range(len(constants.HEADERS_NO_DESC)),
                            range(len(book_to_be_added))):
        print(f"{constants.HEADERS_NO_DESC[header]}: " + Fore.LIGHTGREEN_EX
              + f"{book_to_be_added[item]}" + Style.RESET_ALL)

    print(f"\n{constants.DESCRIPTION}: ")
    wrap_text(Fore.LIGHTGREEN_EX + book_to_be_added[-1].capitalize()
                                 + Style.RESET_ALL)

    print(constants.LINE)

    # Loop is used to ask user for confirmation Y/N before adding the book,
    # the input is then validated.
    # After updating the worksheet, all records are re-sorted
    # to keep ascending order in DB
    while True:
        are_you_sure = input(Fore.LIGHTYELLOW_EX
                             + " \nConfirm adding this book. Y/N: "
                             + Style.RESET_ALL)
        if validate_yes_no(are_you_sure):

            if "y" in are_you_sure or "Y" in are_you_sure:
                clear_terminal()
                LIBRARY.append_row(book_to_be_added)
                print(Fore.LIGHTYELLOW_EX + "Adding book to the database..."
                                          + Style.RESET_ALL)

                if optional_method == default_sorting_method:
                    sort(default_method)
                else:
                    sort(optional_method)
                print(Fore.LIGHTGREEN_EX + "Book added successfully."
                                         + Style.RESET_ALL)
                break
            # negative answer breaks the loop and takes user back
            elif "n" in are_you_sure or "N" in are_you_sure:
                clear_terminal()
                print(Fore.LIGHTRED_EX + "Aborting... Book has not been added."
                      + Style.RESET_ALL)
                break


def remove_book():
    """
    Function allows user to remove whole database entry for selected book.
    Entry deletion is followed by renumbering book's ID values to keep
    numeration in ascending order.
    """
    if database_check():  # checks if DB is not empty
        pass
    else:
        print(constants.REMOVE_BOOK)
        show_all_books()  # prints a list of all books
        # creates a list with all allowed input to check against
        allowed_input = LIBRARY.col_values(1)[1:]

        # Loop below is used to ask user to select book to be removed.
        # The input is validated. In case of wrong input, user is ask to select
        # book e.g. 1-10. In case there is only one book in the database,
        # user is asked to select that book. User is asked to confirm the
        # choice before deletion. The input is validated. Book is removed if
        # positive answer is given. Database is re-sorted to keep ascending
        # order. In case of negative answer, user is taken back to previous
        # menu.
        while True:
            user_choice = input(Fore.LIGHTYELLOW_EX
                                + "\nPlease select a book to remove (#ID): "
                                + Style.RESET_ALL)

            if user_choice in allowed_input:
                # finds DB row counting in list zero notation
                db_row = int(user_choice) + 1
                row_str = str(db_row)
                delete_title = LIBRARY.acell("B" + row_str).value
                delete_author = LIBRARY.acell("C" + row_str).value
                delete_status = LIBRARY.acell("E" + row_str).value
                clear_terminal()

                # below condition is used to print different message
                # depends on book's read status
                if delete_status == constants.READ_YES:
                    confirm = f"The book \"{delete_title.title()}\" by " \
                              f"{delete_author.title()} will be removed."
                    read_status = \
                        Fore.LIGHTGREEN_EX \
                        + f"The book is {delete_status.lower()}." \
                        + Style.RESET_ALL
                    wrap_text(Fore.LIGHTYELLOW_EX + confirm + Style.RESET_ALL)
                    print(read_status)

                elif delete_status == constants.READ_NO:
                    confirm = f"The book \"{delete_title.title()}\" " \
                              f"by {delete_author.title()} will be removed."
                    read_status = \
                        Fore.LIGHTRED_EX \
                        + f"The book is {delete_status.lower()}." \
                        + Style.RESET_ALL
                    wrap_text(Fore.LIGHTYELLOW_EX + confirm + Style.RESET_ALL)
                    print(read_status)

                while True:
                    are_you_sure = \
                        input(Fore.LIGHTRED_EX
                              + "\nAre you sure you want to delete "
                                "this book? Y/N: "
                              + Style.RESET_ALL)
                    if validate_yes_no(are_you_sure):

                        if "y" in are_you_sure or "Y" in are_you_sure:
                            LIBRARY.delete_rows(db_row)
                            clear_terminal()
                            print(Fore.LIGHTYELLOW_EX
                                  + "Removing book, please wait..."
                                  + Style.RESET_ALL)
                            renumber_id_column()
                            print(Fore.LIGHTGREEN_EX
                                  + "Book removed. Database updated "
                                    "successfully."
                                  + Style.RESET_ALL)
                            break

                        elif "n" in are_you_sure or "N" in are_you_sure:
                            clear_terminal()
                            print(Fore.LIGHTRED_EX
                                  + "Aborting... Database hasn't been changed."
                                  + Style.RESET_ALL)
                            break

                    else:
                        clear_terminal()
                        print(Fore.LIGHTRED_EX
                              + "Wrong input, please select \"Y\" or \"N\"..."
                              + Style.RESET_ALL)

            else:
                clear_terminal()
                # checks if there is only one book in the database
                # in this specific situation user is asked to select
                # the only possible option
                if has_multiple_books():
                    print(Fore.LIGHTRED_EX +
                          "Wrong input!\nNot much of a choice, "
                          "you have only one book, please select it...\n"
                          + Style.RESET_ALL)
                # if there's more than one book in the database,
                # user is given specific range of options e.g. 1-10
                elif has_multiple_books() is False:
                    print(Fore.LIGHTRED_EX +
                          f"Wrong input!\nPlease select #ID from 1 "
                          f"to {utils.utils.last_book_id}.\n"
                          + Style.RESET_ALL)
                remove_book()

            break


def edit_book():
    """
    Allows user to edit all database entries for each book such as:
    title, author, category, read status and description.
    All inputs are validated.
    """
    if database_check():
        pass
    else:
        allowed_input = LIBRARY.col_values(1)[1:]

        while True:
            print(constants.EDIT_BOOK)
            show_all_books()
            user_choice = input(Fore.LIGHTYELLOW_EX
                                + "\nWhich book would you like to edit?: "
                                + Style.RESET_ALL)
            clear_terminal()

            if user_choice in allowed_input:
                # finds book in the database, counting in list's zero-notation
                db_row = int(user_choice) + 1
                # assigns exact row to variable
                book_id = LIBRARY.row_values(db_row)
                book_description = str(book_id[-1])
                book_no_desc = book_id[:-1]

                def print_edited_book():
                    """
                    Takes a list with database headers and book details and
                    prints all in the form of the table using PrettyTable
                    library. Maximum width of the whole table is set to 79
                    characters.Each table column has assigned maximum width
                    individually.
                    """
                    print(constants.EDIT_BOOK)
                    print(constants.LINE)
                    x = PrettyTable()
                    # assigns table's headers from first row in DB
                    x.field_names = constants.HEADERS_NO_DESC
                    x._max_table_width = constants.TABLE_MAX_LEN
                    x._max_width = constants.MAX_LEN
                    x.align["Title"] = "l"  # align column to the left
                    # inserts a list with book details to the table
                    x.add_rows([book_no_desc])
                    print(x)  # prints to the terminal created table
                    print(f"\n{constants.DESCRIPTION}: ")
                    # book description can be longer text that will
                    # be wrapped to the new line over 79 char.
                    wrap_text(book_description)
                    print(constants.LINE)

                # Once book details are presented to the user, he can choose
                # what data he wants to edit. Using this code in the loop
                # allows user to edit details one after another in any
                # selected order.
                while True:
                    print_edited_book()
                    print(Fore.LIGHTGREEN_EX + """
                    1. Title
                    2. Author
                    3. Category
                    4. Status
                    5. Description
                    6. Return
                    """ + Style.RESET_ALL)
                    user_choice = input(Fore.LIGHTYELLOW_EX
                                        + "What do you want to edit? "
                                          "Select 1-6: "
                                        + Style.RESET_ALL)
                    validate_num_range(user_choice, 1, 6)

                    if user_choice == "1":
                        # if user choose to edit the title, function
                        # check_prefix converts the title given by the user
                        # if it contains "The ".
                        title = validate_string(Fore.LIGHTCYAN_EX
                                                + "Please update book's "
                                                  "title: "
                                                + Style.RESET_ALL,
                                                constants.TITLE_MAX_LEN,
                                                "title")
                        title = check_title_prefix(title)
                        book_no_desc[1] = title.title()
                        LIBRARY.update_cell(db_row, 2, title.title())
                        print(Fore.LIGHTYELLOW_EX + "Updating database..."
                              + Style.RESET_ALL)
                        clear_terminal()
                        print(Fore.LIGHTGREEN_EX
                              + f'Book title updated successfully to '
                                f'"{title.title()}".\n'
                              + Style.RESET_ALL)
                        print(Fore.LIGHTYELLOW_EX
                              + "Keep editing this book or return to "
                                "main menu."
                              + Style.RESET_ALL)

                    elif user_choice == "2":
                        author = validate_string(Fore.LIGHTCYAN_EX
                                                 + "Please update book's "
                                                   "author: "
                                                 + Style.RESET_ALL,
                                                 constants.TITLE_MAX_LEN,
                                                 "author")
                        book_no_desc[2] = author.title()
                        LIBRARY.update_cell(db_row, 3, author.title())
                        clear_terminal()
                        print(
                            Fore.LIGHTGREEN_EX
                            + f'Book author updated successfully '
                              f'to "{author.title()}".\n'
                            + Style.RESET_ALL)
                        print(Fore.LIGHTYELLOW_EX + "Keep editing this book "
                                                    "or return to main menu."
                                                  + Style.RESET_ALL)

                    elif user_choice == "3":
                        category = validate_string(
                            Fore.LIGHTCYAN_EX + "Please update book's "
                                                "category: "
                            + Style.RESET_ALL, constants.CAT_MAX_LEN,
                            "category")
                        # allows to display updated category value in the table
                        book_no_desc[3] = category.capitalize()
                        # push change to database
                        LIBRARY.update_cell(db_row, 4, category.capitalize())
                        clear_terminal()
                        print(
                            Fore.LIGHTGREEN_EX
                            + f'Book category updated successfully '
                              f'to "{category.capitalize()}".\n'
                            + Style.RESET_ALL)
                        print(Fore.LIGHTYELLOW_EX + "Keep editing this "
                                                    "book or "
                                                    "return to main menu."
                                                  + Style.RESET_ALL)

                    elif user_choice == "4":
                        # there is conditional used to give user an option to
                        # select 1 or 2 for book status
                        # instead of writing "Read" or "Not read".
                        while True:
                            select_status = input(
                                Fore.LIGHTCYAN_EX
                                + "Please select \"1\" if you read that book "
                                  "or \"2\" if you didn't: "
                                + Style.RESET_ALL)
                            if validate_num_range(select_status, 1, 2):
                                if select_status == "1":
                                    status = constants.READ_YES
                                    book_no_desc[4] = status
                                    LIBRARY.update_cell(db_row, 5, status)
                                    clear_terminal()
                                    print(
                                        Fore.LIGHTGREEN_EX
                                        + f'Book status updated successfully '
                                          f'to "{status.lower()}".\n'
                                        + Style.RESET_ALL)
                                    print(Fore.LIGHTYELLOW_EX
                                          + "Keep editing this book or return "
                                            "to main menu."
                                          + Style.RESET_ALL)
                                    break
                                elif select_status == "2":
                                    status = constants.READ_NO
                                    book_no_desc[4] = status
                                    LIBRARY.update_cell(db_row, 5, status)
                                    clear_terminal()
                                    print(
                                        Fore.LIGHTGREEN_EX
                                        + f'Book status updated successfully '
                                          f'to "{status.lower()}".\n'
                                        + Style.RESET_ALL)
                                    print(Fore.LIGHTYELLOW_EX
                                          + "Keep editing this book or return "
                                            "to main menu."
                                          + Style.RESET_ALL)
                                    break

                    elif user_choice == "5":
                        description = \
                            validate_string(Fore.LIGHTCYAN_EX
                                            + "Please update book's "
                                              "description: "
                                            + Style.RESET_ALL,
                                            constants.DESC_MAX_LEN,
                                            "description")
                        LIBRARY.update_cell(db_row, 6,
                                            description.capitalize())
                        book_description = description.capitalize()
                        clear_terminal()
                        print(Fore.LIGHTGREEN_EX
                              + f"Book description updated successfully.\n"
                              + Style.RESET_ALL)
                        print(Fore.LIGHTYELLOW_EX
                              + "Keep editing this book or return."
                              + Style.RESET_ALL)

                    elif user_choice == "6":
                        clear_terminal()
                        show_all_books()  # returns to previous menu
                        break

            else:
                # The conditional is used to give user different message
                # depending on how many books there are in the database.
                # User is asked to select the only possible choice if there's
                # only one book saved. Otherwise, user is given exact number
                # of possible options.
                if has_multiple_books():
                    print(Fore.LIGHTRED_EX +
                          "Wrong input!\nNot much of a choice, you have "
                          "only one book, please select it...\n"
                          + Style.RESET_ALL)
                elif has_multiple_books() is False:
                    print(Fore.LIGHTRED_EX + f"Wrong input\nPlease select #ID "
                                             f"from 1 to "
                                             f"{utils.utils.last_book_id}.\n"
                                           + Style.RESET_ALL)

                edit_book()

            break


def change_sorting_method():
    """
    Changes sorting method to keep database entries in ascending order.
    Books are sorted alphabetically in ascending order.
    Possible sorting methods: by title, or by author.
    User can choose how to sort and display books.
    If database is empty user is asked to add first book to continue.
    """
    if database_check():  # checks if database is not empty
        pass
    else:
        show_all_books()  # displays all the books
        while True:
            print(
                Fore.LIGHTYELLOW_EX
                + f"Books are displayed in alphabetical order and sorted "
                  f"{default_sorting_method}."
                + Style.RESET_ALL)
            print(Fore.LIGHTYELLOW_EX
                  + "How would you like to sort them?" + Style.RESET_ALL)
            if default_sorting_method == "by title":
                print(Fore.LIGHTGREEN_EX + f"""
                        1. {optional_sorting_method.capitalize()}
                        2. Return
                        """ + Style.RESET_ALL)
            elif default_sorting_method == "by author":
                print(Fore.LIGHTGREEN_EX + f"""
                        1. {optional_sorting_method.capitalize()}
                        2. Return
                        """ + Style.RESET_ALL)
            user_choice = input(Fore.LIGHTYELLOW_EX + "Select 1 or 2: "
                                + Style.RESET_ALL)
            clear_terminal()
            validate_num_range(user_choice, 1, 2)  # only digits 1-2 are valid
            if user_choice == "1":
                sort(optional_sorting_method)
                show_all_books()
                break
            elif user_choice == "2":
                clear_terminal()
                show_all_books()
                break


def show_book_details():
    """
    Prints to the terminal a single book entry selected by the user.
    Takes user input and looks up the database for selected book,
    extracts and assigns all the information to variables and print
    detailed info as a table using PrettyTable library.
    If database is empty user is asked to add first book to continue.
    """
    if database_check():  # checks if database is not empty
        pass
    else:
        show_all_books()  # shows user all the books
        # creates list with all possible inputs to check against
        allowed_input = LIBRARY.col_values(1)[1:]

        while True:
            user_choice = input(Fore.LIGHTYELLOW_EX
                                + "\nWhich book details would you like "
                                  "to see?: "
                                + Style.RESET_ALL)

            if user_choice in allowed_input:
                db_row = int(user_choice) + 1
                book_id = LIBRARY.row_values(db_row)
                book_to_display = book_id[:-1]  # find last row in the database
                book_description = str(book_id[-1])

                x = PrettyTable()
                x.field_names = constants.HEADERS_NO_DESC
                # Maximum width of the whole table is set to 79 characters.
                # Each column's maximum width is assigned individually.
                x._max_table_width = constants.TABLE_MAX_LEN
                x._max_width = constants.MAX_LEN
                x.add_rows([book_to_display])
                x.align["ID"] = "r"  # aligns column to the right
                x.align["Title"] = "l"  # aligns column to the left
                x.align["Author"] = "l"
                x.align["Category"] = "l"
                x.align["Status"] = "l"
                clear_terminal()
                print(constants.SHOW_BOOK_DETAILS)
                print(constants.LINE)
                print(x)
                print(f"\n{constants.DESCRIPTION}: ")
                wrap_text(book_description)
                print(constants.LINE)
            else:
                clear_terminal()
                # Conditional is used to give user a hint about possible input
                # If there's only one book in the database, user is asked to
                # select it. If there's more than one book, user is given exact
                # range of options e.g. 1-10
                if has_multiple_books():
                    print(Fore.LIGHTRED_EX +
                          "Wrong input!\nNot much of a choice, you have only "
                          "one book, please select it...\n"
                          + Style.RESET_ALL)
                elif has_multiple_books() is False:
                    print(Fore.LIGHTRED_EX +
                          f"Wrong input!\nPlease select #ID from 1 "
                          f"to {utils.utils.last_book_id}.\n"
                          + Style.RESET_ALL)
                show_book_details()

            break


def quit_app():
    """
     This function prints goodbye message to the user.
     It displays app credits and developers social links.
     User is asked to confirm exit and random quote is printed.
     Next read suggestion is printed to the user if in database
     is any book with status "Not read".
    """
    while True:
        random_quit_msg()
        are_you_sure = input(Fore.LIGHTYELLOW_EX
                             + "\nAre you sure you want to quit? Y/N: "
                             + Style.RESET_ALL)
        if validate_yes_no(are_you_sure):

            if "y" in are_you_sure or "Y" in are_you_sure:
                clear_terminal()
                print(Fore.LIGHTYELLOW_EX
                      + f"Thank you for using {constants.APP} app!"
                      + Style.RESET_ALL)
                print(constants.END_SCREEN)
                random_not_read()
                print(Fore.LIGHTYELLOW_EX + "\nTerminating..."
                                          + Style.RESET_ALL)
                break
            else:
                clear_terminal()
                menu.show_menu()

        else:
            quit_app()

        break
