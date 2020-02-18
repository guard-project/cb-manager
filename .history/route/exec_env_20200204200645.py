import falcon
from query_parser import QueryParser
from schema import Query
from marshmallow import fields, Schema
import elasticsearch
from elasticsearch_dsl import Document, InnerDoc, Nested, Text


class ExecEnvDocument(Document):
    hostname = Text()
    type_id = Text()

    class Index:
        name = 'exec-env'

ExecEnvDocument.init()

class ExecEnvResource(object, ):
    def on_get(self, req, resp):
        query = req.context['json']
        QueryParser(index=ExecEnvDocument.Index.name).parse(query=query).search()
                    res = s.execute()
        resp.media = [cls.get_data(item) for item in res], status.HTTP_200_OK, cls.HEADERS

    def on_post(self, req, resp):
        data = req.context['json']
        id = data.pop('id', None)
        if id is None:
            pass # TODO error id not found
        try:
            ExecEnvDocument.get(id=id)
        except elasticsearch.NotFoundError:
            res = ExecEnvDocument(meta={'id': id}, **data).save()
            # TODO return res
        else:
            pass # TODO error id already found

    def on_delete(self, req, resp):
        query = req.context['json']
        resp.media = QueryParser(index=ExecEnvDocument.Index.name).parse(query=query)

    def on_put(self, req, resp):
        pass