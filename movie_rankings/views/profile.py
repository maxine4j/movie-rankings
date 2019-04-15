import flask
import movie_rankings.data as data
import movie_rankings.auth as auth


app_profile = flask.Blueprint('app_profile', __name__)


@app_profile.route('/user/<user_id>')
def view_user(user_id):
    movies = data.get_fav_movies(auth.current_user_id())
    movies = data.flag_fav_movies(movies, auth.current_user_id())
    target_user = auth.get_user_context(user_id)
    if target_user is None:
        return flask.abort(404)
    return flask.render_template('profile.html', c={
        'user': auth.get_user_context(auth.current_user_id()),
        'target_user': target_user,
        'movies': movies[:50]
    })