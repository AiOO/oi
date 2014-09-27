from flask import Blueprint
from flask import redirect, render_template, request, url_for
from oi.db import db_session_scope
from oi.user import get_user_in_session, require_sign_in
from oi.oauth.github import auth_github

repository = Blueprint('repository', __name__)

@repository.route('/add')
@require_sign_in()
def add_repository():
    with db_session_scope() as db_session:
        user = get_user_in_session(db_session)
        if user.github_access_token is None:
            return redirect(url_for('oauth.redirect_to_auth', service='github'))
        else:
            oauth_session = auth_github.get_session(
                    token=user.github_access_token)
            repos = oauth_session.get('user/repos?type=owner').json()
            return render_template('repository.html',
                                   repositories=repos,
                                   user=user)

