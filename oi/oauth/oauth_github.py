from .__secret__ import client_id_github, client_secret_github
from rauth.service import OAuth2Service

auth_github = OAuth2Service(
        name='github',
        client_id=client_id_github,
        client_secret=client_secret_github,
        authorize_url='https://github.com/login/oauth/authorize',
        access_token_url='https://github.com/login/oauth/access_token',
        base_url='https://api.github.com/')
custom_params_github = None
decoder_github = None

