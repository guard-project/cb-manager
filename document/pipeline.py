from elasticsearch_dsl.field import Date, Text

from document.base import Base_Document


class Pipeline_Document(Base_Document):
    """Represents the stored pipelines."""

    # id already defined by Elasticsearch
    updated_at = Date()
    created_at = Date(required=True)
    name = Text()
    status = Text(required=True)
    user = Text()

    class Index:
        """Elasticsearch configuration."""

        name = 'pipeline'
