from document.base import Base_Document

__all__ = [
    'Pipeline_Document'
]


class Pipeline_Document(Base_Document):
    """Represents the stored pipelines."""

    # id already defined by Elasticsearch


    class Index:
        """Elasticsearch configuration."""
        name = 'pipeline'
