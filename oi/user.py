from flask import Blueprint
from flask import redirect, session, url_for
from functools import partial, wraps
from oi.model import User
from oi.util import timestamp, TIME_MINUTES

def get_user(db_session, user_id):
    user = db_session.query(User).filter(User.id == user_id).first()
    return user

def get_user_by_google_id(db_session, google_id):
    user = db_session.query(User).filter(User.google_id == google_id).first()
    return user

def get_user_in_session(db_session):
    return get_user(db_session, session['user_id'])

def set_expire():
    session['expires'] = timestamp() + 30 * TIME_MINUTES

def sign_in(user, service='google'):
    session['user_id'] = user.id
    set_expire()

def sign_out():
    session.pop('user_id', None)
    session.pop('expires', None)

def check_sign_in(service='google'):
    if 'expires' not in session:
        return False
    if session['expires'] < timestamp():
        sign_out()
        return False
    set_expire()
    return True

def require_sign_in(func=None, service='google'):
    if func is None:
        return partial(require_sign_in, service=service)
    @wraps(func)
    def new_function(*args, **kwargs):
        if check_sign_in(service) == True:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('index'))
    return new_function

