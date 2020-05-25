from marshmallow import Schema
from marshmallow.fields import Nested, String


class AgentCatalogActionConfigSchema(Schema):
    """
    Agent action configuration.
    """
    cmd = String(required=True,
                many=True,
                description='Action command',
                example='sudo service filebeat')


class AgentCatalogActionSchema(Schema):
    """
    Agent action.
    """
    id = String(required=True,
                enum=['start', 'stop'],
                description='Action name',
                example='start')
    config = Nested(AgentCatalogActionConfigSchema,
                    required=True,
                    many=True,
                    description='Action config')
