from configparser import BasicInterpolation as Basic_Interpolation, ConfigParser as Config_Parser
from os import path
from pathlib import Path
from utils.log import Log

__all__ = [
    'Config_Reader'
]


class Config_Reader:
    path = Path(__file__).parent / '../config.ini'

    def __init__(self):
        self.cr = Config_Parser(interpolation=Config_Reader.Env_Interpolation())

    def read(self):
        self.cr.read(self.path.resolve())

        self.cb_host = self.cr.get('context-broker', 'host')
        self.cb_port = self.cr.get('context-broker', 'port')

        self.hb_timeout = self.cr.get('heartbeat', 'timeout')
        self.hb_period = self.cr.get('heartbeat', 'period')
        self.hb_auth_expiration = self.cr.get('heartbeat', 'auth-expiration')

        self.es_endpoint = self.cr.get('elasticsearch', 'endpoint')
        self.es_timeout = self.cr.get('elasticsearch', 'timeout')
        self.es_retry_period = self.cr.get('elasticsearch', 'retry-period')

        self.elastic_apm_server = self.cr.get('elastic-apm', 'server');

        self.dev_username = self.cr.get('dev', 'username')
        self.dev_password = self.cr.get('dev', 'password')

        self.log_level = self.cr.get('log', 'level')

        Log.init(default=self.log_level, levels=self.cr.items('log'))

    def write(self, db):
        self.cr.set('context-broker', 'port', db.port)
        self.cr.set('elasticsearch', 'endpoint', db.es_endpoint)
        self.cr.set('elasticsearch', 'timeout', db.es_timeout)

        with self.path.open('w') as f:
            self.cr.write(f)

    class Env_Interpolation(Basic_Interpolation):
        """Interpolation which expands environment variables in values."""

        def before_get(self, parser, section, option, value, defaults):
            """
            Executes before getting the value.

            :param self: class instance
            :param parser: configparser instance
            :param section: section value
            :param option: option value
            :param value: current value
            :param defaults: default values
            :returns: value with expanded variables
            """
            return path.expandvars(value)
