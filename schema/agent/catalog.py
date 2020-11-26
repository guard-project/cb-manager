from document.agent.catalog import Agent_Catalog_Document
from marshmallow import Schema, validate
from marshmallow.fields import Bool, List, Nested, Raw, Str
from schema.base import Base_Schema
from schema.validate import Unique_List

__all__ = [
    'Agent_Catalog_Schema'
]

AGENT_STATUS = ['started', 'stopped', 'unknown']
PARAMETER_SCHEMAS = ['properties', 'json', 'xml', 'yaml']
PARAMETER_TYPES = ['binary', 'boolean', 'choice',
                   'integer', 'number', 'time-duration', 'string']


class Agent_Catalog_Action_Config_Schema(Schema):
    """Agent action configuration."""

    cmd = Str(required=True, example='service filebeat start',
              description='Action command.')
    args = Str(many=True, example='-v',
               description='Action command argument')
    daemon = Bool(default=False, example=True,
                  description='Execute the command as daemon.')


class Agent_Catalog_Action_Schema(Schema):
    """Agent action."""

    id = Str(required=True, example='start',
             description='Action name')
    config = Nested(Agent_Catalog_Action_Config_Schema, unknown='INCLUDE', required=True,
                    description='Action config.')  # TODO unique?
    status = Str(enum=AGENT_STATUS, example=AGENT_STATUS[0],
                 description='Update the status the of the agent-instance if the command is executed correctly.',
                 validate=validate.OneOf(AGENT_STATUS))
    description = Str(example='Start the execution of the agent.',
                      description='Short description of the agent actions.')


class Agent_Catalog_Parameter_Config_Schema(Schema):
    """Agent parameter configuration."""

    schema = Str(required=True, enum=PARAMETER_SCHEMAS, example=PARAMETER_SCHEMAS[0],
                 description='Schema of the parameter file',
                 validate=validate.OneOf(PARAMETER_SCHEMAS))
    source = Str(required=True, example='/usr/share/filebeat/filebeat.yml',
                 description='Path of the source parameter file')
    path = List(Str(required=True, example='enabled',
                    description='Path of the parameter value in the file'))


class Agent_Catalog_Parameter_Schema(Schema):
    """Agent parameter."""

    id = Str(required=True, example='log-period',
             description='Parameter id.')
    type = Str(required=True, enum=PARAMETER_TYPES, example=PARAMETER_TYPES[0],
               description='Parameter type.',
               validate=validate.OneOf(PARAMETER_TYPES))
    config = Nested(Agent_Catalog_Parameter_Config_Schema, unknown='INCLUDE', required=True,
                    description='Parameter configuration.')
    list = Bool(default=False, example=True,
                description='Indicate if the parameter can have multiple values.')
    values = Str(many=True, example='mysql',
                 description='Possible values if the parameter type is choice.')
    description = Str(example='Enable the agent.',
                      description='Short description of the parameter.')
    example = Raw(example='10s',
                  description='Example of parameter value.')


class Agent_Catalog_Resource_Config_Schema(Schema):
    """Agent resource configuration."""

    path = Str(required=True, example='/usr/share/filebeat/filebeat.yml',
               description='File path.')


class Agent_Catalog_Resource_Schema(Schema):
    """Agent resource."""

    id = Str(required=True, example='filebeat-config',
             description='Resource id.')
    config = Nested(Agent_Catalog_Resource_Config_Schema, unknown='INCLUDE', required=True,
                    description='Resource configuration.')
    description = Str(example='Filebeat configuration file.',
                      description='Short description of the resource.')


class Agent_Catalog_Schema(Base_Schema):
    """Represents an agent in the catalog."""
    doc = Agent_Catalog_Document

    id = Str(required=True, example='filebeat',
             description='Id of the agent in the catalog.')
    actions = Nested(Agent_Catalog_Action_Schema, many=True, unknown='INCLUDE',
                     description='Action properties.',
                     validate=Unique_List.apply('id'),
                     error_messages=Unique_List.error_messages)
    parameters = Nested(Agent_Catalog_Parameter_Schema, many=True, unknown='INCLUDE',
                        description='Parameter properties.',
                        validate=Unique_List.apply('id'),
                        error_messages=Unique_List.error_messages)
    resources = Nested(Agent_Catalog_Resource_Schema, many=True, unknown='INCLUDE',
                       description='Resource properties.',
                       validate=Unique_List.apply('id'),
                       error_messages=Unique_List.error_messages)
    description = Str(example='Collect system metrics from execution environments.',
                      description='Short description of the agent.')
