import flask
import json
import movie_rankings.data as data
import movie_rankings.auth as auth


app_poll = flask.Blueprint('app_poll', __name__)


@app_poll.route('/polls')
def view_all_polls():
    polls = []
    return flask.render_template('poll.html', c={
        'user': auth.get_user_context(auth.current_user_id()),
        'polls': polls
    })
