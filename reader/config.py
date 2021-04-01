from configparser import BasicInterpolation as Basic_Interpolation
from configparser import ConfigParser as Config_Parser
from os import path
from pathlib import Path


class Config_Reader:
    path = Path(__file__).parent / '../config.ini'

    def __init__(self):
        self.cr = Config_Parser(interpolation=Config_Reader.Env_Interpolation())

    def read(self):
        self.cr.read(self.path.resolve())

        self.cb_host = self.cr.get('context-broker', 'host', fallback='0.0.0.0')
        self.cb_port = self.cr.get('context-broker', 'port', fallback=5000)
        self.cb_https = self.cr.getboolean('context-broker', 'https', fallback=False)

        self.auth = self.cr.getboolean('auth', 'enabled', fallback=True)
        self.auth_header_prefix = self.cr.get('auth', 'header-prefix', fallback='GUARD')
        self.auth_secret_key = self.cr.get('auth', 'secret-key', fallback='guard-secret-key')

        self.hb_timeout = self.cr.get('heartbeat', 'timeout', fallback='10s')
        self.hb_period = self.cr.get('heartbeat', 'period', fallback='1min')

        self.es_endpoint = self.cr.get('elasticsearch', 'endpoint', fallback='localhost:9200')
        self.es_timeout = self.cr.get('elasticsearch', 'timeout', fallback='20s')
        self.es_retry_period = self.cr.get('elasticsearch', 'retry-period', fallback='3min')

        self.elastic_apm_enabled = self.cr.getboolean('elastic-apm', 'enabled', fallback=False)
        self.elastic_apm_server = self.cr.get('elastic-apm', 'server', fallback='http://localhost:8200')

        self.log_config = self.cr.get('log', 'config', fallback='log.yaml')

    def write(self, db):
        # FIXME is it necessary?
        self.cr.set('context-broker', 'port', db.port)
        self.cr.set('elasticsearch', 'endpoint', db.es_endpoint)
        self.cr.set('elasticsearch', 'timeout', db.es_timeout)

        with self.path.open('w') as f:
            self.cr.write(f)

    class Env_Interpolation(Basic_Interpolation):
        """Interpolation which expands environment variables in values."""

        def before_get(self, parser, section, option, value, defaults):
            """Execute before getting the value.

            :param self: class instance
            :param parser: configparser instance
            :param section: section value
            :param option: option value
            :param value: current value
            :param defaults: default values
            :returns: value with expanded variables
            """
            return path.expandvars(value)
