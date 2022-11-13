import utils.utils
from utils.utils import *
from colorama import Fore, Style

default_sorting_method = CONFIG.acell("B1").value  # either "by title" or "by author"
optional_sorting_method = CONFIG.acell("B2").value  # always opposite value to default_sorting_method


def show_all_books():
    """
     Prints to terminal a list of all books stored in the database.
    """
    database_check()
    print(constants.VIEW_ALL_BOOKS)
    print(constants.LINE)
    print_all_database()
    print(constants.LINE)


def add_book():
    """
    Allows user to add new book to database using user input with following values:
    author, title, category, read status and description.
    The ID of the book is generated and added automatically for each new entry.
    Function looks up the database for first empty row and inserts new entry there.
    """
    print(constants.ADD_BOOK)
    print(constants.LINE)

    book_to_be_added = []

    title = check_prefix()  # checks if book title starts with "The" and returns "Title, The"
    validate_string(title)
    author = input(Fore.YELLOW + "Please enter the author: " + Style.RESET_ALL).title()
    validate_string(author)
    category = input(Fore.YELLOW + "Please enter book category: " + Style.RESET_ALL).capitalize()
    validate_string(category)

    while True:
        status = input(Fore.YELLOW + 'Please select "1" if book is READ and "2" if NOT READ: ' + Style.RESET_ALL)
        if validate_num_range(status, 1, 2):
            if status == "1":
                read_status = "Read"
                break
            elif status == "2":
                read_status = "Not read"
                break

        else:
            print(Fore.RED + f"Please try again...\n" + Style.RESET_ALL)

    description = input(Fore.YELLOW + "Please enter book description: " + Style.RESET_ALL).capitalize()
    validate_string(description)
    book_to_be_added.extend([title, author, category, read_status, description])
    clear_terminal()
    print(constants.LINE)
    first_empty_row = len(LIBRARY.get_all_values())  # look up database for first empty row

    book_to_be_added.insert(0, first_empty_row)  # adds ID as a first item in book list
    for header, item in zip(range(len(constants.HEADERS_NO_DESC)), range(len(book_to_be_added))):
        print(f"{constants.HEADERS_NO_DESC[header]}: " + Fore.GREEN + f"{book_to_be_added[item]}" + Style.RESET_ALL)

    print(f"\n{constants.DESCRIPTION}: ")
    wrap_text(Fore.GREEN + book_to_be_added[-1].capitalize() + Style.RESET_ALL)

    print(constants.LINE)

    while True:
        are_you_sure = input(Fore.YELLOW + " \nConfirm adding this book. Y/N: " + Style.RESET_ALL)
        if validate_yes_no(are_you_sure):

            if "y" in are_you_sure or "Y" in are_you_sure:
                clear_terminal()
                LIBRARY.append_row(book_to_be_added)
                print(Fore.YELLOW + "Adding book to the database..." + Style.RESET_ALL)

                if optional_method == default_sorting_method:  # sorting is required to keep order in database
                    sort(default_method)
                else:
                    sort(optional_method)
                print(Fore.GREEN + "Book added successfully." + Style.RESET_ALL)
                break

            elif "n" in are_you_sure or "N" in are_you_sure:
                clear_terminal()
                print(Fore.RED + "Aborting..." + Style.RESET_ALL)
                break
        else:
            clear_terminal()
            print(Fore.RED + "Wrong input, please select \"Y\" or \"N\"..." + Style.RESET_ALL)
            # menu.show_menu()


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
        user_choice = input(Fore.YELLOW + "\nPlease select a book to remove (#ID): " + Style.RESET_ALL)

        if user_choice in allowed_input:

            db_row = int(user_choice) + 1
            row_str = str(db_row)
            # book_id = LIBRARY.row_values(db_row)
            delete_title = LIBRARY.acell("B" + row_str).value
            delete_author = LIBRARY.acell("C" + row_str).value
            delete_status = LIBRARY.acell("E" + row_str).value
            clear_terminal()

            if delete_status == "Read":
                confirm = f"The book \"{delete_title.title()}\" by {delete_author.title()} will be removed." \
                          + Fore.GREEN + f"\nThe book is {delete_status.lower()}." + Style.RESET_ALL
                wrap_text(Fore.YELLOW + confirm + Style.RESET_ALL)

            elif delete_status == "Not read":
                confirm = f"The book \"{delete_title.title()}\" by {delete_author.title()} will be removed." \
                          + Fore.RED + f"\nThe book is {delete_status.lower()}." + Style.RESET_ALL
                wrap_text(Fore.YELLOW + confirm + Style.RESET_ALL)

            while True:
                are_you_sure = input(Fore.RED + "\nAre you sure you want to delete this book? Y/N: " + Style.RESET_ALL)
                if validate_yes_no(are_you_sure):

                    if "y" in are_you_sure or "Y" in are_you_sure:
                        LIBRARY.delete_rows(db_row)
                        clear_terminal()
                        print(Fore.YELLOW + "Removing book, please wait..." + Style.RESET_ALL)
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
            if how_many_books() is True:
                print(
                    Fore.YELLOW + "Not much of a choice, you have only one book, please select it...\n" + Style.RESET_ALL)
            elif how_many_books() is False:
                print(
                    Fore.RED + f"No such record! Please select #ID from 1 to {utils.utils.last_book_id}.\n" + Style.RESET_ALL)
            remove_book()

        break

def edit_book():
    """
    Allows user to edit all database values for each book such as:
    title, author, category, read status and description.
    """
    database_check()
    allowed_input = LIBRARY.col_values(1)[1:]

    while True:
        print(constants.EDIT_BOOK)
        show_all_books()
        user_choice = input(Fore.YELLOW + "\nWhich book would you like to edit?: " + Style.RESET_ALL)
        clear_terminal()

        if user_choice in allowed_input:

            db_row = int(user_choice) + 1
            book_id = LIBRARY.row_values(db_row)
            book_description = str(book_id[-1])
            book_no_desc = book_id[:-1]

            def print_edited_book():
                print(constants.EDIT_BOOK)
                print(constants.LINE)
                x = PrettyTable()
                x.field_names = constants.HEADERS_NO_DESC  # assigns table's headers from first row in DB
                x.align["Title"] = "l"  # align column to the left
                x.add_rows([book_no_desc])
                print(x)  # prints created table
                print(f"\n{constants.DESCRIPTION}: ")
                wrap_text(book_description)
                print(constants.LINE)

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
                user_choice = input(Fore.YELLOW + "What do you want to edit? Select 1-6: " + Style.RESET_ALL)
                validate_num_range(user_choice, 1, 6)
                # validate_input_range(user_choice, 1, 6)

                if user_choice == "1":
                    edit_cell = check_prefix()
                    validate_string(edit_cell)
                    book_no_desc[1] = edit_cell.title()
                    LIBRARY.update_cell(db_row, 2, edit_cell.title())
                    print(Fore.YELLOW + "Updating database..." + Style.RESET_ALL)
                    clear_terminal()
                    print(Fore.GREEN + f'Book title updated successfully to "{edit_cell.title()}".\n' + Style.RESET_ALL)
                    print(Fore.YELLOW + "Keep editing this book or return to main menu." + Style.RESET_ALL)

                elif user_choice == "2":
                    edit_cell = (input(Fore.YELLOW + "Please enter new author: " + Style.RESET_ALL)).title()
                    validate_string(edit_cell)
                    book_no_desc[2] = edit_cell.title()
                    LIBRARY.update_cell(db_row, 3, edit_cell)
                    clear_terminal()
                    print(
                        Fore.GREEN + f'Book author updated successfully to "{edit_cell.title()}".\n' + Style.RESET_ALL)
                    print(Fore.YELLOW + "Keep editing this book or return to main menu." + Style.RESET_ALL)

                elif user_choice == "3":
                    edit_cell = (input(Fore.YELLOW + "Please enter new category: " + Style.RESET_ALL))
                    validate_string(edit_cell)
                    book_no_desc[3] = edit_cell.capitalize()
                    LIBRARY.update_cell(db_row, 4, edit_cell)
                    clear_terminal()
                    print(
                        Fore.GREEN + f'Book category updated successfully to "{edit_cell.capitalize()}".\n' + Style.RESET_ALL)
                    print(Fore.YELLOW + "Keep editing this book or return to main menu." + Style.RESET_ALL)

                elif user_choice == "4":
                    while True:
                        edit_cell = input(
                            Fore.YELLOW + 'Please select "1" if book is READ and "2" if NOT READ: ' + Style.RESET_ALL)
                        if validate_num_range(edit_cell, 1, 2):
                            if edit_cell == "1":
                                edit_cell = "Read"
                                book_no_desc[4] = edit_cell
                                LIBRARY.update_cell(db_row, 5, edit_cell)
                                clear_terminal()
                                print(
                                    Fore.GREEN + f'Book status updated successfully to "{edit_cell.lower()}".\n' + Style.RESET_ALL)
                                print(Fore.YELLOW + "Keep editing this book or return to main menu." + Style.RESET_ALL)
                                break
                            elif edit_cell == "2":
                                edit_cell = "Not read"
                                book_no_desc[4] = edit_cell
                                LIBRARY.update_cell(db_row, 5, edit_cell)
                                clear_terminal()
                                print(
                                    Fore.GREEN + f'Book status updated successfully to "{edit_cell.lower()}".\n' + Style.RESET_ALL)
                                print(Fore.YELLOW + "Keep editing this book or return to main menu." + Style.RESET_ALL)
                                break
                        else:
                            clear_terminal()
                            print(Fore.RED + f"Wrong input, please try again...\n" + Style.RESET_ALL)

                elif user_choice == "5":
                    edit_cell = (input(Fore.YELLOW + "Please enter new description: " + Style.RESET_ALL)).capitalize()
                    validate_string(edit_cell)
                    LIBRARY.update_cell(db_row, 6, edit_cell)
                    book_description = edit_cell
                    clear_terminal()
                    print(Fore.GREEN + f"Book description updated successfully.\n" + Style.RESET_ALL)
                    print(Fore.YELLOW + "Keep editing this book or return." + Style.RESET_ALL)

                elif user_choice == "6":
                    clear_terminal()
                    show_all_books()  # returns to previous menu
                    break

        else:
            clear_terminal()
            if how_many_books() is True:
                print(
                    Fore.YELLOW + "Not much of a choice, you have only one book, please select it...\n" + Style.RESET_ALL)
            elif how_many_books() is False:
                print(
                    Fore.RED + f"No such record! Please select #ID from 1 to {utils.utils.last_book_id}.\n" + Style.RESET_ALL)

            edit_book()

        break


def change_sorting_method():
    """
    Changes sorting method
    """
    database_check()
    show_all_books()
    while True:
        print(
            Fore.YELLOW + f"Books are displayed in alphabetical order and sorted {default_sorting_method}." + Style.RESET_ALL)
        print(Fore.YELLOW + "How would you like to sort them?" + Style.RESET_ALL)
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
        user_choice = input(Fore.YELLOW + "Select 1 or 2: " + Style.RESET_ALL)
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
        user_choice = input(Fore.YELLOW + "\nWhich book details would you like to see?: " + Style.RESET_ALL)

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
                print(
                    Fore.YELLOW + "Not much of a choice, you have only one book, please select it...\n" + Style.RESET_ALL)
            elif how_many_books() is False:
                print(
                    Fore.RED + f"No such record! Please select #ID from 1 to {utils.utils.last_book_id}.\n" + Style.RESET_ALL)
            show_book_details()

        break


def quit_app():
    """
     This function prints goodbye message to the user
    """
    while True:
        random_quit_msg()
        are_you_sure = input(Fore.YELLOW + "\nAre you sure you want to quit? Y/N: " + Style.RESET_ALL)
        if validate_yes_no(are_you_sure):

            if "y" in are_you_sure or "Y" in are_you_sure:
                clear_terminal()
                print(Fore.YELLOW + f"Thank you for using {constants.APP} app!" + Style.RESET_ALL)
                print(constants.END_SCREEN)
                random_not_read()
                print(Fore.YELLOW + "\nTerminating..." + Style.RESET_ALL)
                break
            else:
                clear_terminal()
                menu.show_menu()

        else:
            clear_terminal()
            print(Fore.RED + "Wrong input, please select \"Y\" or \"N\"...\n" + Style.RESET_ALL)
            quit_app()

        break
