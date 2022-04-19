from resource.base import BaseMinimalResource

from falcon import HTTP_200, HTTP_404

from api.oauth2_token_provider import Oauth2TokenProvider


class DevResource(BaseMinimalResource):
    routes = "/dev/{resource}"

    def on_get(self, _, resp, resource="token"):
        resp.status = HTTP_404
        if resource.lower() == "token":
            resp.content_type = "text/html"
            self.token_provider = Oauth2TokenProvider()
            resp.body = self.token_provider.token()
            resp.status = HTTP_200
