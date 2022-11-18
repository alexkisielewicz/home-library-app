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

CREDS = Credentials.from_service_account_file('creds.json')  # added to .gitignore
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('home-library')

# Two worksheets that are used by the app
LIBRARY = SHEET.worksheet('library')  # database worksheet with all books
CONFIG = SHEET.worksheet('config')  # config worksheet to read/write DB sorting method
