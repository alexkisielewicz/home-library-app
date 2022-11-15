"""
Main functionalities of the program.
"""

import utils.utils
from utils.utils import *
from colorama import Fore, Style

# reads database sorting methods from CONFIG worksheet
default_sorting_method = CONFIG.acell("B1").value  # either "by title" or "by author"
optional_sorting_method = CONFIG.acell("B2").value  # always opposite value to default_sorting_method


def show_all_books():
    """
     Prints to the terminal a list of all books stored in the database.
     If database is empty database_check() prompts user to add first book.
    """
    database_check()
    print(constants.VIEW_ALL_BOOKS)
    print(constants.LINE)
    print_all_database()
    print(constants.LINE)


def add_book():
    """
    Allows user to add new book to database using user input with following data:
    author, title, category, read status and description.
    The ID of the book is generated and added automatically for each new entry.
    Function looks up the database for first empty row and inserts new entry there.
    After adding new book the database is re-sorted and all ID values are
    renumbered to keep ascending order in the database.
    """
    print(constants.ADD_BOOK)
    print(constants.LINE)

    book_to_be_added = []  # initialize variable to store all book details from user input

    while True:
        # user inputs title, then it's being validated, max 24 char allowed
        title = validate_string(Fore.LIGHTCYAN_EX + "Please enter book's title: " + Style.RESET_ALL, 24, "title")
        # checks if book title starts with "The" and returns "Title, The"
        title = check_title_prefix(title)
        # user inputs author then it's being validated, max 16 char allowed
        author = validate_string(Fore.LIGHTCYAN_EX + "Please enter book's author: " + Style.RESET_ALL, 16, "author")
        # user inputs category then it's being validated, max 12 char allowed
        category = validate_string(Fore.LIGHTCYAN_EX + "Please enter book's category: "
                                   + Style.RESET_ALL, 12, "category")
        # user choose book reading status, allowed input is 1 or 2
        while True:
            status = input(Fore.LIGHTCYAN_EX + 'Please select "1" if book is READ and "2" if NOT READ: '
                           + Style.RESET_ALL)
            if validate_num_range(status, 1, 2):  # checks if user input is digit in range 1-2
                if status == "1":
                    read_status = "Read"
                    break
                elif status == "2":
                    read_status = "Not read"
                    break

        description = validate_string(
            Fore.LIGHTCYAN_EX + "Please enter book's description: " + Style.RESET_ALL, 200, "description")

        break

    # insert all collected inputs into the list
    book_to_be_added.extend([title, author, category, read_status, description])

    clear_terminal()
    print(constants.LINE)
    first_empty_row = len(LIBRARY.get_all_values())  # look up the database for first empty row
    book_to_be_added.insert(0, first_empty_row)  # adds ID as a first item in book list - with index 0

    # Below code iterates through two lists using zip method
    # 1st list with database headers and 2nd list with book details
    # then it prints output for each pair e.g. TITLE: "Game of Thrones"
    for header, item in zip(range(len(constants.HEADERS_NO_DESC)), range(len(book_to_be_added))):
        print(f"{constants.HEADERS_NO_DESC[header]}: " + Fore.GREEN + f"{book_to_be_added[item]}" + Style.RESET_ALL)

    print(f"\n{constants.DESCRIPTION}: ")
    wrap_text(Fore.GREEN + book_to_be_added[-1].capitalize() + Style.RESET_ALL)

    print(constants.LINE)

    # Loop below is used to ask user for confirmation Y/N before adding the book,
    # the input is then validated.
    # After updating the worksheet, all records are re-sorted to keep ascending order in DB
    while True:
        are_you_sure = input(Fore.LIGHTYELLOW_EX + " \nConfirm adding this book. Y/N: " + Style.RESET_ALL)
        if validate_yes_no(are_you_sure):

            if "y" in are_you_sure or "Y" in are_you_sure:
                clear_terminal()
                LIBRARY.append_row(book_to_be_added)
                print(Fore.LIGHTYELLOW_EX + "Adding book to the database..." + Style.RESET_ALL)

                if optional_method == default_sorting_method:
                    sort(default_method)
                else:
                    sort(optional_method)
                print(Fore.GREEN + "Book added successfully." + Style.RESET_ALL)
                break
            # negative answer breaks the loop and takes user back to previous screen
            elif "n" in are_you_sure or "N" in are_you_sure:
                clear_terminal()
                print(Fore.RED + "Aborting... Book has not been added." + Style.RESET_ALL)
                break


def remove_book():
    """
    Function allows user to remove whole database entry for selected book.
    Entry deletion is followed by renumbering book's ID values to keep
    numeration in ascending order.
    """
    database_check()  # checks if DB is not empty, if so, it prompts to add first book

    print(constants.REMOVE_BOOK)
    show_all_books()  # prints a list of all books
    allowed_input = LIBRARY.col_values(1)[1:]  # creates a list with all allowed input to check against

    # Loop below is used to ask user to select book to be removed. The input is validated.
    # In case of wrong input, user is ask to select book e.g. 1-10.
    # In case there is only one book in the database, user is asked to select that book.
    # User is asked to confirm the choice before deletion. The input is validated.
    # Book is removed if positive answer is given. Database is re-sorted to keep ascending order.
    # In case of negative answer, user is taken back to previous menu.
    while True:
        user_choice = input(Fore.LIGHTYELLOW_EX + "\nPlease select a book to remove (#ID): " + Style.RESET_ALL)

        if user_choice in allowed_input:

            db_row = int(user_choice) + 1  # finds DB row counting in list zero notation
            row_str = str(db_row)
            delete_title = LIBRARY.acell("B" + row_str).value
            delete_author = LIBRARY.acell("C" + row_str).value
            delete_status = LIBRARY.acell("E" + row_str).value
            clear_terminal()

            # below condition is used to print different message depends on book's read status
            if delete_status == "Read":
                confirm = f"The book \"{delete_title.title()}\" by {delete_author.title()} will be removed."
                read_status = Fore.GREEN + f"The book is {delete_status.lower()}." + Style.RESET_ALL
                wrap_text(Fore.LIGHTYELLOW_EX + confirm + Style.RESET_ALL)
                print(read_status)

            elif delete_status == "Not read":
                confirm = f"The book \"{delete_title.title()}\" by {delete_author.title()} will be removed."
                read_status = Fore.RED + f"The book is {delete_status.lower()}." + Style.RESET_ALL
                wrap_text(Fore.LIGHTYELLOW_EX + confirm + Style.RESET_ALL)
                print(read_status)

            while True:
                are_you_sure = input(Fore.RED + "\nAre you sure you want to delete this book? Y/N: " + Style.RESET_ALL)
                if validate_yes_no(are_you_sure):

                    if "y" in are_you_sure or "Y" in are_you_sure:
                        LIBRARY.delete_rows(db_row)
                        clear_terminal()
                        print(Fore.LIGHTYELLOW_EX + "Removing book, please wait..." + Style.RESET_ALL)
                        renumber_id_column()  # to keep numeration in order after entry deletion.
                        print(Fore.GREEN + "Book removed. Database updated successfully." + Style.RESET_ALL)
                        break

                    elif "n" in are_you_sure or "N" in are_you_sure:
                        clear_terminal()
                        print(Fore.RED + "Aborting... Database hasn't been changed." + Style.RESET_ALL)
                        break

                else:
                    clear_terminal()
                    print(Fore.RED + "Wrong input, please select \"Y\" or \"N\"..." + Style.RESET_ALL)

        else:
            clear_terminal()
            # checks if there is only one book in the database
            # in this specific situation user is asked to select the only possible option
            if how_many_books() is True:
                print(Fore.RED + """Wrong input!\nNot much of a choice, you have only one book, please select it...\n"""
                               + Style.RESET_ALL)
            # if there's more than one book in the database,
            # user is given specific range of options e.g. 1-10
            elif how_many_books() is False:
                print(Fore.RED + f"""Wrong input!\nPlease select #ID from 1 to {utils.utils.last_book_id}.\n"""
                               + Style.RESET_ALL)
            remove_book()

        break


def edit_book():
    """
    Allows user to edit all database entries for each book such as:
    title, author, category, read status and description.
    All inputs are validated.
    """
    database_check()
    allowed_input = LIBRARY.col_values(1)[1:]

    while True:
        print(constants.EDIT_BOOK)
        show_all_books()
        user_choice = input(Fore.LIGHTYELLOW_EX + "\nWhich book would you like to edit?: " + Style.RESET_ALL)
        clear_terminal()

        if user_choice in allowed_input:

            db_row = int(user_choice) + 1  # finds book in the database, counting in list's zero-notation
            book_id = LIBRARY.row_values(db_row)  # assigns exact row to variable
            book_description = str(book_id[-1])
            # slices out description data, description will be printed separately
            book_no_desc = book_id[:-1]

            def print_edited_book():
                """
                Takes a list with database headers and book details and prints
                all in the form of the table using PrettyTable library.
                Maximum width of the whole table is set to 79 characters.
                Each table column has assigned maximum width individually.
                """
                print(constants.EDIT_BOOK)
                print(constants.LINE)
                x = PrettyTable()
                x.field_names = constants.HEADERS_NO_DESC  # assigns table's headers from first row in DB
                x._max_table_width = 79
                x._max_width = {"ID": 2, "Title": 24, "Author": 16, "Category": 12, "Status": 8}
                x.align["Title"] = "l"  # align column to the left
                x.add_rows([book_no_desc])  # inserts a list with book details to the table
                print(x)  # prints to the terminal created table
                print(f"\n{constants.DESCRIPTION}: ")
                # book description can be longer text that will be wrapped to the new line over 79 char.
                wrap_text(book_description)
                print(constants.LINE)

            # Once book details are presented to the user, he can choose what data he wants to edit.
            # Using this code in the loop allows user to edit details one after another in any selected order.
            while True:
                print_edited_book()
                print(Fore.GREEN + """
                1. Title 
                2. Author
                3. Category
                4. Status
                5. Description
                6. Return
                """ + Style.RESET_ALL)
                user_choice = input(Fore.LIGHTYELLOW_EX + "What do you want to edit? Select 1-6: " + Style.RESET_ALL)
                validate_num_range(user_choice, 1, 6)  # validates the input, only 1-6 is valid

                if user_choice == "1":
                    # if user choose to edit the title, function check_prefix converts
                    # the title given by the user if it contains "The ".
                    title = validate_string(Fore.LIGHTCYAN_EX + "Please update book's title: "
                                            + Style.RESET_ALL, 24, "title")
                    title = check_title_prefix(title)
                    book_no_desc[1] = title.title()  # allows to display updated title value in the table
                    LIBRARY.update_cell(db_row, 2, title.title())  # push change to database
                    print(Fore.LIGHTYELLOW_EX + "Updating database..." + Style.RESET_ALL)
                    clear_terminal()
                    print(Fore.GREEN + f'Book title updated successfully to "{title.title()}".\n' + Style.RESET_ALL)
                    print(Fore.LIGHTYELLOW_EX + "Keep editing this book or return to main menu." + Style.RESET_ALL)

                elif user_choice == "2":
                    author = validate_string(Fore.LIGHTCYAN_EX + "Please update book's author: "
                                             + Style.RESET_ALL, 16, "author")
                    book_no_desc[2] = author.title()  # allows to display updated author value in the table
                    LIBRARY.update_cell(db_row, 3, author.title())  # push change to database
                    clear_terminal()
                    print(
                        Fore.GREEN + f'Book author updated successfully to "{author.title()}".\n' + Style.RESET_ALL)
                    print(Fore.LIGHTYELLOW_EX + "Keep editing this book or return to main menu." + Style.RESET_ALL)

                elif user_choice == "3":
                    category = validate_string(Fore.LIGHTCYAN_EX + "Please update book's category: "
                                               + Style.RESET_ALL, 16, "category")
                    book_no_desc[3] = category.capitalize()  # allows to display updated category value in the table
                    LIBRARY.update_cell(db_row, 4, category.capitalize())  # push change to database
                    clear_terminal()
                    print(
                        Fore.GREEN + f'Book category updated successfully to "{category.capitalize()}".\n'
                        + Style.RESET_ALL)
                    print(Fore.LIGHTYELLOW_EX + "Keep editing this book or return to main menu." + Style.RESET_ALL)

                elif user_choice == "4":
                    # there is conditional used to give user an option to select 1 or 2 for book status
                    # instead of writing "Read" or "Not read".
                    while True:
                        select_status = input(
                            Fore.LIGHTCYAN_EX + 'Please select "1" if book is READ and "2" if NOT READ: '
                            + Style.RESET_ALL)
                        if validate_num_range(select_status, 1, 2):
                            if select_status == "1":
                                status = "Read"
                                book_no_desc[4] = status
                                LIBRARY.update_cell(db_row, 5, status)  # push change to database
                                clear_terminal()
                                print(
                                    Fore.GREEN + f'Book status updated successfully to "{status.lower()}".\n'
                                    + Style.RESET_ALL)
                                print(Fore.LIGHTYELLOW_EX + "Keep editing this book or return to main menu."
                                      + Style.RESET_ALL)
                                break
                            elif select_status == "2":
                                status = "Not read"
                                book_no_desc[4] = status
                                LIBRARY.update_cell(db_row, 5, status)
                                clear_terminal()
                                print(
                                    Fore.GREEN + f'Book status updated successfully to "{status.lower()}".\n'
                                    + Style.RESET_ALL)
                                print(Fore.LIGHTYELLOW_EX + "Keep editing this book or return to main menu."
                                      + Style.RESET_ALL)
                                break

                elif user_choice == "5":
                    description = validate_string(Fore.LIGHTCYAN_EX + "Please update book's description: "
                                                  + Style.RESET_ALL, 200, "description")
                    LIBRARY.update_cell(db_row, 6, description.capitalize())  # push change to database
                    book_description = description.capitalize()
                    clear_terminal()
                    print(Fore.GREEN + f"Book description updated successfully.\n" + Style.RESET_ALL)
                    print(Fore.LIGHTYELLOW_EX + "Keep editing this book or return." + Style.RESET_ALL)

                elif user_choice == "6":
                    clear_terminal()
                    show_all_books()  # returns to previous menu
                    break

        else:
            # The conditional is used to give user different message
            # depending on how many books there are in the database.
            # User is asked to select the only possible choice if there's only one book saved.
            # Otherwise, user is given exact number of possible options.
            if how_many_books() is True:
                print(Fore.RED + "Wrong input!\nNot much of a choice, you have only one book, please select it...\n"
                               + Style.RESET_ALL)
            elif how_many_books() is False:
                print(Fore.RED + f"Wrong input\nPlease select #ID from 1 to {utils.utils.last_book_id}.\n"
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
    database_check()  # checks if database is not empty
    show_all_books()  # displays all the books
    while True:
        print(
            Fore.LIGHTYELLOW_EX + f"Books are displayed in alphabetical order and sorted {default_sorting_method}."
            + Style.RESET_ALL)
        print(Fore.LIGHTYELLOW_EX + "How would you like to sort them?" + Style.RESET_ALL)
        # conditional is used to give user a choice, the input is validated.
        if default_sorting_method == "by title":
            print(Fore.GREEN + f"""
                    1. {optional_sorting_method.capitalize()}
                    2. Return
                    """ + Style.RESET_ALL)
        elif default_sorting_method == "by author":
            print(Fore.GREEN + f"""
                    1. {optional_sorting_method.capitalize()}
                    2. Return
                    """ + Style.RESET_ALL)
        user_choice = input(Fore.LIGHTYELLOW_EX + "Select 1 or 2: " + Style.RESET_ALL)
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
    database_check()  # checks if database is not empty
    show_all_books()  # shows user all the books
    allowed_input = LIBRARY.col_values(1)[1:]  # creates list with all possible inputs to check against

    while True:
        user_choice = input(Fore.LIGHTYELLOW_EX + "\nWhich book details would you like to see?: " + Style.RESET_ALL)

        if user_choice in allowed_input:
            db_row = int(user_choice) + 1  # because of list's zero notation
            book_id = LIBRARY.row_values(db_row)
            book_to_display = book_id[:-1]  # find last row in the database
            book_description = str(book_id[-1])  # extract selected book's description from all values

            x = PrettyTable()
            x.field_names = constants.HEADERS_NO_DESC
            # Maximum width of the whole table is set to 79 characters.
            # Each column's maximum width is assigned individually.
            x._max_table_width = 79
            x._max_width = {"ID": 2, "Title": 24, "Author": 16, "Category": 12, "Status": 8}
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
            wrap_text(book_description)  # description can be a longer text, it's wrapped over 79 char.
            print(constants.LINE)
        else:
            clear_terminal()
            # Conditional is used to give user a hint about possible input
            # If there's only one book in the database, user is asked to select it
            # If there's more than one book, user is given exact range of options e.g. 1-10
            if how_many_books() is True:
                print(Fore.RED + """Wrong input!\nNot much of a choice, you have only one book, please select it...\n"""
                               + Style.RESET_ALL)
            elif how_many_books() is False:
                print(Fore.RED + f"""Wrong input!\nPlease select #ID from 1 to {utils.utils.last_book_id}.\n"""
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
        are_you_sure = input(Fore.LIGHTYELLOW_EX + "\nAre you sure you want to quit? Y/N: " + Style.RESET_ALL)
        if validate_yes_no(are_you_sure):

            if "y" in are_you_sure or "Y" in are_you_sure:
                clear_terminal()
                print(Fore.LIGHTYELLOW_EX + f"Thank you for using {constants.APP} app!" + Style.RESET_ALL)
                print(constants.END_SCREEN)
                random_not_read()
                print(Fore.LIGHTYELLOW_EX + "\nTerminating..." + Style.RESET_ALL)
                break
            else:
                clear_terminal()
                menu.show_menu()

        else:
            quit_app()

        break
