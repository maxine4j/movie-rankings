import flask
import movie_rankings.data as data
import movie_rankings.auth as auth


app_profile = flask.Blueprint('app_profile', __name__)


@app_profile.route('/user/<target_user_id>')
def view_user_favs(target_user_id):
    target_user = auth.get_user_context(target_user_id)
    # 404 if the use doesnt exist
    if target_user is None:
        return flask.abort(404)
    # get the target users favourite movies
    movies = data.get_fav_movies(target_user_id)
    movies = data.add_fav_count(movies)
    # flag our own favourite status for each of them
    movies = data.flag_fav_movies(movies, auth.current_user_id())
    # render the profile page
    return flask.render_template('profile_favourites.html', c={
        'user': auth.get_user_context(auth.current_user_id()),
        'target_user': target_user,
        'movies': movies[:50]
    })


@app_profile.route('/user/<target_user_id>/polls')
def view_user_polls(target_user_id):
    polls = data.get_polls(auth.current_user_id(), target_user_id=target_user_id)
    for poll in polls:
        poll['choices'] = list(poll['choices'].values())
        poll['choices'].sort(key=lambda x: x['vote_count'], reverse=True)
    return flask.render_template('polls.html', c={
        'user': auth.get_user_context(auth.current_user_id()),
        'polls': polls
    })
