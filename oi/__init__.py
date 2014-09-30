from flask import Flask
from flask import render_template, redirect, request, url_for
from oi.db import db_session_scope
from oi.oauth import oauth
from oi.repository import repository
from oi.user import check_sign_in, require_sign_in, sign_out
from oi.user import get_user_in_session
from oi.util import get_random_string

app = Flask(__name__)
app.secret_key = get_random_string(128)
app.register_blueprint(oauth, url_prefix='/oauth')
app.register_blueprint(repository, url_prefix='/repository')

@app.route("/")
def index():
    if check_sign_in():
        return redirect(url_for('dashboard'))
    message = None
    if 'error' in request.args:
        if request.args['error'] == 'email':
            message = "Your account has not verified it's email!"
    return render_template('frame.html', message=message)

@app.route("/sign_out")
def do_sign_out():
    sign_out()
    return redirect(url_for("index"))

@app.route("/dashboard")
@require_sign_in()
def dashboard():
    with db_session_scope() as db_session:
        user = get_user_in_session(db_session)
        return render_template('dashboard.html', user=user)

