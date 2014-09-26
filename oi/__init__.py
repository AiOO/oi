from flask import Flask
from flask import render_template
from oi.oauth import oauth
from oi.db import db_session_scope
from oi.user import require_sign_in, sign_out, get_user_in_session
from oi.util import get_random_string

app = Flask(__name__)
app.secret_key = get_random_string(128)
app.register_blueprint(oauth, url_prefix='/oauth')

@app.route("/")
def index():
    return render_template('signin.html')

@app.route("/hello")
@require_sign_in()
def hello():
    with db_session_scope() as db_session:
        user = get_user_in_session(db_session)
        return 'Hello %s!' % user.name

