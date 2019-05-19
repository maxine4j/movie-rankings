import flask
import json
import movie_rankings.data as data
import movie_rankings.auth as auth


app_poll = flask.Blueprint('app_poll', __name__)


@app_poll.route('/polls/')
def view_all_polls():
    polls = data.get_polls(auth.current_user_id())
    for poll in polls:
        poll['choices'] = list(poll['choices'].values())
        poll['choices'].sort(key=lambda x: x['vote_count'], reverse=True)
    return flask.render_template('polls.html', c={
        'user': auth.get_user_context(auth.current_user_id()),
        'polls': polls
    })


@app_poll.route('/poll/<poll_id>')
def view_poll(poll_id):
    poll = data.get_poll(poll_id, current_user_id=auth.current_user_id())
    if not poll:
        return flask.redirect('/polls')
    # sort poll choices by vote count
    poll['choices'] = list(poll['choices'].values())
    poll['choices'].sort(key=lambda x: x['vote_count'], reverse=True)
    # get comments for the poll
    comments = data.get_poll_comments(poll_id)
    comments.sort(key=lambda x: x['timestamp'], reverse=True)
    return flask.render_template('poll.html', c={
        'user': auth.get_user_context(auth.current_user_id()),
        'poll': poll,
        'comments': comments
    })
