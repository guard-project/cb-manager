from marshmallow.fields import Str

from document.network_link import Network_Link_Document, Network_Link_Type_Document
from schema.base import Base_Schema
from schema.validate import In


class Network_Link_Schema(Base_Schema):
    """Represents a network link."""

    doc = Network_Link_Document
    id = Str(required=True, example='net-link-1', description='Id of the network link.')
    type_id = Str(required=True, example='pnt2pnt', description='Id of the network link type.',
                  validate=In.apply(Network_Link_Type_Document.get_ids), error_messages=In.error_messages)
    description = Str(example='Allow communication between front-end and back-end services.',
                      description='Short description of the network link,')


class Network_Link_Type_Schema(Base_Schema):
    """Represents a network link type."""

    doc = Network_Link_Type_Document
    id = Str(required=True, example='pnt2pnt', description='Id of the network link type.')
    name = Str(required=True, readonly=True, example='Point to point', description='Name of the network link type.')
    description = Str(example='Communications connection between two communication endpoints.',
                      description='Short description of the network link type,')
