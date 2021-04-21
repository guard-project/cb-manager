from elasticsearch_dsl.field import Text

from document.base import Base_Document


class Pipeline_Document(Base_Document):
    """Represents the stored pipelines."""

    # id already defined by Elasticsearch
    # updated_at = Date()  #FIXME long format not compatible with date
    # created_at = Date(required=True)  #FIXME long format not compatible with date
    name = Text()
    status = Text(required=True)
    user = Text()

    class Index:
        """Elasticsearch configuration."""

        name = 'pipeline'
