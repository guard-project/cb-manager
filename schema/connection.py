from marshmallow import Schema
from marshmallow.fields import Nested, String


class ConnectionSchema(Schema):
    """
    Represents an connection between execution environments and network links.
    """
    id = String(required=True,
                description='ID of connection.',
                example='conn-1')
    exec_env_id = String(required=True,
                         description='ID of the connected execution environment',
                         example='apache')
    network_link_id = String(required=True,
                             description='ID of the connected network link',
                             example='net-link-1')
