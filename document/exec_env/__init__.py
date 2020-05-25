from elasticsearch_dsl import Date, Document, InnerDoc, Integer, Nested, Text


class LCPDocument(InnerDoc):
    port = Integer(required=True)
    username = Text()
    password = Text()
    cb_password = Text()
    cb_expiration = Date()
    last_heartbeat = Date()


class ExecEnvDocument(Document):
    hostname = Text(required=True)
    lcp = Nested(LCPDocument, required=True)
    type_id = Text(required=True)

    class Index:
        name = 'exec-env'
