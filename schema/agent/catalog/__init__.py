from marshmallow import Schema
from marshmallow.fields import Nested, String
from schema.agent.catalog.parameter import AgentCatalogParameterSchema
from schema.agent.catalog.action import AgentCatalogActionSchema


class AgentCatalogSchema(Schema):
    """
    Represents an agent in the catalog.
    """
    id = String(required=True,
                description='ID of the agent in the catalog.',
                example='filebeat')
    parameters = Nested(AgentCatalogParameterSchema,
                        required=True,
                        many=True,
                        description='Parameter properties')
    actions = Nested(AgentCatalogActionSchema,
                     required=True,
                     many=True,
                     description='Action properties')
