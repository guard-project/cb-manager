from falcon import HTTPUnauthorized
from falcon_auth.backends import AuthBackend
from requests import post

from api.oauth2_token_provider import Oauth2TokenProvider


class GuardJWTAuthBackend(AuthBackend):
    def __init__(self, user_loader,
                 client_id,
                 client_secret,
                 token_check_uri,
                 verify,
                 auth_header_prefix):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_check_uri = token_check_uri
        self.verify = verify
        self.auth_header_prefix = auth_header_prefix
        self.token_provider = Oauth2TokenProvider()

    def authenticate(self, req, resp, resource):
        auth_header = req.get_header('Authorization')
        token = self.parse_auth_token_from_request(auth_header=auth_header)
        auth_check = post(self.token_check_uri,
                          headers={
                              'Authorization': 'Bearer ' + self.token_provider.token()},  # noqa: E501
                          verify=self.verify,
                          data={'token': token})
        if auth_check.status_code >= 400 or auth_check.json() is None or not auth_check.json().get('active', False):  # noqa: E501
            raise HTTPUnauthorized(
                title='401 Unauthorized',
                description='Invalid JWT Credentials',
                challenges=None)
        return auth_check.json()
