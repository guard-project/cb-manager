from functools import partial
from resource import routes

import falcon
from falcon import API
from falcon.media import JSONHandler, MessagePackHandler
from falcon_auth import FalconAuthMiddleware, JWTAuthBackend
from falcon_elastic_apm import ElasticApmMiddleware
from falcon_require_https import RequireHTTPS
from swagger_ui import falcon_api_doc

from api.error_handler import (BadRequestHandler, InternalServerErrorHandler,
                               UnsupportedMediaTypeHandler)
from api.media_handler import XMLHandler, YAMLHandler
from api.middleware import NegotiationMiddleware
from api.spec import Spec
from lib.heartbeat import heartbeat
from reader.arg import ArgReader
from utils.json import dumps, loads
from utils.log import Log


def api(title, version):
    log = Log.get('api')

    middlewares = [
        NegotiationMiddleware()
    ]

    if ArgReader.db.auth:
        log.notice('JWT authentication enabled')
        def user_loader(token): return {'user': token}
        secret_key = ArgReader.db.auth_secret_key,
        auth_header_prefix = ArgReader.db.auth_header_prefix
        jwt_auth_backend = JWTAuthBackend(user_loader,
                                          secret_key,
                                          auth_header_prefix)
        exempt_routes = ['/api/doc', '/api/doc/swagger.json']
        middlewares.append(FalconAuthMiddleware(
            jwt_auth_backend, exempt_routes))
    else:
        log.notice('JWT authentication disabled')

    if ArgReader.db.https:
        log.notice('Force to use HTTPS instead of HTTP')
        middlewares.append(RequireHTTPS())
    else:
        log.notice('HTTPS not set')

    if ArgReader.db.apm_enabled:
        log.notice('Elastic APM enabled')
        service_name = 'cb_manager-apm',
        server_url = ArgReader.db.apm_server
        middlewares.append(ElasticApmMiddleware(service_name, server_url))
    else:
        log.notice('Elastic APM disabled')

    instance = API(middleware=middlewares)

    media_handlers = {
        falcon.MEDIA_JSON: JSONHandler(loads=loads,
                                       dumps=partial(dumps,
                                                     ensure_ascii=False,
                                                     sort_keys=True)),
        falcon.MEDIA_MSGPACK: MessagePackHandler(),
        falcon.MEDIA_XML: XMLHandler(),
        falcon.MEDIA_YAML: YAMLHandler()
    }
    instance.req_options.media_handlers.update(media_handlers)
    instance.resp_options.media_handlers.update(media_handlers)

    instance.add_error_handler(*BadRequestHandler.get())
    instance.add_error_handler(*InternalServerErrorHandler.get())
    instance.add_error_handler(*UnsupportedMediaTypeHandler.get())

    api_spec = Spec(api=instance, title=title, version=version)
    routes(api=instance, spec=api_spec.get())
    falcon_api_doc(instance, config_path='./swagger/schema.json',
                   url_prefix='/api/doc', title='API doc')
    api_spec.write()

    heartbeat()

    return instance
