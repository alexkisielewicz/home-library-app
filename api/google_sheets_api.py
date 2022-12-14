"""
Google Sheets API connection and its constants
"""

import gspread
from google.oauth2.service_account import Credentials

# API connected as per gspread documentation
# and Love Sandwiches Code Institute Project.
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

# creds.json is added to .gitignore
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('home-library')

# Two worksheets that are used by the app
LIBRARY = SHEET.worksheet('library')  # database WS with all books
CONFIG = SHEET.worksheet('config')  # config WS to read/write DB sorting method
