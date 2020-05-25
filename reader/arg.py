from argparse import ArgumentParser
from log import Log
from reader.config import ConfigReader
from utils import get_seconds


class ArgReader:
    db = None

    @classmethod
    def read(cls):
        cr = ConfigReader()
        cr.read()
        ap = ArgumentParser(prog='python3 main.py',
                            description=f'{cr.title}: {cr.description}')
        add = ap.add_argument

        add('--host', '-o', type=str, help='Hostname/IP of the REST Server', default=cr.cb_host)
        add('--port', '-p', type=int, help='Tcr Port of the REST Server', default=cr.cb_port)

        add('--hb-timeout', '-b', type=str,
            help='Timeout (with unit, e.g.: 10s) for heartbeat with LCP', default=cr.hb_timeout)
        add('--hb-period', '-r', type=str,
            help='Period (with unit, e.g.: 1min) for the hearthbeat with the LCP', default=cr.hb_period)
        add('--hb-auth-expiration', '-x', type=str,
            help='Period (with unit, e.g.: 1min) for auth expiration used in the hearthbeat with the LCP',
            default=cr.hb_auth_expiration)

        add('--es-endpoint', '-e', type=str,
            help='Elasticsearch server hostname/IP:port',
            default=cr.es_endpoint)
        add('--es-timeout', '-s', type=str,
            help='Timeout (with unit, e.g.: 10s) for the connection to Elasticsearch',
            default=cr.es_timeout)
        add('--es-retry_period', '-y', type=str,
            help='Period (with unit, e.g.: 1min) to retry the connection to Elasticsearch',
            default=cr.es_retry_period)

        add('--dev-username', '-u', type=str, help='Authorized username', default=cr.dev_username)
        add('--dev-password', '-a', type=str, help='Authorized password', default=cr.dev_password)
        add('--log-level', '-l', choices=Log.get_levels(), help='Log level', default=cr.log_level)

        add('--write-config', '-w', help='Write options to cr.ini', action='store_true')
        add('--version', '-v', help='Show version', action='store_const', const=cr.version)

        cls.db = ap.parse_args()
        cls.db.config = cr
        for field in ('hb_timeout', 'hb_period', 'hb_auth_expiration', 'es_timeout', 'es_retry_period'):
            setattr(cls.db, field, get_seconds(getattr(cls.db, field)))

        if cls.db.write_config:
            cr.write(cls.db)

        return cls.db
