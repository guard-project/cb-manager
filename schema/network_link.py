from marshmallow.fields import Str

from document.network_link import NetworkLinkDocument, NetworkLinkTypeDocument
from schema.base import BaseSchema
from schema.validate import In


class NetworkLinkSchema(BaseSchema):
    """Represents a network link."""

    doc = NetworkLinkDocument
    id = Str(required=True, example="net-link-1", description="Id of the network link.")
    type_id = Str(
        required=True,
        example="pnt2pnt",
        description="Id of the network link type.",
        validate=In.apply(NetworkLinkTypeDocument.get_ids),
        error_messages=In.error_messages,
    )
    description = Str(
        example="Allow communication between front-end and back-end services.",  # noqa: E501
        description="Short description of the network link",
    )


class NetworkLinkTypeSchema(BaseSchema):
    """Represents a network link type."""

    doc = NetworkLinkTypeDocument
    id = Str(
        required=True, example="pnt2pnt", description="Id of the network link type."
    )
    name = Str(
        required=True,
        readonly=True,
        example="Point to point",
        description="Name of the network link type.",
    )
    description = Str(
        example="Communications connection between two communication endpoints.",  # noqa: E501
        description="Short description of the network link type.",
    )  # noqa: E501
