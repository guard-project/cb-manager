from configparser import ConfigParser
from log import Log
from utils import EnvInterpolation

import git


class ConfigReader:
    def __init__(self):
        self.cr = ConfigParser(interpolation=EnvInterpolation())
        repo = git.Repo(search_parent_directories=True)
        self.version = f'{repo.head.object.hexsha}@{repo.active_branch}'

    def read(self):
        self.cr.read('config.ini')

        self.title = self.cr.get('info', 'title')
        self.description = self.cr.get('info', 'description')

        self.cb_host = self.cr.get('context-broker', 'host')
        self.cb_port = self.cr.get('context-broker', 'port')

        self.hb_timeout = self.cr.get('hearthbeat', 'timeout')
        self.hb_period = self.cr.get('hearthbeat', 'period')
        self.hb_auth_expiration = self.cr.get('hearthbeat', 'auth-expiration')

        self.es_endpoint = self.cr.get('elasticsearch', 'endpoint')
        self.es_timeout = self.cr.get('elasticsearch', 'timeout')
        self.es_retry_period = self.cr.get('elasticsearch', 'retry-period')

        self.dev_username = self.cr.get('dev', 'username')
        self.dev_password = self.cr.get('dev', 'password')

        self.log_level = self.cr.get('log', 'level')

        Log.init(default=self.log_level, levels=self.cr.items('log'))


    def write(self, db):
        self.cr.set('context-broker', 'port', db.port)
        self.cr.set('elasticsearch', 'endpoint', db.es_endpoint)
        self.cr.set('elasticsearch', 'timeout', db.es_timeout)

        with open('config.ini', 'w') as f:
            self.cr.write(f)
