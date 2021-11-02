from elasticsearch_dsl.field import Text

from document.base import BaseDocument


class PipelineDocument(BaseDocument):
    """Represents the stored pipelines."""

    # id already defined by Elasticsearch
    # FIXME long format not compatible with date
    # updated_at = Date()
    # created_at = Date(required=True)
    name = Text()
    status = Text(required=True)
    user = Text()

    class Index:
        """Elasticsearch configuration."""

        name = 'pipeline'
