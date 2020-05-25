from elasticsearch_dsl import Date, Document, Text


class DataDocument(Document):
    exec_env_id = Text()
    agent_instance_id = Text()
    timestamp_event = Date()
    timestamp_agent = Date()

    class Index:
        name = 'data'
