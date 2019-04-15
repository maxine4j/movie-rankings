import flask
import app.data as data
import json
import os
import requests
from flask_dance.contrib.facebook import make_facebook_blueprint, facebook

app = flask.Flask(__name__, static_url_path='/static')
app.secret_key = 'debug_key'
blueprint = make_facebook_blueprint(
    client_id=os.environ.get('FACEBOOK_CLIENTID'),
    client_secret=os.environ.get('FACEBOOK_SECRET'),
)
app.register_blueprint(blueprint, url_prefix='/login')
data.init_db()


def is_authenticated():
    return 'user_id' in flask.session


def get_authed_user_id():
    return flask.session['user_id']


def try_login_user():
    if facebook.token and 'user_id' not in flask.session:
        # ask FB for account ID
        res = requests.get('https://graph.facebook.com/me?access_token=' + facebook.token['access_token'])
        fb_json = res.json()
        # try and get the user from out local DB
        user = data.get_user(fb_json['id'])
        # if we havent seen this user before, register them
        if not user:
            data.register_user(fb_json['id'], fb_json['name'])
        # save the users ID to our session
        flask.session['user_id'] = fb_json['id']


def get_user_context(user_id):
    user = data.get_user(user_id)
    if user is None:
        return None
    # avatar
    res = requests.get('https://graph.facebook.com/v3.2/' + str(user['id']) + '/picture?type=large&redirect=false&access_token=' + facebook.token['access_token'])
    avatar_url = "https://i.imgur.com/IGUApaz.jpg"
    if res.ok:
        avatar_url = res.json()['data']['url']
    return {
        'name': user['name'],
        'avatar_url': avatar_url,
        'id': user['id']
    }


@app.route('/')
def view_index():
    try_login_user()
    if not is_authenticated():
        return flask.redirect(flask.url_for('facebook.login'))
    else:
        movies = data.get_popular_movies()
        movies = data.prepare_movie_list(movies, get_authed_user_id())
        return flask.render_template('index.html', context={
            'user': get_user_context(get_authed_user_id()),
            'movies': movies[:50]
        })


@app.route('/search')
def view_search():
    term_str = flask.request.args.get('q')
    terms = term_str.split(' ')
    movies = data.search_movies(terms)
    movies = data.prepare_movie_list(movies, get_authed_user_id())
    return flask.render_template('search.html', context={
        'user': get_user_context(get_authed_user_id()),
        'movies': movies[:50],
        'search_query': term_str
    })


@app.route('/user/<user_id>')
def view_user(user_id):
    movies = data.get_user_fav_movies(user_id)
    movies = data.prepare_movie_list(movies, get_authed_user_id())
    target_user = get_user_context(user_id)
    if target_user is None:
        return flask.abort(404)
    return flask.render_template('profile.html', context={
        'user': get_user_context(get_authed_user_id()),
        'target_user': target_user,
        'movies': movies[:50]
    })


@app.route('/rankings')
def view_rankings():
    movies = data.get_top_favourited_movies()
    movies = data.prepare_movie_list(movies, get_authed_user_id())
    return flask.render_template('rankings.html', context={
        'user': get_user_context(get_authed_user_id()),
        'movies': movies[:50]
    })


@app.route('/api/1/favourite/<movie_id>')
def api_toggle_favourite(movie_id):
    if not is_authenticated():
        return json.dumps({
            'success': False,
            'message': 'You are not logged in'
        })
    favourite_status = data.toggle_favourite(flask.session['user_id'], movie_id)
    return json.dumps({
        'favourite': favourite_status,
    })


def main():
    app.run(host='127.0.0.1', port='443', debug=True, ssl_context='adhoc')


if __name__ == '__main__':
    main()
