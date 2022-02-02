from marshmallow.fields import Str

from document.connection import ConnectionDocument
from document.exec_env import ExecEnvDocument
from document.network_link import NetworkLinkDocument
from schema.base import BaseSchema
from schema.validate import In


class ConnectionSchema(BaseSchema):
    """Represents an connection between execution
    environments and network links."""

    doc = ConnectionDocument
    id = Str(required=True, example="conn-1", description="Id of connection.")
    exec_env_id = Str(
        required=True,
        readonly=True,
        example="apache",
        description="Id of the connected execution environment.",
        validate=In.apply(ExecEnvDocument.get_ids),
        error_messages=In.error_messages,
    )
    network_link_id = Str(
        required=True,
        readonly=True,
        example="net-link-1",
        description="Id of the connected network link.",
        validate=In.apply(NetworkLinkDocument.get_ids),
        error_messages=In.error_messages,
    )
    description = Str(
        example="Added to this network for debug purposes.",
        description="Short description of the connection.",
    )
