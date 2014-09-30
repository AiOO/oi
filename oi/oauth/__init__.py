import json

from flask import Blueprint
from flask import abort, redirect, request, url_for
from oi.db import db_session_scope
from oi.model import User
from oi.oauth.github import auth_github, custom_params_github, decoder_github
from oi.oauth.google import auth_google, custom_params_google, decoder_google
from oi.user import check_sign_in, get_user_by_google_id, get_user_in_session
from oi.user import sign_in

oauth = Blueprint('oauth', __name__)

def register_oauth(service_name, auth, custom_params=None, decoder=None):
    """ Register oauth information to get ready to authorize.
    """
    new_auth_service = dict()
    new_auth_service['auth'] = auth
    if custom_params:
        new_auth_service['custom_params'] = custom_params
    if decoder:
        new_auth_service['decoder'] = decoder
    __auth_map__[service_name] = new_auth_service

def get_redirect_uri(service):
    """ Simply return redirect uri to serve it to OAuth service.
    """
    return url_for('oauth.catch_code', service=service, _external=True)

@oauth.route('/signin/<service>')
def redirect_to_auth(service):
    """ Take user to login page for OAuth service.
    """
    if service not in __auth_map__:
        abort(404)
        return
    auth = __auth_map__[service]['auth']
    if 'custom_params' in __auth_map__[service]:
        params = __auth_map__[service]['custom_params']
    else:
        params = dict()
    params['redirect_uri'] = get_redirect_uri(service)
    return redirect(auth.get_authorize_url(**params))

@oauth.route('/authorize/<service>')
def catch_code(service):
    """ If it is authorized successfully, get code and request access token.
    """
    if service not in __auth_map__:
        abort(404)
        return
    auth = __auth_map__[service]['auth']
    code = request.args['code']
    params = {
            'data': {
                'code': code,
                'redirect_uri': get_redirect_uri(service),
                'grant_type': 'authorization_code'
            }
    }
    if 'decoder' in __auth_map__[service]:
        params['decoder'] = __auth_map__[service]['decoder']
    auth_session = auth.get_auth_session(**params)
    if service =='google':
        userinfo = auth_session.get('userinfo').json() 
        if userinfo['verified_email'] is False:
            return redirect(url_for('index', error='email'))
        with db_session_scope() as db_session:
            google_id = userinfo['id']
            user = get_user_by_google_id(db_session, google_id)
            if user is None:
                user = User(
                        google_id=google_id,
                        name=userinfo['name'],
                        email=userinfo['email'],
                        avatar=userinfo['picture']
                )
                db_session.add(user)
                db_session.commit()
            sign_in(user)
        return redirect(url_for('dashboard'))
    elif service == 'github':
        if not check_sign_in():
            return redirect(url_for('index'))
        with db_session_scope() as db_session:
            user = get_user_in_session(db_session)
            if user.github_access_token is None:
                user.github_access_token = auth_session.access_token
            else:
                # TODO: Exchange github account?
                pass
            sign_in(user)
            db_session.add(user)
        return redirect(url_for('dashboard'))
    else:
        abort(404)

__auth_map__ = dict()
register_oauth('github', auth_github, custom_params_github, decoder_github)
register_oauth('google', auth_google, custom_params_google, decoder_google)

