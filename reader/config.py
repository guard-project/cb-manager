from configparser import BasicInterpolation
from configparser import ConfigParser as Config_Parser
from os import path
from pathlib import Path


class ConfigReader:
    path = Path(__file__).parent / "../config.ini"

    def __init__(self):
        self.cfg_parser = Config_Parser(
            interpolation=ConfigReader.EnvInterpolation())

    def read(self):
        self.cfg_parser.read(self.path.resolve())

        self.cb_host = self.cfg_parser.get(
            "context-broker", "host", fallback="0.0.0.0")
        self.cb_port = self.cfg_parser.get(
            "context-broker", "port", fallback=5000)
        self.cb_https = self.cfg_parser.getboolean(
            "context-broker", "https", fallback=False
        )

        self.auth = self.cfg_parser.getboolean(
            "auth", "enabled", fallback=True)
        self.auth_header_prefix = self.cfg_parser.get(
            "auth", "header-prefix", fallback="GUARD"
        )
        self.auth_secret_key = self.cfg_parser.get(
            "auth", "secret-key", fallback="guard-secret-key"
        )

        self.hb_timeout = self.cfg_parser.get(
            "heartbeat", "timeout", fallback="10s")
        self.hb_period = self.cfg_parser.get(
            "heartbeat", "period", fallback="1min")

        self.es_endpoint = self.cfg_parser.get(
            "elasticsearch", "endpoint", fallback="localhost:9200"
        )
        self.es_timeout = self.cfg_parser.get(
            "elasticsearch", "timeout", fallback="20s"
        )
        self.es_retry_period = self.cfg_parser.get(
            "elasticsearch", "retry-period", fallback="3min"
        )

        self.elastic_apm_enabled = self.cfg_parser.getboolean(
            "elastic-apm", "enabled", fallback=False
        )
        self.elastic_apm_server = self.cfg_parser.get(
            "elastic-apm", "server", fallback="http://localhost:8200"
        )

        self.log_config = self.cfg_parser.get(
            "log", "config", fallback="log.yaml")

    def write(self, data_base):
        # FIXME is it necessary?
        self.cfg_parser.set("context-broker", "port", data_base.port)
        self.cfg_parser.set("elasticsearch", "endpoint", data_base.es_endpoint)
        self.cfg_parser.set("elasticsearch", "timeout", data_base.es_timeout)

        with self.path.open("w") as file:
            self.cfg_parser.write(file)

    class EnvInterpolation(BasicInterpolation):
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
