import flask
import json
import movie_rankings.data as data
import movie_rankings.auth as auth


app_api = flask.Blueprint('app_api', __name__)


@app_api.route('/api/1/favourite/<movie_id>')
def toggle_favourite(movie_id):
    # check if the user is logged in
    if not auth.is_authenticated():
        return json.dumps({
            'success': False,
            'message': 'You are not logged in'
        })
    # toggle favourite status and send the new status back
    favourite_status = data.toggle_favourite(flask.session['user_id'], movie_id)
    return json.dumps({
        'success': True,
        'favourite': favourite_status,
    })


@app_api.route('/api/1/vote/<poll_id>/<choice_id>')
def vote_poll(poll_id, choice_id):
    # check if the user is logged in
    if not auth.is_authenticated():
        return json.dumps({
            'success': False,
            'message': 'You are not logged in'
        })
    data.change_poll_vote(auth.current_user_id(), poll_id, choice_id)
    return json.dumps({
        'success': True,
    })
