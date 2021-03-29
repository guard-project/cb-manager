from elasticsearch_dsl import Text

from document.base import Base_Document


class Connection_Document(Base_Document):
    """Represents an connection between execution environments and network links."""

    # id already defined by Elasticsearch
    exec_env_id = Text(required=True)
    network_link_id = Text(required=True)
    description = Text()

    class Index:
        """Elasticsearch configuration."""

        name = 'connection'
