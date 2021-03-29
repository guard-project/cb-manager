from document.base import Base_Document


class Event_Document(Base_Document):
    """Represents the stored events."""

    # id already defined by Elasticsearch

    class Index:
        """Elasticsearch configuration."""

        name = 'event'
