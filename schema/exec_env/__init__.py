from marshmallow import Schema
from marshmallow.fields import DateTime, Integer, Nested, String


class LCPSchema(Schema):
    port = Integer(required=True,
                   description='TCP port number of LCP in the execution environment.',
                   example=5000)
    username = String(description='Username to connect from the CB to the LCP.',
                      example='22c6d368beabf9de1ea03e010010758a394c37c3b18aa0705b8634f5')
    password = String(description='Password to connect from the CB to the LCP.',
                      example='22c6d368beabf9de1ea03e010010758a394c37c3b18aa0705b8634f5')
    cb_password = String(description='Hashed password assigned to LCP to connect with the CB.',
                         example='22c6d368beabf9de1ea03e010010758a394c37c3b18aa0705b8634f5')
    cb_expiration = DateTime(description='Datetime until the authentication with the CB is valid.',
                             example='2019_02_14 15:23:30')
    last_hearbeat = DateTime(description='Timestamp of the last hearbeat between the LCP and CB.',
                             example='2019_02_14 15:23:30')


class ExecEnvSchema(Schema):
    """
    Represents an execution environment.
    """
    id = String(required=True,
                description='ID of the execution environment.',
                example='apache')
    hostname = String(required=True,
                      description='Hostname of the execution environment.',
                      example='192.168.1.2')
    lcp = Nested(LCPSchema,
                 required=True,
                 description='Data related to the LCP')
    type_id = String(required=True,
                     description='ID of the execution environment type.',
                     example='vm')
