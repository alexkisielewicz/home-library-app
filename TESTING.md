# Manual testing of validation and functionalities

Reasonable amount of manual testing was done to check all inputs and features. <br>
Minor spelling and typo errors were fixed during the development.


# Main menu
Function used for inputs validation - validate_num_range in utils/utils.py

| What is being tested | Input  | Expected response | Result  |
|---|---|---|---|
|  Please select a number from 1 to 7 to continue | "8", "asd", "empty"   |Wrong input | Pass
|  Please select a number from 1 to 7 to continue | "1" | Valid input, call add_book fn | Pass
|  Please select a number from 1 to 7 to continue | "2" | Valid input, call edit_book fn | Pass
|  Please select a number from 1 to 7 to continue | "3" | Valid input, call remove_book fn | Pass
|  Please select a number from 1 to 7 to continue | "4" | Valid input, call show_all_books fn  | Pass
|  Please select a number from 1 to 7 to continue | "5" | Valid input, call change_sorting_method fn | Pass
|  Please select a number from 1 to 7 to continue | "6" | Valid input, call show_book_details fn | Pass
|  Please select a number from 1 to 7 to continue | "7" | Valid input, call quit fn | Pass
|  Please select a number from 1 to 7 to continue | "2" (database is empty)| Valid input, prompt user to add first book | Pass
Please select a number from 1 to 7 to continue | "3" (database is empty)| Valid input, prompt user to add first book | Pass
Please select a number from 1 to 7 to continue | "4" (database is empty)| Valid input, prompt user to add first book | Pass
Please select a number from 1 to 7 to continue | "5" (database is empty)| Valid input, prompt user to add first book | Pass
Please select a number from 1 to 7 to continue | "6" (database is empty)| Valid input, prompt user to add first book | Pass

# Add book function
Function used - validate_string() in utils/utils.py<br>
The same function is used to validate book's author, category and description.

|  What is being tested  | Input  | Expected response  | Result
|---|---|---|---|
|  Please enter book's title | "a"  | Input too short  | Pass
|  Please enter book's title | "ad"  | Input too short  | Pass
|  Please enter book's title | empty  | Input can't be empty  | Pass
|  Please enter book's title | "!title"  | Input can't start with special char.  | Pass
|  Please enter book's title | "This is a title of a long book"  | Input exceeded 24 characters  | pass
|  Please enter book's title | "1984"  | Valid input  | Pass
|  Please enter book's title | "the title"  | Valid input, convert title to "Title, The"  | Pass
|  Please select "1" if you read that book or "2 if you didn't | "3"  | Wrong input  | Pass
|  Please select "1" if you read that book or "2 if you didn't | empty  | Wrong input  | Pass
|  Please select "1" if you read that book or "2 if you didn't | "!"  | Wrong input  | Pass


# Yes/No question
Function used for inputs validation - validate_yes_no() in utils/utils.py

|  What is being tested  | Input  | Expected response  | Result
|---|---|---|---|
|  Confirm adding this book. Y/N | "0", "3", "f", empty  | Wrong input  | Pass
|  Confirm adding this book. Y/N |  "y", "Y" | Valid input, proceed | Pass
|  Confirm adding this book. Y/N |  "n", "N" | Valid input, abort  | Pass



# Edit book function

|  What is being tested  | Input  | Expected response  | Result
|---|---|---|---|
|  Wchich book would you like to edit? | "6" (5 records exist)  | Wrong input, please select ID from 1 to 5  | Pass
|  Wchich book would you like to edit? | "g", empty (5 records exist)  | Wrong input, please select ID from 1 to 5  | Pass
|  Wchich book would you like to edit? | "5" (5 records exist )  | Input valid, show book #5  | Pass
|  What do you want to edit? Select 1-6 | "0", "a", "`", empty (6 possible choices )  | Wrong input | Pass
|  What do you want to edit? Select 1-6 | "7" (6 possible choices )  | Wrong input | Pass
|  Please update book's title | "the da vincii code" | Valid input, convert title to "Da Vincii Code, The" | Pass

The same validation method is used for input of author, title, category, status and description for both "add book" and "edit book" features.


# Remove book function

|  What is being tested  | Input  | Expected response  | Result
|---|---|---|---|
|  Please select a book to remove (#ID) | "6" (5 records exist) | Wrong input - unexpected line break in terminal output  | Fail (issue#2 in README) ![test_fail](docs/img/bug2.png)
|  Please select a book to remove (#ID) | "0", "k", empty (5 records exist) | Wrong input | Pass
|  Are you sure you want to delete this book? Y/N | "0", "b", empty | Wrong input | Pass
|  Are you sure you want to delete this book? Y/N | "n" | Valid input, return | Pass
|  Are you sure you want to delete this book? Y/N | "Y" | Valid input, remove book | Pass


# Change sorting method function
Function used for inputs validation - validate_num_range in utils/utils.py


|  What is being tested  | Input  | Expected response  | Result
|---|---|---|---|
|  Select 1 or 2 | "1" (sorting by autor is set to default)  | Valid input, sort by title  | Pass
|  Select 1 or 2 | "1" (sorting by title is set to default)  | Valid input, sort by author  | Pass
|  Select 1 or 2 | "2" (sorting by title is set to default)  | Valid input, return  | Pass
|  Select 1 or 2 | "3", "0", "a", empty (sorting by autor is set to default)  | Wrong input | Pass

# Show book details function
Function used for inputs validation - validate_num_range in utils/utils.py

|  What is being tested  | Input  | Expected response  | Result
|---|---|---|---|
| Which book details would you like to see? | "6" (5 records exist)  | Wrong input  | Pass
| Which book details would you like to see? | "5"  | Valid input, show book details  | Pass
| Which book details would you like to see? | "asd", "!"  | Wrong input  | Pass
| Which book details would you like to see? | "2", (1 record exists)  | Valid input, prompt user to select the only entry available  | Pass

# Quit function

|  What is being tested  | Input  | Expected response  | Result
|---|---|---|---|
| Correctly display random quote on exit screen? | N/A  | Random quote printed to the terminal  | Pass
| Are you sure you want to quit? | "n"  | Valid input, retur  | Pass
| Are you sure you want to quit? | "0", "!", empty | Wrong input | Pass
| Are you sure you want to quit? | "y"  | Valid input, terminate program  | Pass
| Correctly display random next read suggestion? | N/A  | Random next read suggestion printed to the terminal  | Pass