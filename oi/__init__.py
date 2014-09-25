from flask import Flask
from flask import render_template
from oi.oauth import oauth

app = Flask(__name__)
app.secret_key='lkj213lk12hgjhghj34bgjuhiy23@#$%kjngfkdlsi827r32rc83h'
app.register_blueprint(oauth, url_prefix='/oauth')

@app.route("/")
def hello():
    return render_template('signin.html')

