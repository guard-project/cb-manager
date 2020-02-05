import falcon
from .base import BaseResource
from elasticsearch_dsl import Document, Text


class ConnectionDocument(Document):
    exec_env_id = Text()
    network_link_id = Text()

    class Index:
        name = 'connection'


ConnectionDocument.init()


class ConnectionResource(BaseResource):
    doc_cls = ConnectionDocument
    doc_name = 'Connection'
