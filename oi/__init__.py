from flask import Flask
from flask import render_template, request
from oi.db import db_session_scope
from oi.oauth import oauth
from oi.repository import repository
from oi.user import require_sign_in, sign_out, get_user_in_session
from oi.util import get_random_string

app = Flask(__name__)
app.secret_key = get_random_string(128)
app.register_blueprint(oauth, url_prefix='/oauth')
app.register_blueprint(repository, url_prefix='/repository')

@app.route("/")
def index():
    message = None
    if 'error' in request.args:
        if request.args['error'] == 'email':
            message = "Your account has not verified it's email!"
    return render_template('frame.html', message=message)

@app.route("/hello")
@require_sign_in()
def hello():
    with db_session_scope() as db_session:
        user = get_user_in_session(db_session)
        return render_template('dashboard.html', user=user)

