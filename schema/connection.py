from document.connection import Connection_Document
from document.exec_env import Exec_Env_Document
from document.network_link import Network_Link_Document
from marshmallow import Schema
from marshmallow.fields import Str
from schema.exec_env import Exec_Env_Schema
from schema.network_link import Network_Link_Schema
from schema.base import Base_Schema
from schema.validate import In

__all__ = [
    'Connection_Schema'
]


class Connection_Schema(Base_Schema):
    """Represents an connection between execution environments and network links."""
    doc = Connection_Document

    id = Str(required=True, example='conn-1',
             description='Id of connection.')
    exec_env_id = Str(required=True, readonly=True, example='apache',
                      description='Id of the connected execution environment.',
                      validate=In.apply(Exec_Env_Document.get_ids),
                      error_messages=In.error_messages)
    network_link_id = Str(required=True, readonly=True, example='net-link-1',
                          description='Id of the connected network link.',
                          validate=In.apply(Network_Link_Document.get_ids),
                          error_messages=In.error_messages)
    description = Str(example='Added to this network for debug purposes.',
                      description='Short description of the connection.')
