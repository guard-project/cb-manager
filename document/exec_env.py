from document.base import Base_Document
from elasticsearch_dsl import Date, InnerDoc as Inner_Doc, Integer, Nested, Text, Boolean

__all__ = [
    'Exec_Env_Document',
    'Exec_Env_Type_Document'
]


class LCP_Document_Inner_Doc(Inner_Doc):
    """LCP configuration data."""
    port = Integer(required=True)
    started = Date()
    last_heartbeat = Date()
    username = Text()
    password = Text()


class Exec_Env_Document(Base_Document):
    """Represents an execution environment."""
    # id already defined by Elasticsearch
    hostname = Text(required=True)
    type_id = Text(required=True)
    lcp = Nested(LCP_Document_Inner_Doc)
    description = Text()
    enabled = Boolean(required=True)

    class Index:
        """Elasticsearch configuration."""
        name = 'exec-env'


class Exec_Env_Type_Document(Base_Document):
    """Type of execution environment. Example: virtual machine or container."""
    # id already defined by Elasticsearch
    name = Text(required=True)
    description = Text()

    class Index:
        """Elasticseach configuration."""
        name = 'exec-env-type'
