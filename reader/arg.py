from argparse import ArgumentParser as Argument_Parser

from about import description, title, version
from reader.config import Config_Reader
from utils.log import Log
from utils.time import get_seconds


class Arg_Reader:
    db = None
    cr = None
    ap = None

    @classmethod
    def init(cls):
        cls.cr = Config_Reader()
        cls.cr.read()
        cls.ap = Argument_Parser(prog='python3 main.py', description=f'{title}: {description}')
        add = cls.ap.add_argument

        add('--host', '-o', type=str, help='Hostname/IP of the REST Server', default=cls.cr.cb_host)
        add('--port', '-p', type=int, help='TCP Port of the REST Server', default=cls.cr.cb_port)
        add('--https', '-q', help='Force to use HTTPS instead of HTTP', action='store_true')

        add('--auth', '-t', help='Enable JWT authentication', action='store_true')
        add('--auth-header-prefix', '-x', type=str, help='Prefix in the JWT authentication header', default=cls.cr.auth_header_prefix)
        add('--auth-secret-key', '-k', type=str, help='Secret key for JWT authentication', default=cls.cr.auth_secret_key)

        add('--hb-timeout', '-b', type=str, help='Timeout (with unit, e.g.: 10s) for heartbeat with LCP', default=cls.cr.hb_timeout)
        add('--hb-period', '-r', type=str, help='Period (with unit, e.g.: 1min) for the heartbeat with the LCP', default=cls.cr.hb_period)

        add('--apm-enabled', '-n', help='Elastic APM hostname/IP:port', action='store_true')
        add('--apm-server', '-m', type=str, help='Elastic APM hostname/IP:port', default=cls.cr.elastic_apm_server)

        add('--es-endpoint', '-e', type=str, help='Elasticsearch server hostname/IP:port', default=cls.cr.es_endpoint)
        add('--es-timeout', '-s', type=str, help='Timeout (with unit, e.g.: 10s) for the connection to Elasticsearch', default=cls.cr.es_timeout)
        add('--es-retry_period', '-y', type=str, help='Period (with unit, e.g.: 1min) to retry the connection to Elasticsearch', default=cls.cr.es_retry_period)

        add('--log-level', '-l', choices=Log.get_levels(), help='Log level', default=cls.cr.log_level)

        add('--write-config', '-w', help='Write options to config.ini', action='store_true')
        add('--version', '-v', help='Show version', action='store_const', const=version)

        return cls.ap

    @classmethod
    def read(cls):
        cls.init()

        cls.db = cls.ap.parse_args()
        cls.db.config = cls.cr
        for field in ('hb_timeout', 'hb_period', 'es_timeout', 'es_retry_period'):
            setattr(cls.db, field, get_seconds(getattr(cls.db, field)))

        cls.db.https = cls.db.https or cls.cr.cb_https
        cls.db.auth = cls.db.auth or cls.cr.auth
        cls.db.apm_enabled = cls.db.apm_enabled or cls.cr.elastic_apm_enabled

        if cls.db.write_config:
            cls.cr.write(cls.db)

        return cls.db
