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


@app_api.route('/api/1/search')
def search_movies():
    q = flask.request.args.get('q')
    if q:
        terms = q.split(' ')
    else:
        terms = [""]
    movies = data.search_movies(terms)
    res = {
        'results': []
    }
    for m in movies:
        res['results'].append({
            'id': m['id'],
            'text': m['title'],
        })
    return json.dumps(res)


@app_api.route('/api/1/poll/new')
def create_poll():
    # check if the user is logged in
    if not auth.is_authenticated():
        return json.dumps({
            'success': False,
            'message': 'You are not logged in'
        })
    poll_title = flask.request.args.get('title')
    poll_desc = flask.request.args.get('description')
    poll_choices = []
    for i in range(1, 25):
        pc = flask.request.args.get('choice' + str(i))
        if not pc:
            break
        poll_choices.append(pc)
    # remove duplicates
    poll_choices = list(dict.fromkeys(poll_choices))
    poll_id = data.create_poll(auth.current_user_id(), poll_title, poll_desc, poll_choices)
    return flask.redirect('/poll/{}'.format(poll_id))


@app_api.route('/api/1/comment/new', methods=['POST'])
def new_comment():
    # check if the user is logged in
    if not auth.is_authenticated():
        return json.dumps({
            'success': False,
            'message': 'You are not logged in'
        })
    comment_body = flask.request.form.get('body')
    print('comment_body =', comment_body)
    poll_id = flask.request.form.get('poll')
    print('poll_id =', poll_id)
    data.create_comment(auth.current_user_id(), poll_id, comment_body)
    return flask.redirect('/poll/{}'.format(poll_id))
