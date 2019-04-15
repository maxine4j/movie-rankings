import flask
import movie_rankings.data as data
import movie_rankings.auth as auth


app_index = flask.Blueprint('app_index', __name__)


@app_index.route('/')
def view_index():
    # TODO: logged out view
    # prompt the user to log in with facebook oauth2
    auth.try_login_user()
    # get movie db popular movies
    movies = data.get_popular_movies(auth.current_user_id())
    # render the index template with user and movies contexts
    return flask.render_template('index.html', c={
        'user': auth.get_user_context(auth.current_user_id()),
        'movies': movies[:50]
    })
