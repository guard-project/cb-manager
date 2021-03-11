from argparse import ArgumentParser as Argument_Parser

from about import description, title, version
from reader.config import Config_Reader
from utils.log import Log
from utils.time import get_seconds

__all__ = [
    'Arg_Reader'
]


class Arg_Reader:
    db = None
    cr = None
    ap = None

    @classmethod
    def init(cls):
        cls.cr = Config_Reader()
        cls.cr.read()
        cls.ap = Argument_Parser(prog='python3 main.py',
                                 description=f'{title}: {description}')
        add = cls.ap.add_argument

        add('--host', '-o', type=str,
            help='Hostname/IP of the REST Server', default=cls.cr.cb_host)
        add('--port', '-p', type=int,
            help='TCP Port of the REST Server', default=cls.cr.cb_port)
        add('--auth', '-t',
            help='Enable HTTP authentication', action='store_true')
        add('--https', '-q',
            help='Force to use HTTPS instead of HTTP', action='store_true')

        add('--hb-timeout', '-b', type=str,
            help='Timeout (with unit, e.g.: 10s) for heartbeat with LCP', default=cls.cr.hb_timeout)
        add('--hb-period', '-r', type=str,
            help='Period (with unit, e.g.: 1min) for the heartbeat with the LCP', default=cls.cr.hb_period)
        add('--hb-auth-expiration', '-x', type=str,
            help='Period (with unit, e.g.: 1min) for auth expiration used in the heartbeat with the LCP',
            default=cls.cr.hb_auth_expiration)

        add('--apm-enabled', '-n',
            help='Elastic APM hostname/IP:port', action='store_true')
        add('--apm-server', '-m', type=str,
            help='Elastic APM hostname/IP:port',
            default=cls.cr.elastic_apm_server)

        add('--es-endpoint', '-e', type=str,
            help='Elasticsearch server hostname/IP:port',
            default=cls.cr.es_endpoint)
        add('--es-timeout', '-s', type=str,
            help='Timeout (with unit, e.g.: 10s) for the connection to Elasticsearch',
            default=cls.cr.es_timeout)
        add('--es-retry_period', '-y', type=str,
            help='Period (with unit, e.g.: 1min) to retry the connection to Elasticsearch',
            default=cls.cr.es_retry_period)

        add('--dev-username', '-u', type=str,
            help='Authorized username', default=cls.cr.dev_username)
        add('--dev-password', '-a', type=str,
            help='Authorized password', default=cls.cr.dev_password)
        add('--log-level', '-l', choices=Log.get_levels(),
            help='Log level', default=cls.cr.log_level)

        add('--write-config', '-w',
            help='Write options to config.ini', action='store_true')
        add('--version', '-v', help='Show version',
            action='store_const', const=version)

        return cls.ap

    @classmethod
    def read(cls):
        cls.init()

        cls.db = cls.ap.parse_args()
        cls.db.config = cls.cr
        for field in ('hb_timeout', 'hb_period', 'hb_auth_expiration',
                      'es_timeout', 'es_retry_period'):
            setattr(cls.db, field, get_seconds(getattr(cls.db, field)))

        cls.db.auth = cls.db.auth or cls.cr.cb_auth
        cls.db.https = cls.db.https or cls.cr.cb_https
        cls.db.apm_enabled = cls.db.apm_enabled or cls.cr.elastic_apm_enabled

        if cls.db.write_config:
            cls.cr.write(cls.db)

        return cls.db
