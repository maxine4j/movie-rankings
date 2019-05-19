import os
import data
import flask
import flask_dance.contrib.facebook as facebook

from views.api import app_api
from views.index import app_index
from views.profile import app_profile
from views.rankings import app_rankings
from views.search import app_search
from views.poll import app_poll
from views.admin import app_admin


# create and set up flask app
app = flask.Flask(__name__, static_url_path='/static')
app.secret_key = os.environ.get('APP_SECRET_KEY')
# set up facebook oauth2 login
blueprint = facebook.make_facebook_blueprint(
    client_id=os.environ.get('FACEBOOK_CLIENTID'),
    client_secret=os.environ.get('FACEBOOK_SECRET'),
)
app.register_blueprint(blueprint, url_prefix='/login')
# register views
app.register_blueprint(app_api)
app.register_blueprint(app_index)
app.register_blueprint(app_profile)
app.register_blueprint(app_rankings)
app.register_blueprint(app_search)
app.register_blueprint(app_poll)
app.register_blueprint(app_admin)
# initialise the DB
data.init_db()


if __name__ == '__main__':
    app.run(host='127.0.0.1', port='443', debug=True, ssl_context='adhoc')
