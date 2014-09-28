from flask import Blueprint
from flask import redirect, render_template, request, session, url_for
from oi.db import db_session_scope
from oi.model import Repository
from oi.oauth.github import auth_github
from oi.user import get_user_in_session, require_sign_in

repository = Blueprint('repository', __name__)

@repository.route('/add', methods=['GET', 'POST'])
@require_sign_in(need_github=True)
def add_repository():
    token = session['github_access_token']
    oauth_session = auth_github.get_session(token=token)
    with db_session_scope() as db_session:
        user = get_user_in_session(db_session)
        organization = None
        if 'organization' in request.args:
            organization = request.args['organization']
            organizations = oauth_session.get('user/orgs').json()
            if len(organizations) == 0:
                return redirect(url_for('repository.add_repository'))
            if (organization == '' or
               organization not in (org['login'] for org in organizations)):
                return render_template('organization_select.html',
                                       items=organizations,
                                       user=user)
        if organization:
            api_path = 'orgs/%s/repos' % organization
        else:
            api_path = 'user/repos?type=owner'
        repositories = oauth_session.get(api_path).json()
        if request.method == 'POST':
            repository = repositories[int(request.form['repository']) - 1]
            db_session.add(Repository(
                github_id=repository['id'],
                name=repository['name'],
                full_name=repository['full_name'],
                description=repository['description'],
                is_private=repository['private'],
                url=repository['html_url'],
                owner_user=user
            ))
            return redirect('dashboard')
        return render_template('repository_add.html',
                               items=repositories,
                               organization=organization,
                               user=user)

