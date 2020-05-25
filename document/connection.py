from elasticsearch_dsl import Document, Text


class ConnectionDocument(Document):
    exec_env_id = Text(required=True)
    network_link_id = Text(required=True)

    class Index:
        name = 'connection'
