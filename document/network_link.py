from document.base import Base_Document
from elasticsearch_dsl import Text

__all__ = [
    'Network_Link_Document',
    'Network_Link_Type_Document'
]


class Network_Link_Document(Base_Document):
    """Represents a network link."""
    # id already defined by Elasticsearch
    type_id = Text(required=True)
    description = Text()

    class Index:
        """Elasticsearch configuration."""
        name = 'network-link'


class Network_Link_Type_Document(Base_Document):
    """Represents a network link type."""
    # id already defined by Elasticsearch
    name = Text(required=True)
    description = Text()

    class Index:
        """Elasticsearch configuration."""
        name = 'network-link-type'
