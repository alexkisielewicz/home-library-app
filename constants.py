"""
Constants used throughout the app
"""

from api.google_sheets_api import *
from colorama import Fore, Style

# App constants
HEADERS = LIBRARY.row_values(1)
HEADERS_NO_DESC = HEADERS[:-1]
HEADERS_NO_DESC_NO_ID = HEADERS[:-1]
DESCRIPTION = LIBRARY.row_values(1).pop()
ALL_VALUES = LIBRARY.get_all_values()
ALL_VALUES_NO_HEADER = ALL_VALUES[1:]
APP = "Home Library App"

# PrettyTable columns width
MAX_LEN = {"ID": 2, "Title": 24, "Author": 18, "Category": 12, "Status": 8}
# PrettyTable table width
TABLE_MAX_LEN = 79
# Book details max length for validation of inputs
ID_MAX_LEN = MAX_LEN["ID"]
TITLE_MAX_LEN = MAX_LEN["Title"]
AUTHOR_MAX_LEN = MAX_LEN["Author"]
CAT_MAX_LEN = MAX_LEN["Category"]
# description below assigned individually, it is displayed outside the PrettyTable tab.
DESC_MAX_LEN = 200
# Separator line
LINE = Fore.YELLOW + "#"*TABLE_MAX_LEN + Style.RESET_ALL  # 79 characters long
# Reading status
READ_YES = "Read"
READ_NO = "Not read"

# Descriptions of the functionalities
ADD_BOOK = Fore.LIGHTYELLOW_EX + """
Now you can add a new book to your library. \n
You will be asked to enter book title, author, category and short description.
Choose if you have read the book or not. Book ID is generated automatically. 
""" + Style.RESET_ALL

EDIT_BOOK = Fore.LIGHTYELLOW_EX + "You can update all book details below." + Style.RESET_ALL

REMOVE_BOOK = Fore.LIGHTYELLOW_EX + "Here you can remove selected book from the database." + Style.RESET_ALL

VIEW_ALL_BOOKS = Fore.LIGHTYELLOW_EX + f"This is the list of all your books." + Style.RESET_ALL

SHOW_BOOK_DETAILS = Fore.LIGHTYELLOW_EX + "This is detailed view of the book entry." + Style.RESET_ALL

END_SCREEN = Fore.LIGHTYELLOW_EX + """
It was developed by Aleksander Kisielewicz 
for Diploma in Full Stack Software Development 
at Code Institute.

Visit my profiles: 
https://github.com/alexkisielewicz
https://www.linkedin.com/in/alekkisielewicz/
""" + Style.RESET_ALL
