from pathlib import Path
from resource.base import Base_Minimal_Resource

from falcon import HTTP_200


class Dashboard_Resource(Base_Minimal_Resource):
    routes = [
        '/dashboard',
        '/dashboard/{part}/{resource}',
    ]

    def on_get(self, req, resp, resource='index.html', part=''):
        resp.status = HTTP_200
        if resource.endswith('.html'):
            resp.content_type = 'text/html'
        elif resource.endswith('.js'):
            resp.content_type = 'text/javascript'
        path = Path(__file__).parent.parent / 'dashboard' / part / resource
        with path.open('r') as file:
            resp.body = file.read()
