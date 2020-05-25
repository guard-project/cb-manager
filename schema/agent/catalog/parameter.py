from marshmallow import Schema
from marshmallow.fields import Boolean, List, Nested, String


# TODO
class AgentCatalogParameterConfigSchema(Schema):
    """
    Agent parameter configuration.
    """
    schema = String(required=True)
    source = String(required=True)
    path = List(String())


class AgentCatalogParameterSchema(Schema):
    """
    Agent parameter.
    """
    id = String(required=True,
                description='Parameter id',
                example='log-period')
    type = String(required=True,
                  enum=['integer', 'number', 'time-duration',
                        'string', 'choice', 'boolean', 'binary'],
                  description='Parameter type.', example='integer')
    list = Boolean(description='Indicate if the parameter can have multiple values.',
                   example=True)
    values = List(String(example=['mysql', 'http']),
                  description='Possible values if the parameter type is choice.')
    config = Nested(AgentCatalogParameterConfigSchema,
                    required=True,
                    many=True,
                    description='Parameter recipe')

