from marshmallow import Schema
from marshmallow.fields import Nested, Raw, Str

from document.agent.catalog import AgentCatalogDocument
from document.agent.instance import AgentInstanceDocument
from document.exec_env import ExecEnvDocument
from schema.agent.catalog import AGENT_STATUS
from schema.base import BaseSchema
from schema.validate import In, UniqueList

OUTPUT_FORMATS = ["plain", "lines", "json"]


class AgentInstanceActionSchema(Schema):
    """Action of the agent instance installed in an execution environment."""

    id = Str(required=True, example="list", description="Action id.")
    output_format = Str(
        enum=OUTPUT_FORMATS,
        example=OUTPUT_FORMATS[1],
        default=OUTPUT_FORMATS[0],
        description="Output format for stdout and stderr "
        "result of action execution.",
    )  # noqa:E501


class AgentInstanceParameterSchema(Schema):
    """Parameter of the agent instance installed
    in an execution environment."""

    id = Str(required=True, example="period", description="Parameter id.")
    value = (
        Raw(required=True, example="10s", description="Paremeter value."),
    )


class AgentInstanceResourceSchema(Schema):
    """Resource of the agent instance installed in an execution environment."""

    id = Str(
        required=True, example="filebeat-config", description="Resource id."
    )
    content = Str(
        required=True, example="period: 10s", description="Resource content."
    )


class AgentInstanceOperationSchema(BaseSchema):
    """Represents the operations to perform with the agent instance
    installed in an execution environment."""

    actions = Nested(
        AgentInstanceActionSchema,
        many=True,
        unknown="INCLUDE",
        description="List of agent instance actions.",
    )
    parameters = Nested(
        AgentInstanceParameterSchema,
        many=True,
        unknown="INCLUDE",
        description="List of agent instance parameters.",
        validate=UniqueList.apply("id"),
        error_messages=UniqueList.error_messages,
    )
    resources = Nested(
        AgentInstanceResourceSchema,
        many=True,
        unknown="INCLUDE",
        description="List of agent instance resources.",
        validate=UniqueList.apply("id"),
        error_messages=UniqueList.error_messages,
    )


class AgentInstanceSchema(BaseSchema):
    """Represents an agent instance installed in an execution environment."""

    doc = AgentInstanceDocument
    id = Str(
        required=True,
        example="filebeat@apache",
        description="Id of the agent instance installed in an "
        "execution environment.",
    )  # noqa: E501
    agent_catalog_id = Str(
        required=True,
        readonly=True,
        example="filebeat",
        description="Id of the agent in the catalog.",
        validate=In.apply(AgentCatalogDocument.get_ids),
        error_messages=In.error_messages,
    )
    exec_env_id = Str(
        required=True,
        readonly=True,
        example="apache",
        description="Id of the execution environment where the agent "
        "instance is installed.",
        validate=In.apply(ExecEnvDocument.get_ids),
        error_messages=In.error_messages,
    )
    status = Str(
        enum=AGENT_STATUS,
        required=True,
        readonly=True,
        example=AGENT_STATUS[0],
        description="Status of the agent.",
    )
    operations = Nested(
        AgentInstanceOperationSchema,
        many=True,
        unknown="INCLUDE",
        description="List of agent instance operations.",
    )
    description = Str(
        example="Collect system metrics from execution environments.",
        description="Short description of the agent installed in "
        "the execution environment.",
    )  # noqa:E501
