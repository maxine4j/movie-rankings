import flask
import movie_rankings.data as data
import movie_rankings.auth as auth


app_rankings = flask.Blueprint('app_rankings', __name__)


@app_rankings.route('/rankings')
def view_rankings():
    # get the top movies by our users favourites
    # TODO: add different sorting methods
    movies = data.get_top_favourited_movies(auth.current_user_id())
    return flask.render_template('rankings.html', c={
        'user': auth.get_user_context(auth.current_user_id()),
        'movies': movies[:50]
    })
