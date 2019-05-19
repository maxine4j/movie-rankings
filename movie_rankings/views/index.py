import flask
import data
import auth


app_index = flask.Blueprint('app_index', __name__)


@app_index.route('/')
def view_index():
    # prompt the user to log in with facebook oauth2
    auth.try_login_user()
    # get movie db popular movies
    movies = data.get_popular_movies(auth.current_user_id())
    all_movies = data.get_all_movies()
    # render the index template with user and movies contexts
    return flask.render_template('index.html', c={
        'user': auth.get_user_context(auth.current_user_id()),
        'all_movies': all_movies,
        'movies': movies[:50],
    })
