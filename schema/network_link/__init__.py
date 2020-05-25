from marshmallow import Schema
from marshmallow.fields import String


class NetworkLinkSchema(Schema):
    """
    Represents a network link.
    """
    id = String(required=True,
                description='ID of the network link.',
                example='net-link-1')
    type_id = String(required=True,
                     description='ID of the network link type.',
                     example='pnt2pnt')
