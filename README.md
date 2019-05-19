# Web Application Project: Social Choice

Due 12pm, May 20, 2019

This project is worth 30% of your final grade in the unit must be done in pairs.

## Project Description

For this project you are required to build a multi-user web application. The application should be written using HTML, CSS, Flask, AJAX, JQuery, and Bootstrap. The application should perform some kind of voting or ranking activity (social choice), based on the inputs from users. The context and the type of social choice mechanism is up to you.

Example contexts you could use are:

- Music/Movie Polls (e.g. find the best anime movie of the 21st century)
- Ranking recipes (e.g. find the best lassangne recipe on the web).
- Find the best units at UWA.

The types of social choice mechanism you could use are

- First past the post voting
- Preferential voting
- Elo rankings (as used in chess leaderboards)
- Page rank type graph algorithms

The web application should be styled to be interesting and engaging for a user in the selected context. It should offer several views including:

1. An adminstrator view, that can add and delete polls, delete responses, and add and delete users.
2. A user view that can view polls and current standings, and submit responses to polls.
3. A general view that can just view polls

In addition to the web application, you should create a private GitHub project that includes a readme describing

<<<<<<< HEAD
1. the purpose of the web application, explaining both the context and the social choice mechanism used.
2. the architecture of the web application
3. describe how to launch the web application.
4. describe some unit tests for the web application, and how to run them.
5. Include commit logs, showing contributions and review from both contributing students
=======
- Displays a list of movies sorted by popularity according to our data supplier, https://themoviedb.org

- Click the 'Add to favourites' button at the bottom of a movie card to add that movie to your favourites and push it up the rankings.

#### Rankings

- Displays a table containing the most favourited movies by our site's users.

#### Polls

- Displays currently active, user created polls.

- Clicking the name of a movie will cast your vote in that poll.

- Clicking on a poll's title will take you to its page which contains user comments.

- Clicking on a user's name will take you to their profile.

#### User Profile

- Displays a user's favourited movies.

- Displays polls created by the target user.

- Click the 'Favourites' and 'Polls' buttons in the bottom right of the profile header to change views.

#### Search

- Searches all movies on the site

#### New Poll

- Allows a user to create a poll that other users can vote and comment on

- Click the 'New Poll' button to open the new poll modal

- Enter a title and description

- Click the 'Add Choice' button to add a choice to your poll

- Search for the movie you want to add.


# Administrator access

- To access administrator functions, ensure that you have logged in with facebook, navigate to https://cits3403-p1.tim-ings.com/admin and click the grant button. This admin grant function would not exist or only be available to existing admins on a real website.

- Doing this enables new buttons on things like polls and comments that allows you to remove them.

# Setting up the application

- The application comes with a sample database. If you would like to generate your own, then you will need an api key from [The Movie DB](https://themoviedb.org). Set this as an environment variable `THEMOVIEDB_KEY` and run `init_test_data.py`. You can modify the variables at the top of the file to specify the characteristics of the generated data.

- The application is hosted at https://cits3403-p1.tim-ings.com with working facebook login. (Production site uses nginx, uwsgi, and postgres)

- If you want to be able to login when running the application locally, you will need to create a [facebook login application](https://developers.facebook.com/) and add an entry to your hosts file that redirects a real domain (such as dev.tim-ings.com) to 127.0.0.1. Ensure this domain is added to your facebook apps valid oauth redirect uris. Set environment variables `FACEBOOK_CLIENTID` and `FACEBOOK_SECRET` with those from your facebook app.

##### Windows

1. Run `setup.bat`

##### Mac/Linux

1. Run `setup.sh`

# Running the application

- You may need to run the application with admin/sudo if it cannot bind to port 443. Running on port 443 is required to get local facebook login working with the hosts file trick. If you would like to run the application without facebook login, than you can change the port (and disable adhoc ssl too) in `movie_rankings/core.py` line 37.

##### Windows

1. Run `run.bat`

##### Mac/Linux

1. Run `run.sh`
>>>>>>> 9351177... Merge branch 'master' of https://github.com/Arwic/CITS3403-Project1-SocialChoice
