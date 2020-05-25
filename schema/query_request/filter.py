from marshmallow import Schema
from marshmallow.fields import String


class QueryRequestFilterSchema(Schema):
    """
    For numeric comparison in the clause.
    """
    target = String(required=True,
                    description='The field to compare.',
                    example='name')
    expr = String(required=True,
                  description='The expression to compare to the field.',
                  example='apache')
