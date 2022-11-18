<h1 align="center">Home Library App - Python Project</h1>

### Developer: Aleksander Kisielewicz

<b>[View live program here](https://home-library-app-ci.herokuapp.com/)</b> :computer:

![Program mockup](docs/img/app_mockup.png)

The Home Library App was created as Portfolio Project #3 (Python Essentials) for Diploma in Full Stack Software Development at [Code Institute](https://www.codeinstitute.net). It allows users to manage their personal book libraries, view, add, edit, and remove books.

Project purpose was to build a command-line python application that allows user to manage a common dataset about a particular domain.


# Table of content

*   [Project](#project)
    *   [Strategy/Scope](#strategyscope)
    *   [Site owner goals](#site-owner-goals)
    *   [External user's goal](#external-users-goal)
*   [Logic and features](#logic-and-features)
    *   [Python logic](#python-logic)
    *   [Database structure](#database-structure)
    *   [Features](#features)
*   [User Experience (UX/UI)](#user-experience-ux)
    *   [Colour Scheme](#colour-scheme)
*   [Technology](#technology)
    *   [Frameworks, libraries & software used](#languages-used)
    *   [Python libraries/modules](#python-librariesmodules)
*   [Testing](#testing)
    *   [Accessibility](#accessibility)
    *   [Validation](#validation)
*   [Deployment](#deployment)
*   [Credits](#credits)
    *   [Code](#code)
    *   [Media](#media)
    *   [Acknowledgements](#acknowledgements)



#   Project
##  Strategy/Scope

I chose to develop an application that can be used in real life. Home Library allows users to manage their personal book libraries. Application contains such functionalities as: viewing book database, adding/editing and removing books. User can display details of every database entry and also sort database in chosen order.

Application should have clean and intuitive user interface and offer easy access and navigation to all functionalities.

To achieve the strategy goals I implemented following features:

- clean user interface for easy navigation and readability
- menu with easy acces to all features and possibility to exit program
- colours in terminal to give user feedback depends on his actions
- reliable and quick connection with database provided by Google
- customised terminal display page for better visual experience

## Site owner goals

As a program owner/developer I would like to:
- create application that has real life usage 
- create application that is easy to use and intuitive to navigate
- create application with clean, good looking and accesible interface
- provide user a feedback to every input and action
- decide what kind of user input is allowed and valid
- create bugs free application

##  External user's goal

As a user I would like to:
- be able to clearly understand application's purpose
- be able to use program with real usability
- be able to easily navigate the program and access all features
- be able to receive feedback to actions taken
- be able to decide what to do next, what features to use
- be able to quit program at all stages
- avoid any errors/bugs 

# Logic and features

## Python Logic

A flow diagram of the logic behind the application was created using [Lucid Chart](https://www.lucidchart.com/).

![Flow diagram](docs/img//home_library_app.png)
For PDF version [click here](docs/flow_diagram.pdf)

## Database structure

## Features

Add book


Edit book

Remove book

View all books

Change sorting method

Show book details

Quit


#   User Experience (UX)
##  Colour Scheme

Colour palette was selected using <b>coolors.co</b> generator and has been extracted from the backgroud picture used in terminal view HTML page. Colour of the "run program" button was adjusted to match the backgroud.

![Colour Scheme](docs/img/palette.jpg)

Terminal outputs are displayed in high-contrast colours over black background for better readability and accesibillity. Standard prompts are yellow, book addition and edit inputs are blue, warnings red. Confirmation messages and menus are green. Bigger chunks of data coming from the database are printed in standard white colour to be non-distractive.

Screenshots presenting terminal and colour outputs are available in [Features](#features) section.

#   Technology
    
##  Languages used

-   [Python](https://www.python.org/) - high-level, general-purpose programming language.
-   [Markdown](https://en.wikipedia.org/wiki/Markdown) - markup language used to write README document.

##  Frameworks, software used

- [Coolors.co](https://coolors.co/) - was used to create colour palette for terminal display page.

- [Font Awesome:](https://fontawesome.com/) - Font Awesome icons were used for social links in terminal display page.

- [Git](https://git-scm.com/) - Git was used for version control by utilizing the Gitpod terminal to commit to Git and Push to GitHub.

- [GitHub](https://github.com/) - GitHub is used to store the project's code after being pushed from Git.

- [Google Sheets API](https://developers.google.com/sheets/api) - was used to connect with the database made of the spreadsheet.

- [Favicon.io](https://www.favicon.io) - tool used to create favicon.

- [LucidChart](https://www.lucidchart.com/pages) - was used to create flow diagram.

- [Pexels.com](https://www.pexels.com/) - was used to source bacground picture for terminal display page.

- [PyCharm](https://www.jetbrains.com/pycharm/) - Python IDE used to write the app.

- [Text ASCII Art Generator](http://patorjk.com/software/taag/) - used to create app logo in ASCII format.

##  Python libraries/modules

- [gspread](https://docs.gspread.org/) - python API for Google Sheets.

- [OAuthLib](https://pypi.org/project/oauthlib/) - required to manage HTTP request and authenticate to Google Sheets API.

- [PrettyTable](https://pypi.org/project/prettytable/) - python library for easily displaying tabular data in a visually appealing ASCII table format

- [colorama](https://pypi.org/project/colorama/) - used to color terminal outputs.

- [os](https://docs.python.org/3/library/os.html) - built-in pythod module - used to write clear_terminal function.

- [textwrap](https://docs.python.org/3/library/textwrap.html) - built-in python module - used to wrap lines over 79 char to next line e.g. long book description. 

- [random](https://docs.python.org/3/library/random.html) - built-in python module - used to generate random quote on exit screen.


#    Testing

##   Accessibility




## Validation

### PEB8



##   Bugs/known issues

- <b>Issue #1:</b> During the edit I made indentation error and misplaced last "break" instruction of the code presented on screenshot below. That caused infinite loop to work in the backgroud without any terminal output. It was a major issue as all main program features generated an Google Sheets API error code 429 - "To many requests HTTP status code response". I thought that I exceeded Google Sheets Quoata per user/per minute/per project but after checking logs and quotas in Google Cloud Console I knew that something else caused an error. I finally managed to find the mistake. It wasn't obvious as function was meant to work "in the bacground" without any terminal output as long as there are records in database. Database wasn't ampty at that time so the message hasn't been shown.

![bug1](docs/img/bug1.png)


<b>Solution:</b> Putting "break" instruction in the correct place, that allows to quit the while loop. 


#   Deployment

PLACEHOLDER

<br>

#   Credits

##  Code

- Google Sheets API connection method is taken from Love Sandwiches CI Project and gspread documentation - in /api/google_sheets_api.py - [line 10-19](https://github.com/alexkisielewicz/home-library-app/blob/dac2a1c42d48e5b81d5fb6c0788b1f3f116317d2/api/google_sheets_api.py#L10)
- [Stack Overflow](https://stackoverflow.com/questions/2084508/clear-terminal-in-python) - method used to write clear_terminal function in /utils/utils.py - [line 26-32](https://github.com/alexkisielewicz/home-library-app/blob/dac2a1c42d48e5b81d5fb6c0788b1f3f116317d2/utils/utils.py#L26)

##  Media


- [Goodreads.com](https://www.goodreads.com/) - the source of the quotes used on app exit screen.
- [Pexels.com](https://www.pexels.com) - the source of the terminal page background picture.
- [Text ASCII Art Generator](http://patorjk.com/software/taag/) - used to create app logo in ASCII format. 

## Learning resources

- [Code Institute course and learning platform](https://codeinstitute.net/)
- [The book "Python Crash Course, 2nd Edition: A Hands-On, Project-Based Introduction To Programming"](https://nostarch.com/pythoncrashcourse2e)
- [StackOverflow](https://stackoverflow.com/)
- [W3Schools](https://www.w3schools.com/python/default.asp)
- [Google Sheets API documentation](https://developers.google.com/sheets/api/quickstart/python)
- [Gspread documentation](https://docs.gspread.org/en/v5.7.0/)

##  Acknowledgements

-   My Mentor Reuben Ferrante for helpful feedback and guidance at all stages of the project. 
-   Code Institute Slack Community for being invaluable knowledge base.

## Disclaimer
-   Home Library app was created for educational purpose only. 