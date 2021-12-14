from marshmallow import validate
from marshmallow.fields import Boolean, Integer, Nested, Str

from schema.base import BaseSchema
from schema.validate import UniqueList
from utils.schema import ListOrOne

ORDER_MODES = ['asc', 'desc']


class QueryRequestOrderSchema(BaseSchema):
    """Order the filtered items."""

    target = Str(required=True, example='name',
                 description='The field to compare.')
    mode = Str(required=True, enum=ORDER_MODES, default='asc',
               example=ORDER_MODES[0], description='Order mode.',
               validate=validate.OneOf(ORDER_MODES))


class QueryRequestLimitSchema(BaseSchema):
    """Limit the items to return."""

    _from = Integer(data_key='from', example=1,
                    description='Started index of the items to return.')
    _to = Integer(data_key='to', example=5,
                  description='Ended index of the items to return.')


class QueryRequestFilterSchema(BaseSchema):
    """For numeric comparison in the clause."""

    target = Str(required=True, example='id',
                 description='The field to compare.')
    expr = Str(required=True, example='apache',
               description='The expression to compare to the field.')


class QueryRequestClauseSchema(BaseSchema):
    """Represents a clause to filter a item based on various conditions."""

    _and = Nested('self', data_key='and', many=True,
                  description='All the clause has to be satisfied.')
    _or = Nested('self', data_key='or', many=True,
                 description='At least the clause has to be satisfied.')
    _not = Nested('self', data_key='not',
                  description='The clause has to be not satisfied.')
    lte = Nested(QueryRequestFilterSchema,
                 description='The target field must be lower or equal to the expr value..')  # noqa:E501
    gte = Nested(QueryRequestFilterSchema,
                 description='The target field must be greater or equal to the expr value.')  # noqa:E501
    lt = Nested(QueryRequestFilterSchema,
                description='The target field must be lower than the expr value.')  # noqa:E501
    gt = Nested(QueryRequestFilterSchema,
                description='The target field must be greater to the expr value.')  # noqa:E501
    equals = Nested(QueryRequestFilterSchema,
                    description='The target field must be equal to the expr value.')  # noqa:E501
    reg_exp = Nested(QueryRequestFilterSchema,
                     description='The target field must be satisfy the regular expression in expr.')  # noqa:E501
    wildcard = Nested(QueryRequestFilterSchema,
                      description='The target field must be satisfy the wildcard in expr.')  # noqa:E501


class QueryRequestSchema(BaseSchema):
    """Query request to filter the items."""

    select = ListOrOne(Str, example='id', description='Fields to return.',
                       validate=UniqueList.apply(),
                       error_messages=UniqueList.error_messages)
    where = Nested(QueryRequestClauseSchema,
                   description='Filter the items based on different conditions.')  # noqa: E501
    order = Nested(QueryRequestOrderSchema, many=True,
                   description='Order the filtered items.')
    limit = Nested(QueryRequestLimitSchema,
                   description='Limit the number of items to return.')
    force = Boolean(default=False, example=True,
                    description='Force the execution of the request even there are some errors (example: delete a inconsistent entries).')  # noqa: E501
