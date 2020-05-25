from marshmallow import Schema
from marshmallow.fields import String


class QueryRequestOrderSchema(Schema):
    """
    Order the filtered items.
    """
    target = String(required=True,
                    description='The field to compare.',
                    example='name')
    mode = String(enum=['asc', 'desc'],
                  required=True,
                  description='Order mode.',
                  example='asc')
