from falcon import HTTPUnauthorized
from falcon_auth.backends import AuthBackend
from requests import post
from requests.auth import HTTPBasicAuth


class GuardJWTAuthBackend(AuthBackend):
    def __init__(self, user_loader,
                 client_id,
                 client_secret,
                 token_check_uri,
                 auth_header_prefix):
        self.client_id = client_id
        self.client_secret = client_secret
        self.user_loader = user_loader
        self.token_check_uri = token_check_uri
        self.auth_header_prefix = auth_header_prefix

    def _decode_jwt_token(self, req):
        auth_header = req.get_header('Authorization')
        token = self.parse_auth_token_from_request(auth_header=auth_header)
        auth_check = post(self.token_check_uri,
                          auth=HTTPBasicAuth(self.client_id,
                                             self.client_secret),
                          data={'token': token})
        if auth_check.text is None:
            raise HTTPUnauthorized(
                title='401 Unauthorized',
                description='Invalid JWT Credentials',
                challenges=None)
        return auth_check.text

    def authenticate(self, req, resp, resource):
        payload = self._decode_jwt_token(req)
        user = self.user_loader(payload)
        if not user:
            raise HTTPUnauthorized(
                title='401 Unauthorized',
                description='Invalid JWT Credentials',
                challenges=None)
        return user
