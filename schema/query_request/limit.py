from marshmallow import Schema
from marshmallow.fields import Integer


class QueryRequestLimitSchema(Schema):
    """
    Limit the items to return.
    """
    _from = Integer(data_key='from',
                    description='Started index of the items to return.',
                    example=1)
    _to = Integer(data_key='to',
                  description='Ended index of the items to return.',
                  example=5)

