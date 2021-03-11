from falcon.errors import HTTPUnauthorized as HTTP_Unauthorized
from falcon_auth import BasicAuthBackend as Basic_Auth_Backend

from document.exec_env import Exec_Env_Document
from lib.response import Unauthorized_Response
from utils.hash import hash
from utils.log import Log

__all__ = [
    'Basic_Auth_Backend_Middleware',
    'Negotiation_Middleware'
]


class Basic_Auth_Backend_Middleware(Basic_Auth_Backend):
    def __init__(self, dev_username, dev_password):
        super().__init__(self.__auth)
        self.dev_username = dev_username
        self.dev_password = dev_password
        self.log = Log.get('basic-auth-backend-middleware')

    def authenticate(self, req, resp, resource):
        try:
            return super().authenticate(req, resp, resource)
        except HTTP_Unauthorized as e:
            self.log.exception('Unauthorized request', e)
            Unauthorized_Response().apply(resp)

    def __auth(self, username, password):
        auth_data = [(self.dev_username, self.dev_password)]
        exec_env = Exec_Env_Document.get(id=username, ignore=404)
        if exec_env is not None and exec_env.lcp.last_heartbeat is not None:
            auth_data.append((exec_env.meta.id, exec_env.lcp.cb_password))
        if (username, hash(password)) in auth_data:
            return dict(username=username)
        else:
            return False


class Negotiation_Middleware(object):
    def process_request(self, req, resp):
        resp.content_type = req.content_type
