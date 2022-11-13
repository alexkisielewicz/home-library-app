"""
Constants used throughout the app
"""
from api.google_sheets_api import *
from colorama import Fore, Style

# app constants

HEADERS = LIBRARY.row_values(1)
HEADERS_NO_DESC = HEADERS[:-1]
HEADERS_NO_DESC_NO_ID = HEADERS[:-1]
DESCRIPTION = LIBRARY.row_values(1).pop()
ALL_VALUES = LIBRARY.get_all_values()
ALL_VALUES_NO_HEADER = ALL_VALUES[1:]
APP = "Home Library"
LINE = Fore.YELLOW + "###############################################################################" + Style.RESET_ALL  # 79 characters long

# descriptions of the functionalities
ADD_BOOK = """
Now you can add a new book to your library. \n
You will be asked to enter book title, author, category and short description.
Choose if you have read the book or not. Book ID is generated automatically. 
"""

EDIT_BOOK = Fore.YELLOW + "Here you can update all book details.\n" + Style.RESET_ALL

REMOVE_BOOK = Fore.YELLOW + "Here you can remove selected book from the database.\n" + Style.RESET_ALL

VIEW_ALL_BOOKS = Fore.YELLOW + f"This is the list of all your books." + Style.RESET_ALL

SHOW_BOOK_DETAILS = Fore.YELLOW + "This is detailed view of the book entry." + Style.RESET_ALL

END_SCREEN = Fore.YELLOW + """
It was developed by Aleksander Kisielewicz 
for Diploma in Full Stack Software Development 
at Code Institute.

Visit my profiles: 
https://github.com/alexkisielewicz
https://www.linkedin.com/in/alekkisielewicz/
""" + Style.RESET_ALL
