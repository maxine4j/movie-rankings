import flask
import requests
import movie_rankings.data as data
from flask_dance.contrib.facebook import facebook


def is_authenticated():
    return 'user_id' in flask.session


def current_user_id():
    if 'user_id' not in flask.session:
        return None
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
    # gets a context used for template rendering of the given user
    user = data.get_user(user_id)
    if user is None:
        return None
    res = None
    if facebook is not None and facebook.token is not None:
        res = requests.get('https://graph.facebook.com/v3.2/' + str(user['id']) + '/picture?type=large&redirect=false&access_token=' + facebook.token['access_token'])
    avatar_url = "https://i.imgur.com/IGUApaz.jpg"
    if res is not None and res.ok:
        avatar_url = res.json()['data']['url']
    user['avatar_url'] = avatar_url
    return user


def is_admin():
    current_user = data.get_user(current_user_id())
    return current_user['admin']
