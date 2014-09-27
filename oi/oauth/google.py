import json

from .__secret__ import client_id_google, client_secret_google
from rauth.service import OAuth2Service

auth_google = OAuth2Service(
        name='google',
        client_id=client_id_google,
        client_secret=client_secret_google,
        authorize_url='https://accounts.google.com/o/oauth2/auth',
        access_token_url='https://accounts.google.com/o/oauth2/token',
        base_url='https://www.googleapis.com/oauth2/v2/')
custom_params_google = {
        'response_type': 'code',
        'scope': 'openid email'
}
# We have to decode text encoding before load because there is
# the compatibility issue about Python 3.
# reference: https://github.com/litl/rauth/issues/145
decoder_google = lambda x: json.loads(x.decode('utf-8'))

