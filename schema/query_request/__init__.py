from marshmallow import Schema
from marshmallow.fields import List, Nested, String
from schema.query_request.clause import QueryRequestClauseSchema
from schema.query_request.order import QueryRequestOrderSchema
from schema.query_request.limit import QueryRequestLimitSchema


class QueryRequestSchema(Schema):
    """
    Query request to filter the items.
    """
    select = List(String(),
                  description='Fields to return.',
                  example='[id, name]')
    where = Nested(QueryRequestClauseSchema,
                   description='Filter the items based on different conditions.')
    order = Nested(QueryRequestOrderSchema,
                   many=True,
                   description='Order the filtered items.')
    limit = Nested(QueryRequestLimitSchema,
                   description='Limit the number of items to return.')
