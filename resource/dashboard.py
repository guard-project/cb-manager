from pathlib import Path
from resource.base import BaseMinimalResource

from falcon import HTTP_200


class DashboardResource(BaseMinimalResource):
    routes = [
        '/dashboard',
        '/dashboard/{part}/{resource}',
    ]

    def on_get(self, _, resp, resource='index.html', part=''):
        resp.status = HTTP_200
        if resource.endswith('.html'):
            resp.content_type = 'text/html'
        elif resource.endswith('.js'):
            resp.content_type = 'text/javascript'
        path = Path(__file__).parent.parent / 'dashboard' / part / resource
        with path.open('r') as file:
            resp.body = file.read()
