from .config import ConfigResource
from elasticsearch_dsl import Document, Text


class NetworkLinkTypeDocument(Document):
    name = Text()

    class Index:
        name = 'network-link-type'


class NetworkLinkTypeResource(ConfigResource):
    doc_cls = NetworkLinkTypeDocument
    doc_name = 'Network Link Type'
