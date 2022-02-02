from marshmallow import Schema
from marshmallow.fields import Boolean, DateTime, Integer, Nested, Str

from document.exec_env import ExecEnvDocument, ExecEnvTypeDocument
from schema.base import BaseSchema
from schema.validate import In


class LCPSchema(Schema):
    """Configuration of the LCP running in the execution environment."""

    port = Integer(
        required=True,
        example=5000,
        description="TCP port number of LCP in the execution environment.",
    )  # noqa: E501
    https = Boolean(
        required=True,
        default=False,
        example=True,
        description="Communication with the LCP using HTTPS.",
    )
    endpoint = Str(
        example="lcp", description="URL Endpoint to connect with the LCP."
    )
    started = DateTime(
        readonly=True,
        example="2019/02/14 15:23:30",
        description="Timestamp when the LCP is started.",
    )
    last_heartbeat = DateTime(
        reaonly=True,
        example="2019/02/14 15:23:33",
        description="Timestamp of the expiration of the API access configuration.",
    )  # noqa: E501


class ExecEnvSchema(BaseSchema):
    """Represents an execution environment."""

    doc = ExecEnvDocument
    id = Str(
        required=True,
        example="apache",
        description="Id of the execution environment.",
    )
    hostname = Str(
        required=True,
        example="192.168.1.2",
        description="Hostname of the execution environment.",
    )
    type_id = Str(
        required=True,
        example="vm",
        description="Id of the execution environment type.",
        validate=In.apply(ExecEnvTypeDocument.get_ids),
        error_messages=In.error_messages,
    )
    lcp = Nested(
        LCPSchema,
        readonly=True,
        unknown="INCLUDE",
        description="Data related to the LCP.",
    )
    description = Str(
        example="Apache HTTP Web Server.",
        description="Short description of the execution environment,",
    )  # noqa: E501
    enabled = Boolean(
        required=True,
        default=True,
        example="Yes",
        description="Indicate if the execution environment is enabled or not",
    )  # noqa: E501


class ExecEnvTypeSchema(BaseSchema):
    """Represents an execution environment type."""

    doc = ExecEnvTypeDocument
    id = Str(
        required=True,
        example="vm",
        description="Id of the execution environment type.",
    )
    name = Str(
        required=True,
        example="Virtual Machine",
        description="Name of the execution environment.",
    )
    description = Str(
        example="Linux container.",
        description="Short description of the type.",
    )
