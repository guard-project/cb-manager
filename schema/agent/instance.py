from document.agent.catalog import Agent_Catalog_Document
from document.agent.instance import Agent_Instance_Document
from document.exec_env import Exec_Env_Document
from marshmallow import Schema, validate, validates_schema
from marshmallow.fields import Bool, Constant, DateTime as Date_Time, Nested, Raw, Str
from schema.agent.catalog import Agent_Catalog_Schema, AGENT_STATUS
from schema.base import Base_Schema
from schema.exec_env import Exec_Env_Schema
from schema.validate import In, Unique_List
from utils.datetime import FORMAT

__all__ = [
    'Agent_Instance_Schema'
]


class Agent_Instance_Action_Schema(Schema):
    """Action of the agent instance installed in an execution environment."""

    id = Str(required=True, example='list',
             description='Action id.')
    data = Raw(example='drop: all',
               description='Action data.')
    timestamp = Date_Time(format=FORMAT, readonly=True,
                          description="Timestamp of the last time the action was executed correctly.")


class Agent_Instance_Parameter_Schema(Schema):
    """Parameter of the agent instance installed in an execution environment."""

    id = Str(required=True, example='period',
             description='Parameter id.')
    value = Raw(required=True, example='10s',
                description='Paremeter value.'),
    timestamp = Date_Time(format=FORMAT, readonly=True,
                          description="Timestamp of the last time the parameter was set correctly.")


class Agent_Instance_Resource_Schema(Schema):
    """Resource of the agent instance installed in an execution environment."""

    id = Str(required=True, example='/opt/firewall.xml',
             description='Resource path.')
    content = Str(required=True,
                  description='Resource content.')
    timestamp = Date_Time(format=FORMAT, readonly=True,
                          description="Timestamp of the last time the resource data was updated or created correctly.")


class Agent_Instance_Operation_Schema(Base_Schema):
    """Represents the operations to perform with the agent instance installed in an execution environment."""

    actions = Nested(Agent_Instance_Action_Schema, many=True, unknown='INCLUDE',
                     description='List of agent instance actions.',
                     validate=Unique_List.apply('id'),
                     error_messages=Unique_List.error_messages)
    parameters = Nested(Agent_Instance_Parameter_Schema, many=True, unknown='INCLUDE',
                        description='List of agent instance parameters.',
                        validate=Unique_List.apply('id'),
                        error_messages=Unique_List.error_messages)
    resources = Nested(Agent_Instance_Resource_Schema, many=True, unknown='INCLUDE',
                       description='List of agent instance resources.',
                       validate=Unique_List.apply('id'),
                       error_messages=Unique_List.error_messages)


class Agent_Instance_Schema(Base_Schema):
    """Represents an agent instance installed in an execution environment."""
    doc = Agent_Instance_Document

    id = Str(required=True, example='filebeat@apache',
             description='Id of the agent instance installed in an execution environment.')
    agent_catalog_id = Str(required=True, readonly=True, example='filebeat',
                           description='Id of the agent in the catalog.',
                           validate=In.apply(Agent_Catalog_Document.get_ids),
                           error_messages=In.error_messages)
    exec_env_id = Str(required=True, readonly=True, example='apache',
                      description='Id of the execution environment where the agent instance is installed.',
                      validate=In.apply(Exec_Env_Document.get_ids),
                      error_messages=In.error_messages)
    status = Str(required=True, readonly=True, enum=AGENT_STATUS, example=AGENT_STATUS[0],
                 description='Status of the agent instance',
                 validate=validate.OneOf(AGENT_STATUS))
    actions = Nested(Agent_Instance_Action_Schema, many=True, unknown='INCLUDE',
                     description='List of agent instance actions.',
                     validate=Unique_List.apply('id'),
                     error_messages=Unique_List.error_messages)
    parameters = Nested(Agent_Instance_Parameter_Schema, many=True, unknown='INCLUDE',
                        description='List of agent instance parameters.',
                        validate=Unique_List.apply('id'),
                        error_messages=Unique_List.error_messages)
    resources = Nested(Agent_Instance_Resource_Schema, many=True, unknown='INCLUDE',
                       description='List of agent instance resources.',
                       validate=Unique_List.apply('id'),
                       error_messages=Unique_List.error_messages)
    description = Str(example='Collect system metrics from execution environments.',
                      description='Short description of the agent installed in the execution environment.')
