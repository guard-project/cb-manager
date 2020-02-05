import falcon
from marshmallow import fields, Schema
import elasticsearch
from elasticsearch_dsl import Document, InnerDoc, Nested, Text, Search

class ExecEnvResponseSchema(Schema):
    hostname = fields.String()
    type_id = fields.String()


class ExecEnvDocument(Document):
    hostname = Text()
    type_id = Text()

    class Index:
        name = 'exec-env'

ExecEnvDocument.init()

class ExecEnvResource(object, ):
    request_schema = ExecEnvRequestSchema()

    def on_get(self, req, resp):
        try:
            self.s = Search(index=ExecEnvDocument.Index.name)
            res = self.s.execute()
            req.context['result'] = [dict(item.to_dict(), id=item.meta.id) for item in res]
        except elasticsearch.RequestError as e:
            pass

    def on_post(self, req, resp):
        pass

    def on_delete(self, req, resp):
        pass

    def on_put(self, req, resp):
        pass
