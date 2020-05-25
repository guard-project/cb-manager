from marshmallow import Schema
from marshmallow.fields import String


class NetworkLinkTypeSchema(Schema):
    """
    Represents a network link type.
    """
    id = String(required=True,
                description='ID of the network link type.',
                example='pnt2pnt')
    name = String(required=True,
                  description='Name of the network link type.',
                  example='Point to point')
