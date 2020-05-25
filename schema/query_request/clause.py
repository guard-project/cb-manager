from marshmallow import Schema
from marshmallow.fields import Nested, String
from schema.query_request.filter import QueryRequestFilterSchema

class QueryRequestClauseSchema(Schema):
    """
    Represents a clause to filter a item based on various conditions.
    """
    _and = Nested('self',
                   data_key='and',
                   many=True,
                   description='All the clause has to be satisfied.')
    _or = Nested('self',
                 data_key='or',
                 many=True,
                 description='At least the clause has to be satisfied.')
    _not = Nested('self',
                  data_key='not',
                  description='The clause has to be not satisfied.')
    lte = Nested(QueryRequestFilterSchema,
                 description='The target field must be lower or equal to the expr value.')
    gte = Nested(QueryRequestFilterSchema,
                 description='The target field must be greater or equal to the expr value.')
    lt = Nested(QueryRequestFilterSchema,
                description='The target field must be lower than the expr value.')
    gt = Nested(QueryRequestFilterSchema,
                description='The target field must be greater to the expr value.')
    equal = Nested(QueryRequestFilterSchema,
                   description='The target field must be equal to the expr value.')
    reg_exp = Nested(QueryRequestFilterSchema,
                     description='The target field must be satisfy the regular expression in expr.')
