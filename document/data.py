from elasticsearch_dsl import Date, Text

from document.base import Base_Document


class Data_Document(Base_Document):
    """Represents the stored data."""

    # id already defined by Elasticsearch
    agent_instance_id = Text()
    ebpf_program_instance_id = Text()
    timestamp_event = Date()
    timestamp_agent = Date()

    class Index:
        """Elasticsearch configuration."""

        name = 'data'
