"""
Constants used throughout the app
"""
from api.google_sheets_api import *

# app constants

HEADERS = LIBRARY.row_values(1)
HEADERS_NO_DESC = HEADERS[:-1]
HEADERS_NO_DESC_NO_ID = HEADERS[:-1]
DESCRIPTION = LIBRARY.row_values(1).pop()
ALL_VALUES = LIBRARY.get_all_values()
ALL_VALUES_NO_HEADER = ALL_VALUES[1:]
APP = "Home Library"
LINE = "###############################################################################"  # 79 characters long
