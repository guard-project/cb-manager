from marshmallow import validate
from marshmallow.fields import Boolean, Integer, List, Nested, Str

from schema.base import Base_Schema
from schema.validate import Unique_List
from utils.schema import List_or_One

ORDER_MODES = ['asc', 'desc']


class Query_Request_Order_Schema(Base_Schema):
    """Order the filtered items."""

    target = Str(required=True, example='name', description='The field to compare.')
    mode = Str(required=True, enum=ORDER_MODES, default='asc', example=ORDER_MODES[0],
               description='Order mode.', validate=validate.OneOf(ORDER_MODES))


class Query_Request_Limit_Schema(Base_Schema):
    """Limit the items to return."""

    _from = Integer(data_key='from', example=1, description='Started index of the items to return.')
    _to = Integer(data_key='to', example=5, description='Ended index of the items to return.')


class Query_Request_Filter_Schema(Base_Schema):
    """For numeric comparison in the clause."""

    target = Str(required=True, example='id', description='The field to compare.')
    expr = Str(required=True, example='apache', description='The expression to compare to the field.')


class Query_Request_Clause_Schema(Base_Schema):
    """Represents a clause to filter a item based on various conditions."""

    _and = Nested('self', data_key='and', many=True, description='All the clause has to be satisfied.')
    _or = Nested('self', data_key='or', many=True, description='At least the clause has to be satisfied.')
    _not = Nested('self', data_key='not', description='The clause has to be not satisfied.')
    lte = Nested(Query_Request_Filter_Schema, description='The target field must be lower or equal to the expr value.')
    gte = Nested(Query_Request_Filter_Schema, description='The target field must be greater or equal to the expr value.')
    lt = Nested(Query_Request_Filter_Schema, description='The target field must be lower than the expr value.')
    gt = Nested(Query_Request_Filter_Schema, description='The target field must be greater to the expr value.')
    equals = Nested(Query_Request_Filter_Schema, description='The target field must be equal to the expr value.')
    reg_exp = Nested(Query_Request_Filter_Schema, description='The target field must be satisfy the regular expression in expr.')
    wildcard = Nested(Query_Request_Filter_Schema, description='The target field must be satisfy the wildcard in expr.')


class Query_Request_Schema(Base_Schema):
    """Query request to filter the items."""

    select = List_or_One(Str, example='id', description='Fields to return.',
                         validate=Unique_List.apply(), error_messages=Unique_List.error_messages)
    where = Nested(Query_Request_Clause_Schema, description='Filter the items based on different conditions.')
    order = Nested(Query_Request_Order_Schema, many=True, description='Order the filtered items.')
    limit = Nested(Query_Request_Limit_Schema, description='Limit the number of items to return.')
    force = Boolean(default=False, example=True,
                    description="""Force the execution of the request even there are some errors
                                   (example: delete a inconstent entries).""")
