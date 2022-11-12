from prettytable import PrettyTable

from api.google_sheets_api import LIBRARY, CONFIG
import os
from scripts import functions
import app_menu as menu
import constants

def clear_terminal():
    """
    Clears terminal for better screen readability
    """
    os.system("cls" if os.name == "nt" else "clear")
    print("terminal cleared!")
    print('\n' * 20)  # prints 20 line breaks to simulate CLS in PyCHarm IDE


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