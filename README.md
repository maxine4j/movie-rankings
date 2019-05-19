# CITS3403-Project1-SocialChoice

Timothy Ings 21716194

# Purpose

Provide a platform for users to display their favourite movies and to create polls that other users can vote and comment on.

# Architecture

The application is a standard flask application. The entry point is `core.py` and it registers multiple blueprints that contain the rest of the application's views. The views can be found in the views directory. Each python file contains one or more routes that renders a template from the templates directory or handles an api call.

The files in the root of this project include setup and run scripts for both windows and mac/linux, pip requirements, and an sqlite3 database containing sample data. Additionally, the script as well as the names and base lorem ipsum used to generate said sample data is also included.

Directory Structure:

    |   data.db (Sample data)
    |   init_test_data.py (Script that generates sample data, requires themoviedb.org api key, see production branch on github for postgres version)
    |   lipsum.txt (Lorem ipsum text used to generate test sample data)
    |   names.json (Top 1000 boy/girl/last names, used to generate sample data)
    |   README.md
    |   requirements.txt (pip requirements file) 
    |   run.bat (Script to run the application on windows)
    |   run.sh (Script to run the application on mac/linux)
    |   setup.bat (Script to set up the applications environment on windows)
    |   setup.sh (Script to set up the applications environment on mac/linux)
    |  
    +---+ movie_rankings  
        |   auth.py (Contains functions that handle user authentication and session)
        |   core.py (Entry point for the application)
        |   data.py (Contains functions that access the database, see production branch on github for postgres version)
        |   movie_rankings.ini (uwsgi config file for production)
        |   wsgi.py (uwsgi entry point for production)
        |  
        +---+ static  
        |   +---+ css  
        |   |       main.css  
        |   |  
        |   +---+ img  
        |   |       avatar.png (Default user avatar image)
        |   |  
        |   +---+ js  
        |           admin.js (Contains admin functions)
        |           main.js  
        |  
        +---+ templates (Contains Jinja templates used in application views)
        |       admin.html
        |       base.html (Base template for all others)
        |       index.html  
        |       movie_card.html (Template that is included in other templates to represent a single movie)
        |       new_poll_modal.html  
        |       poll.html  
        |       polls.html  
        |       poll_card.html (Template that is included in other templates to represent a single poll)
        |       poll_comment_card.html (Template that is included in other templates to represent a single polls comments)
        |       profile_favourites.html  
        |       profile_header.html  
        |       profile_polls.html  
        |       rankings.html  
        |       search.html  
        |  
        +---+ views  
            |   admin.py
            |   api.py (Contains functions accessed via AJAX)
            |   index.py
            |   poll.py  
            |   profile.py  
            |   rankings.py  
            |   search.py  

# Setting up the application

- The application comes with a sample database. If you would like to generate your own, then you will need an api key from [The Movie DB](https://themoviedb.org). Set this as an environment variable `THEMOVIEDB_KEY` and run `init_test_data.py`. You can modify the variables at the top of the file to specify the generated characteristics of the data.

- The application is hosted at https://cits3403-p1.tim-ings.com with working facebook login. (Production site uses nginx, uwsgi, and postgres)

- If you want to be able to login when running the application locally, you will need to create a [facebook login application](https://developers.facebook.com/) and add an entry to your hosts file that redirects a real domain (such as dev.tim-ings.com) to 127.0.0.1. Ensure this domain is added to your facebook apps valid oauth redirect uris. Set environment variables `FACEBOOK_CLIENTID` and `FACEBOOK_SECRET` with those from your facebook app.

### Windows

1. Run `setup.bat`

## Mac/Linux

1. Run `setup.sh`

# Running the application

### Windows

1. Run `run.bat`

## Mac/Linux

1. Run `run.sh`
