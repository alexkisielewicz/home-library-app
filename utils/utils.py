from api.google_sheets_api import LIBRARY, CONFIG
import os
import textwrap
import app_menu as menu
import constants
import random
from prettytable import PrettyTable
from scripts import functions

def clear_terminal():
    """
    Clears terminal for better screen readability
    """
    os.system("cls" if os.name == "nt" else "clear")
    print("terminal cleared!")
    print('\n' * 20)  # prints 20 line breaks to simulate CLS in PyCHarm IDE


def database_check():
    while True:
        is_empty = len(LIBRARY.row_values(2))  # checks if there is a record below DB headers
        if is_empty == 0:
            clear_terminal()
            print("Database is empty, add at least one book to continue.")
            menu.show_menu()
            break
        else:
            break


def print_all_database():
    """
    Gets all values from the database and prints to the terminal
    all records in table easy to read.
    """
    x = PrettyTable()
    x.field_names = constants.HEADERS_NO_DESC
    x.align["ID"] = "r"  # aligns column to the right
    x.align["Title"] = "l"  # aligns column to the left
    x.align["Author"] = "l"
    x.align["Category"] = "l"
    x.align["Status"] = "l"
    all_values = LIBRARY.get_all_values()  # gets all values from DB
    all_values_no_headers = all_values[1:]  # all values without the first row
    for i in all_values_no_headers:
        x.add_rows(
            [i[:-1]]  # each iteration adds a row to the table, we skip the header
        )
    print(x)


def renumber_id_column():
    """
    Renames values in column A in the worksheet to keep ID values in order when book is removed
    """
    col = LIBRARY.col_values(1)
    new_col = col[1:]
    id_val = 1
    row_val = 2

    for _ in new_col:
        LIBRARY.update_acell("A" + str(row_val), id_val)  # renumbering ID value to keep order
        id_val += 1
        row_val += 1
    print("Updating database...")