from marshmallow import Schema
from marshmallow.fields import Nested, String


class AgentInstanceParameterSchema(Schema):
    name = String(required=True,
                  description='Parameter name',
                  example='period')
    value = String(required=True,
                   description='Paremeter value',
                   example='10s')


class AgentInstanceSchema(Schema):
    """
    Represents an agent instance installed in an execution environment.
    """
    id = String(required=True,
                description='ID of the agent instance installed in an execution environment.',
                example='apache-filebeat')
    agent_catalog_id = String(required=True,
                              description='ID of the agent in the catalog',
                              example='filebeat')
    exec_env_id = String(required=True,
                         description='ID of the execution environment where the agent instance is installed',
                         example='apache')
    status = String(required=True,
                    enum=['start', 'stop'],
                    description='Status of the agent instance',
                    example='start')
    parameters = Nested(AgentInstanceParameterSchema,
                        many=True,
                        description='List of agent instance parameters')
