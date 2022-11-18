"""
Utilities - functions used in addition to main
app functionalities e.g. for printing, sorting, clearing terminal,
validating inputs, generating random output.
"""

from api.google_sheets_api import LIBRARY, CONFIG
import os
import textwrap
import app_menu as menu
import constants
import random
from prettytable import PrettyTable
from scripts import functions
from colorama import Fore, Style

default_method = CONFIG.acell('B1').value  # either "by title" or "by author"
optional_method = CONFIG.acell('B2').value  # is always opposite value to default_method

# Initialize two values to store id's of first and las book.
# They are used later to determine valid input range and DB length.
first_book_id = ""
last_book_id = ""


def clear_terminal():
    """
    Clears terminal for better screen readability.
    Method found on StackOverflow:
    https://stackoverflow.com/questions/2084508/clear-terminal-in-python
    """
    os.system("cls" if os.name == "nt" else "clear")


def database_check():
    """
    Checks if database is not empty.
    If it's empty, user is asked to add his first book.
    Majority of app functionalities are disabled if DB is empty.
    """
    while True:
        is_empty = len(LIBRARY.row_values(2))  # checks if there is a record below DB headers
        if is_empty == 0:
            clear_terminal()
            print(Fore.LIGHTRED_EX + "Database is empty, add at least one book to continue." + Style.RESET_ALL)
            menu.show_menu()
            break

        break


def wrap_text(text):
    """
    The function uses textwrap library to wrap long strings
    over 79 characters to the new line. It's used to correctly display
    books descriptions and quotes on exit function.
    :param text - any string
    """
    wrapper = textwrap.TextWrapper(width=79)
    wrapped_text = wrapper.fill(text=text)
    print(wrapped_text)


def how_many_books():
    """
    Checks if there is one or more books in the database.
    It's used in edit_book, remove_book, and show_book_details functions
    to conditionally give user hint on possible input selection.
    E.g - "Select the only book" or "Select book 1-10".
    :return: first_book_id
    :return: last_book_id
    :return: True if there's only one book in DB
    :return: False if there's more than one book in DB
    """
    all_books = LIBRARY.col_values(1)[1:]  # list of IDs of all books
    global first_book_id
    global last_book_id

    if len(all_books) == 1:
        return True
    elif len(all_books) > 1:
        first_book_id = all_books[0]
        last_book_id = all_books[-1]
        return False

    return first_book_id, last_book_id


def check_title_prefix(text):
    """
    Checks if title starts with prefix "the" and converts it to format "Title, The"
    :return: title
    """
    text = text.lower()

    if text.startswith("the "):
        prefix = ", The"
        rewrite_title = text[4:]  # slice of a string - remove first 4 char "the ".
        new_title = rewrite_title + prefix
        title = new_title.title()
        print(Fore.LIGHTYELLOW_EX + "Converted to: ", title + Style.RESET_ALL)
    else:
        title = text.title()

    return title


def validate_num_range(user_input, first_val, last_val):  # e. g use in main menu, allowed options 1-7
    """
    Checks if user input is withing the range of possible options.
    Any input out of desired range will give user a hint showing
    a message containing exact range of possible options.
    :param user_input: this is user input
    :param first_val: this is first option from the range of options
    :param last_val:  this is the last option from the range of options
    :returns True if user's input is valid
    :returns False if user's input is invalid
    """
    try:
        options = list(range(first_val, last_val + 1))
        allowed_options = [str(i) for i in options]

        if user_input in allowed_options:
            return True
        else:
            raise ValueError
    except ValueError:
        clear_terminal()
        print(Fore.LIGHTRED_EX +
              f"\nWrong input, please select option from {first_val} to {last_val} "
              f"to continue..." + Style.RESET_ALL)


def validate_yes_no(user_input):
    """
    Validates Y/N inputs.
    Prints user feedback if input is invalid.
    :param user_input - contains user choice
    :return True if valid input is given
    """
    try:
        valid_options = ["y", "Y", "n", "N"]
        if user_input in valid_options:
            return True
        else:
            raise ValueError
    except ValueError:
        clear_terminal()
        print(Fore.LIGHTRED_EX + "\nWong input, please select \"Y\" or \"N\".\n" + Style.RESET_ALL)


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !This one is to be finished, not working as expected!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def validate_string(user_text, max_length, element):
    """
    TO BE CHANGED
    :param element: is variable assigned to user input, e.g. title, author
    :param user_text contains prompt to enter text
    :param max_length - max characters in string
    """
    #
    # NEED TO FIX THIS VALIDATION - IT SHOULD ASK FOR INPUT AGAIN if invalid input given
    #
    while True:
        user_input = input(user_text)
        # checks if input is empty
        if len(user_input) == 0:
            clear_terminal()
            print(Fore.LIGHTRED_EX + f"{element.capitalize()} can't be empty!" + Style.RESET_ALL)
        # checks if first character of the string is not special character
        elif not user_input[0].isalnum():
            print(Fore.LIGHTRED_EX + f"{element.capitalize()} has to start with letter or digit!"
                                   + Style.RESET_ALL)
        # checks if input is shorter than required 3 characters
        elif len(user_input) <= 2:
            clear_terminal()
            print(Fore.LIGHTRED_EX + "Please enter at least 3 characters..." + Style.RESET_ALL)
        # checks if input is longer than maximum allowed
        elif len(user_input) > int(max_length):
            clear_terminal()
            print(
                Fore.LIGHTRED_EX + f"Entered {element} exceeds maximum allowed length of {max_length} characters!"
                + Style.RESET_ALL)
        else:
            element = user_input.title()
            return element


def print_all_database():
    """
    Gets all values from the database and prints them
    to the terminal in a form of table generated with
    PrettyTable library.
    Maximum width of whole table is set to 79 characters.
    Each column's maximum width is set individually.
    """
    x = PrettyTable()
    x.field_names = constants.HEADERS_NO_DESC
    x._max_table_width = 79  # max width of whole table
    x._max_width = {"ID": 2, "Title": 24, "Author": 18, "Category": 12, "Status": 8}  # columns max width
    x.field_names = constants.HEADERS_NO_DESC
    x.align["ID"] = "r"  # aligns column to the right
    x.align["Title"] = "l"  # aligns column to the left
    x.align["Author"] = "l"
    x.align["Category"] = "l"
    x.align["Status"] = "l"
    all_values = LIBRARY.get_all_values()  # gets all values from DB
    all_values_no_headers = all_values[1:]  # all values without the first row (db headers)
    for i in all_values_no_headers:
        x.add_rows(
            [i[:-1]]  # each iteration adds a row to the table, skips the headers
        )
    print(x)


def renumber_id_column():
    """
    Renumber values in column 1 in the worksheet
    to keep ID values in order when book is added or removed.
    """
    col = LIBRARY.col_values(1)  # assigns values from column 1
    new_col = col[1:]  # slices out the headers
    id_val = 1  # allows to start ID values from 1
    row_val = 2  # allows to start iteration from row 2

    for _ in new_col:  # underline used to avoid using variable without later need
        LIBRARY.update_acell("A" + str(row_val), id_val)  # renumbering ID value to keep order
        id_val += 1
        row_val += 1
    print(Fore.LIGHTYELLOW_EX + "Updating database..." + Style.RESET_ALL)  # feedback to the user


def sort_books(col, order):
    """
    Sorts database records alphabetically.
    Gspread allows to sort in two ways - ascending or descending order.
    :param col - number of the column in Google Sheets
    :param order - can be chosen "asc", or "des"
    """
    LIBRARY.sort((col, order))  # sorts values in worksheet LIBRARY


def sort(sorting_order):
    """
    Sorts entries in the database in alphabetical order (default).
    Function can be called by the user in "Change sorting method" menu.
    User can opt for method "by title" or by "author".
    Function is used automatically by the app to sort books
    each time entry is added or deleted to keep proper order in the database.
    Automatic sorting is always set to method opposite to default. T
    That prevents from long waiting for app response when starting program.
    :param sorting_order: is variable that gets value from CONFIG worksheet
    """
    global default_method
    global optional_method
    if sorting_order == default_method:
        pass
    elif sorting_order == optional_method:
        if default_method == "by author":
            print(Fore.LIGHTYELLOW_EX + "Sorting database by title. Please wait..." + Style.RESET_ALL)
            CONFIG.update_acell("B1", "by title")  # write method to database
            CONFIG.update_acell("B2", "by author")  # write method to database
            functions.default_sorting_method = "by title"  # changing value so can be updated in functions.py
            functions.optional_sorting_method = "by author"  # changing value so can be updated in functions.py
            default_method = "by title"
            optional_method = "by author"
            sort_books(2, "asc")  # sorts by column 2 in alphabetical order
            renumber_id_column()  # reassigns ID values to keep order after sorting
        elif default_method == "by title":
            print(Fore.LIGHTYELLOW_EX + "Sorting database by author. Please wait..." + Style.RESET_ALL)
            CONFIG.update_acell("B1", "by author")  # writing method to database
            CONFIG.update_acell("B2", "by title")  # writing method to database
            functions.default_sorting_method = "by author"  # changing value so can be updated in functions.py
            functions.optional_sorting_method = "by title"  # changing value so can be updated in functions.py
            default_method = "by author"
            optional_method = "by title"
            sort_books(3, "asc")  # sorts by column 3 in alphabetical order
            renumber_id_column()  # reassigns ID values to keep order after sorting


def random_not_read():
    """
    Generates random book title from the database
    and prints it to the user as next read suggestion.
    Works only if there's at least one book with
    status "Not read" in the database.
    It also checks if book title contains suffix "the"
    and converts the title accordingly,
    opposite to check_prefix function.
    """
    all_books = LIBRARY.get_all_values()[1:]  # all books without db headers
    not_read = []

    # iterates through column 4 - "Status" to find all books that are "Not read"
    for book in all_books:
        if "Not read" in book[4]:
            not_read.append(book)  # creates of all books with status "Not read"

    if len(not_read) > 0:
        random_book = random.choice(not_read)  # picks random book
        suffix = ", The"
        prefix = "The "
        title = random_book[1]  # extracts title

        # conditional below checks if in book adding process title
        # containing prefix "the" was converted.
        # it's opposite function to check_prefix():
        if suffix in title:
            short = title[:-5]  # a title without last 5 characters
            new_title = prefix + short
            title = new_title

        print(Fore.LIGHTGREEN_EX + "Looking for your next read?" + Style.RESET_ALL)
        wrap_text(Fore.LIGHTGREEN_EX + f"Why don't you grab \"{title}\" by {random_book[2]}. "
                                       f"It's still not read." + Style.RESET_ALL)


def random_quit_msg():
    """
    Generates random quote from all quotes
    and prints it as quit_message.
    Output is wrapped not to exceed 79 characters in line.
    Quotes found on www.goodreads.com
    """
    quit_messages = [
        '"So many books, so little time..." - Frank Zappa',
        '"A room without books is like a body without a soul" - Cicero',
        '"There is no friend as loyal as a book" - Ernest Hemingway',
        '"A reader lives a thousand lives before he dies, said Jojen.\n'
        'The man who never reads lives only one" - George R.R. Martin, A Dance with Dragons',
        '"The best books... are those that tell you what you know already" - George Orwell, 1984',
        '"Life is too short to read books that I\'m not enjoying" - Melissa Marr',
        '"Books are a uniquely portable magic" - Stephen King'
    ]

    random_msg = random.choice(quit_messages)
    wrap_text(Fore.LIGHTGREEN_EX + random_msg + Style.RESET_ALL)


def copy_demo_worksheet():
    print("test")
    # get all values from DEMO --> insert to LIBRARY
    # find last row in library ---- > clear all up to last line ---> insert all from DEMO sheet.
