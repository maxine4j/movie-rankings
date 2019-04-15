import flask
import movie_rankings.data as data
import movie_rankings.auth as auth


app_search = flask.Blueprint('app_search', __name__)


@app_search.route('/search')
def view_search():
    # split the search terms up
    term_str = flask.request.args.get('q')
    terms = term_str.split(' ')
    # search the database for movies
    movies = data.search_movies(terms, auth.current_user_id())
    # render the results page
    return flask.render_template('search.html', c={
        'user': auth.get_user_context(auth.current_user_id()),
        'movies': movies[:50],
        'search_query': term_str
    })
