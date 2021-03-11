from functools import partial
from pathlib import Path
from resource import routes

import falcon
from falcon import API
from falcon.media import JSONHandler as JSON_Handler
from falcon.media import MessagePackHandler as Message_Pack_Handler
from falcon_auth import FalconAuthMiddleware as Falcon_Auth_Middleware
from falcon_elastic_apm import ElasticApmMiddleware as Elastic_Apm_Middleware
from falcon_elastic_apm import middleware
from falcon_require_https import RequireHTTPS
from swagger_ui import falcon_api_doc

from api.error_handler import *
from api.media_handler import *
from api.middleware import *
from api.spec import Spec
from lib.heartbeat import heartbeat
from reader.arg import Arg_Reader
from utils.json import dumps, loads
from utils.log import Log

__all__ = [
    'api'
]


def api(title, version):
    log = Log.get('api')
    middlewares = [
        Negotiation_Middleware()
    ]
    if Arg_Reader.db.auth:
        log.info('HTTP authentication enabled')
        middlewares.append(Falcon_Auth_Middleware(Basic_Auth_Backend_Middleware(Arg_Reader.db.dev_username,
                                                                                Arg_Reader.db.dev_password),
                                                  exempt_routes=['/api/doc', '/api/doc/swagger.json']))
    else:
        log.info('HTTP authentication disabled')

    if Arg_Reader.db.https:
        log.info('Force to use HTTPS instead of HTTP')
        middlewares.append(RequireHTTPS())
    else:
        log.info('HTTPS not set')

    if Arg_Reader.db.apm_enabled:
        log.info('Elastic APM enabled')
        middlewares.append(Elastic_Apm_Middleware(service_name='cb_manager-apm',
                                                  server_url=Arg_Reader.db.apm_server))
    else:
        log.info('Elastic APM disabled')

    instance = API(middleware=middlewares)

    media_handlers = {
        falcon.MEDIA_JSON: JSON_Handler(loads=loads,
                                        dumps=partial(dumps, ensure_ascii=False, sort_keys=True)),
        falcon.MEDIA_MSGPACK: Message_Pack_Handler(),
        falcon.MEDIA_XML: XML_Handler(),
        falcon.MEDIA_YAML: YAML_Handler()
    }
    instance.req_options.media_handlers.update(media_handlers)
    instance.resp_options.media_handlers.update(media_handlers)

    instance.add_error_handler(*Bad_Request_Handler.get())
    instance.add_error_handler(*Internal_Server_Error_Handler.get())
    instance.add_error_handler(*Unsupported_Media_Type_Handler.get())

    api_spec = Spec(api=instance, title=title, version=version)
    routes(api=instance, spec=api_spec.get())
    falcon_api_doc(instance, config_path='./swagger/schema.json',
                   url_prefix='/api/doc', title='API doc')
    api_spec.write()

    heartbeat()

    return instance
