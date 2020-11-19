from document.base import Base_Document

__all__ = [
    'Algorithm_Document'
]


class Algorithm_Document(Base_Document):
    """Represents the algorithms."""

    # id already defined by Elasticsearch

    class Index:
        """Elasticsearch configuration."""
        name = 'algorithm'
