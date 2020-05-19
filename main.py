import os
path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)
os.chdir(dir_path)

import utils
from configparser import ConfigParser
config_parser = ConfigParser(interpolation=utils.EnvInterpolation())
config_parser.read('config.ini')

from log import Log
Log.set_levels(config_parser.items('log'))

from args import Args
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from elasticsearch_dsl import connections
from falcon_apispec import FalconPlugin
from falcon_auth import FalconAuthMiddleware, BasicAuthBackend
from falcon_marshmallow import Marshmallow
from resource import *
from schema import *
from swagger_ui import falcon_api_doc

import argparse
import falcon
import git
import hashlib
import json
import time
import waitress


repo = git.Repo(search_parent_directories=True)

title = config_parser.get('info', 'title')
description = config_parser.get('info', 'description')
version = f'{repo.head.object.hexsha}@{repo.active_branch}'

cb_host = config_parser.get('context-broker', 'host')
cb_port = config_parser.get('context-broker', 'port')

hb_timeout = config_parser.get('hearthbeat', 'timeout')
hb_period = config_parser.get('hearthbeat', 'period')

es_endpoint = config_parser.get('elasticsearch', 'endpoint')
es_timeout = config_parser.get('elasticsearch', 'timeout')
es_retry_period = config_parser.get('elasticsearch', 'retry-period')

dev_username = config_parser.get('dev', 'username')
dev_password = config_parser.get('dev', 'password')

log_level = config_parser.get('log', 'level')


print(f'{title} version:{version}')


parser = argparse.ArgumentParser(
    prog='python3 {__FILENAME__}', description=f'{title}: {description}')

parser.add_argument('--host', '-o', type=str,
                    help='Hostname/IP of the REST Server', default=cb_host)
parser.add_argument('--port', '-p', type=int,
                    help='TCP Port of the REST Server', default=cb_port)

parser.add_argument('--hb-timeout', '-b', type=str,
                    help='Timeout (with unit, e.g.: 10s) for heartbeat with LCPs', default=hb_timeout)
parser.add_argument('--hb-period', '-r', type=str,
                    help='Period (with unit, e.g.: 1min) per the hearthbeat with the LCPs', default=hb_period)

parser.add_argument('--es-endpoint', '-e', type=str,
                    help='Elasticsearch server hostname/IP:port', default=es_endpoint)
parser.add_argument('--es-timeout', '-s', type=str,
                    help='Timeout (with unit, e.g.: 10s) for the connection to Elasticsearch', default=es_timeout)
parser.add_argument('--es-retry_period', '-y', type=str,
                    help='Period (with unit, e.g.: 1min) to retry the connection to Elasticsearch', default=es_retry_period)

parser.add_argument('--dev-username', '-u', type=str,
                    help='Authorized username', default=dev_username)
parser.add_argument('--dev-password', '-a', type=str,
                    help='Authorized password', default=dev_password)

parser.add_argument('--log-level', '-l', choices=Log.get_levels(),
                    help='Log level', default=log_level)

parser.add_argument('--write-config', '-w', help='Write options to config.ini',
                    action='store_true')
parser.add_argument('--version', '-v', help='Show version',
                    action='store_const', const=version)

Args.set(parser.parse_args(),
         convert_to_seconds=('hb_timeout', 'hb_period', 'es_timeout', 'es_retry_period'))

log = Log.get('main')

if Args.db.write_config:
    config_parser.set('context-broker', 'port', Args.db.port)
    config_parser.set('elasticsearch', 'endpoint', Args.db.es_endpoint)
    config_parser.set('elasticsearch', 'timeout', Args.db.es_timeout)
    with open('config.ini', 'w') as f:
            config_parser.write(f)

if Args.db.version is not None:
    print(Args.db.version)
else:
    def elastic_connection():
        try:
            log.info(f'start connection to Elasticsearch ({Args.db.es_endpoint})')
            connections.create_connection(hosts=Args.db.es_endpoint, timeout=Args.db.es_timeout)
        except Exception as e:
            log.debug(e)
            log.error(f'connection to Elasticsearch ({Args.db.es_endpoint}) not possible')
            log.error(f'try again in {Args.db.es_retry_period} seconds')
            time.sleep(Args.db.es_retry_period)
            elastic_connection()
        else:
            log.success(f'connection to Elasticsearch ({Args.db.es_endpoint}) established')


    def auth(username, password):
        auth_data = [(Args.db.dev_username, Args.db.dev_password)]
        exec_env = ExecEnvDocument.get(id=username, ignore=404)
        if exec_env is not None and exec_env.lcp.last_heartbeat is not None:
            auth_data.append((exec_env.meta.id, exec_env.lcp.cb_password))
        if (username, utils.hash(password)) in auth_data:
            return {'username': username}
        else:
            False

    api = falcon.API(middleware=[
        FalconAuthMiddleware(BasicAuthBackend(auth), exempt_routes=['/api/doc', '/api/doc/swagger.json']),
        Marshmallow()
    ])

    resource_set = (AgentCatalogResource, AgentCatalogSelectedResource,
        AgentInstanceResource, AgentInstanceSelectedResource,
        ConnectionResource, ConnectionSelectedResource,
        DataResource, DataSelectedResource,
        ExecEnvResource, ExecEnvSelectedResource,
        ExecEnvTypeResource, ExecEnvTypeSelectedResource,
        NetworkLinkResource, NetworkLinkSelectedResource,
        NetworkLinkTypeResource, NetworkLinkTypeSelectedResource,
        PkgResource)

    tags = []
    for Resource in resource_set:
        tags.append(Resource.tag)

    api_spec = APISpec(
        title=title,
        version=version,
        openapi_version='2.0',
        produces=['application/json'],
        consumes=['application/json'],
        tags=tags,
        plugins=[
            FalconPlugin(api),
            MarshmallowPlugin(),
        ],
    )

    elastic_connection()

    for Resource in resource_set:
        resource = Resource()
        for route in utils.wrap(Resource.routes):
            api.add_route(route, resource)
            api_spec.path(resource=resource)
            log.success(f'{route} endpoint configured')

    with open('./api/schema.yaml', 'w') as file:
        file.write(api_spec.to_yaml())

    with open('./api/schema.json', 'w') as file:
        file.write(json.dumps(api_spec.to_dict(), indent=2))

    falcon_api_doc(api, config_path='./api/schema.json', url_prefix='/api/doc', title='API doc')

    waitress.serve(api, host=Args.db.host, port=Args.db.port)
