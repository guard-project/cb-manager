from marshmallow import Schema, validate
from marshmallow.fields import Bool, Nested, Raw, Str

from document.agent.catalog import AgentCatalogDocument
from schema.base import BaseSchema
from schema.validate import UniqueList
from utils.schema import ListOrOne

AGENT_STATUS = ["started", "stopped", "unknown"]
PARAMETER_SCHEMAS = ["properties", "json", "xml", "yaml"]
PARAMETER_TYPES = [
    "binary",
    "boolean",
    "choice",
    "integer",
    "number",
    "time-duration",
    "string",
]


class AgentCatalogActionConfigSchema(Schema):
    """Agent action configuration."""

    cmd = Str(
        required=True, example="service filebeat start", description="Action command."
    )
    args = ListOrOne(Str, example="-v", description="Action command argument")
    daemon = Bool(
        default=False, example=True, description="Execute the command as daemon."
    )


class AgentCatalogActionSchema(Schema):
    """Agent action."""

    id = Str(required=True, example="start", description="Action name")
    # TODO unique?
    config = Nested(
        AgentCatalogActionConfigSchema,
        unknown="INCLUDE",
        required=True,
        description="Action config.",
    )
    status = Str(
        enum=AGENT_STATUS,
        example=AGENT_STATUS[0],
        description="Update the status the of the agent-instance if the command is executed correctly.",  # noqa:E501
        validate=validate.OneOf(AGENT_STATUS),
    )
    description = Str(
        example="Start the execution of the agent.",
        description="Short description of the agent actions.",
    )


class AgentCatalogParameterConfigSchema(Schema):
    """Agent parameter configuration."""

    schema = Str(
        required=True,
        enum=PARAMETER_SCHEMAS,
        example=PARAMETER_SCHEMAS[0],
        description="Schema of the parameter file",
        validate=validate.OneOf(PARAMETER_SCHEMAS),
    )
    source = Str(
        required=True,
        example="/usr/share/filebeat/filebeat.yml",
        description="Path of the source parameter file",
    )
    path = ListOrOne(
        Str,
        required=True,
        example="enabled",
        description="Path of the parameter value in the file",
    )


class AgentCatalogParameterSchema(Schema):
    """Agent parameter."""

    id = Str(required=True, example="log-period", description="Parameter id.")
    type = Str(
        required=True,
        enum=PARAMETER_TYPES,
        example=PARAMETER_TYPES[0],
        description="Parameter type.",
        validate=validate.OneOf(PARAMETER_TYPES),
    )
    config = Nested(
        AgentCatalogParameterConfigSchema,
        unknown="INCLUDE",
        required=True,
        description="Parameter configuration.",
    )
    list = Bool(
        default=False,
        example=True,
        description="Indicate if the parameter can have multiple values.",
    )  # noqa: E501
    values = ListOrOne(
        Str,
        example="mysql",
        description="Possible values if the parameter type is choice.",
    )  # noqa: E501
    description = Str(
        example="Enable the agent.", description="Short description of the parameter."
    )
    example = Raw(example="10s", description="Example of parameter value.")


class AgentCatalogResourceConfigSchema(Schema):
    """Agent resource configuration."""

    path = ListOrOne(
        Str,
        required=True,
        example="/usr/share/filebeat/filebeat.yml",
        description="File path.",
    )


class AgentCatalogResourceSchema(Schema):
    """Agent resource."""

    id = Str(required=True, example="filebeat-config", description="Resource id.")
    config = Nested(
        AgentCatalogResourceConfigSchema,
        unknown="INCLUDE",
        required=True,
        description="Resource configuration.",
    )
    description = Str(
        example="Filebeat configuration file.",
        description="Short description of the resource.",
    )


class AgentCatalogSchema(BaseSchema):
    """Represents an agent in the catalog."""

    doc = AgentCatalogDocument
    id = Str(
        required=True, example="filebeat", description="Id of the agent in the catalog."
    )
    actions = Nested(
        AgentCatalogActionSchema,
        unknown="INCLUDE",
        many=True,
        description="Action properties.",
        validate=UniqueList.apply("id"),
        error_messages=UniqueList.error_messages,
    )
    parameters = Nested(
        AgentCatalogParameterSchema,
        unknown="INCLUDE",
        many=True,
        description="Parameter properties.",
        validate=UniqueList.apply("id"),
        error_messages=UniqueList.error_messages,
    )
    resources = Nested(
        AgentCatalogResourceSchema,
        unknown="INCLUDE",
        many=True,
        description="Resource properties.",
        validate=UniqueList.apply("id"),
        error_messages=UniqueList.error_messages,
    )
    description = Str(
        example="Collect system metrics from execution environments.",  # noqa: E501
        description="Short description of the agent.",
    )
    deployment_source = ListOrOne(
        Str,
        example="https://www.example.com/k8s-artefact.yaml",  # noqa: E501
        description="Link to the deployment sources",
    )
