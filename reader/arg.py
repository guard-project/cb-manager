from argparse import ArgumentParser as Argument_Parser

from about import description, title, version
from reader.config import ConfigReader
from utils.time import get_seconds


class ArgReader:
    db = None
    cr = None
    ap = None

    @classmethod
    def init(cls):
        cls.cr = ConfigReader()
        cls.cr.read()
        cls.ap = Argument_Parser(
            prog="python3 main.py", description=f"{title}: {description}"
        )
        add = cls.ap.add_argument

        add("--host", "-o", type=str,
            help="Hostname/Ip of the REST Server", default=cls.cr.cb_host)
        add("--port", "-p", type=int,
            help="TCP Port of the REST Server", default=cls.cr.cb_port)
        add("--https", "-q", help="Force to use HTTPS instead of HTTP",
            action="store_true")

        add("--auth", "-t", help="Enable JWT authentication",
            action="store_true", default=cls.cr.auth)
        add("--auth-header-prefix", "-x", type=str,
            help="Prefix in the JWT authentication header",
            default=cls.cr.auth_header_prefix)
        add("--auth-secret-key", "-k", type=str,
            help="Secret key for JWT authentication",
            default=cls.cr.auth_secret_key)

        add("--oauth2", "-j", help="Enable OAuth2/JWT authentication",
            action="store_true", default=cls.cr.oauth2)
        add("--oauth2-client-id", "-c", type=str,
            help="Client ID for OAuth2/JWT authentication",
            default=cls.cr.oauth2_client_id)
        add("--oauth2-client-secret", "-g", type=str,
            help="OAuth2 secret for OAuth2/JWT authentication",
            default=cls.cr.oauth2_client_secret)
        add("--oauth2-token-check-uri", "-u", type=str,
            help="URI for check OAuth2/JWT authentication",
            default=cls.cr.oauth2_token_check_uri)
        add("--oauth2-token-get-uri", "-a", type=str,
            help="URI for get OAuth2/JWT authentication",
            default=cls.cr.oauth2_token_get_uri)
        add("--oauth2-verify", "-i", type=str,
            help="Path to the TLS certificate for OAuth2/JWT authentication",
            default=cls.cr.oauth2_verify)

        add("--hb-timeout", "-b", type=str,
            help="Timeout (with unit, e.g.: 10s) for heartbeat with LCP",
            default=cls.cr.hb_timeout)
        add("--hb-period", "-r", type=str,
            help="Period (with unit, e.g.: 1min) for the heartbeat with the LCP",  # noqa: E501
            default=cls.cr.hb_period)

        add("--discovery-period", "-d", type=str,
            help="Period (with unit, e.g.: 1min) for the discovery with the LCP",  # noqa: E501
            default=cls.cr.discovery_period)

        add("--apm-enabled", "-n", help="Enable Elastic APM integration",
            action="store_true")
        add("--apm-server", "-m", type=str,
            help="Elastic APM hostname/IP:port",
            default=cls.cr.elastic_apm_server)

        add("--es-endpoint", "-e", type=str,
            help="Elasticsearch server hostname/IP:port",
            default=cls.cr.es_endpoint)
        add("--es-timeout", "-s", type=str,
            help="Timeout (with unit, e.g.: 10s) for the connection to Elasticsearch",  # noqa: E501
            default=cls.cr.es_timeout,)
        add("--es-retry_period", "-y", type=str,
            help="Period (with unit, e.g.: 1min) to retry the connection to Elasticsearch",  # noqa: E501
            default=cls.cr.es_retry_period)

        add("--log-config", "-l",
            help="Path of the log configuration file (e.g. log.yaml)",
            default=cls.cr.log_config)

        add("--write-config", "-w", help="Write options to config.ini",
            action="store_true")
        add("--version", "-v", help="Show version", action="store_const",
            const=version)

        return cls.ap

    @classmethod
    def read(cls):
        cls.init()

        cls.db = cls.ap.parse_args()
        cls.db.config = cls.cr
        for field in (
            "hb_timeout",
            "hb_period",
            "es_timeout",
            "es_retry_period",
            "discovery_period"
        ):
            setattr(cls.db, field, get_seconds(getattr(cls.db, field)))

        cls.db.https = cls.db.https or cls.cr.cb_https
        cls.db.auth = cls.db.auth or cls.cr.auth
        cls.db.apm_enabled = cls.db.apm_enabled or cls.cr.elastic_apm_enabled

        if cls.db.write_config:
            cls.cr.write(cls.db)

        return cls.db
