from elasticsearch_dsl import Document, Text


class NetworkLinkDocument(Document):
    type_id = Text(required=True)

    class Index:
        name = 'network-link'
