from elasticsearch_dsl import Boolean, Date, Integer, Nested, Text

from document.base import BaseDocument, BaseInnerDoc


class LCPDocumentInnerDoc(BaseInnerDoc):
    """LCP configuration data."""

    port = Integer(required=True)
    https = Boolean(required=True)
    endpoint = Text()
    started = Date()
    last_heartbeat = Date()


class ExecEnvDocument(BaseDocument):
    """Represents an execution environment."""

    # id already defined by Elasticsearch
    hostname = Text(required=True)
    type_id = Text(required=True)
    lcp = Nested(LCPDocumentInnerDoc)
    description = Text()
    enabled = Boolean(required=True)

    class Index:
        """Elasticsearch configuration."""

        name = 'exec-env'


class ExecEnvTypeDocument(BaseDocument):
    """Type of execution environment. Example: virtual machine or container."""

    # id already defined by Elasticsearch
    name = Text(required=True)
    description = Text()

    class Index:
        """Elasticseach configuration."""

        name = 'exec-env-type'
