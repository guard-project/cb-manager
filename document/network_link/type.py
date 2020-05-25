from elasticsearch_dsl import Document, Text


class NetworkLinkTypeDocument(Document):
    name = Text(required=True)
    description = Text()

    class Index:
        name = 'network-link-type'
