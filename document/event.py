from document.base import BaseDocument


class EventDocument(BaseDocument):
    """Represents the stored events."""

    # id already defined by Elasticsearch

    class Index:
        """Elasticsearch configuration."""

        name = 'event'
