from marshmallow import Schema
from marshmallow.fields import Boolean
from marshmallow.fields import DateTime as Date_Time
from marshmallow.fields import Integer, Nested, Str

from document.exec_env import Exec_Env_Document, Exec_Env_Type_Document
from schema.base import Base_Schema
from schema.validate import In


class LCP_Schema(Schema):
    """Configuration of the LCP running in the execution environment."""

    port = Integer(required=True, example=5000, description='TCP port number of LCP in the execution environment.')
    started = Date_Time(readonly=True, example='2019/02/14 15:23:30', description='Timestamp when the LCP is started')
    last_heartbeat = Date_Time(reaonly=True, example='2019/02/14 15:23:33',
                               description='Timestamp of the expiration of the API access configuration.')


class Exec_Env_Schema(Base_Schema):
    """Represents an execution environment."""

    doc = Exec_Env_Document
    id = Str(required=True, example='apache', description='Id of the execution environment.')
    hostname = Str(required=True, example='192.168.1.2', description='Hostname of the execution environment.')
    type_id = Str(required=True, example='vm', description='Id of the execution environment type.',
                  validate=In.apply(Exec_Env_Type_Document.get_ids), error_messages=In.error_messages)
    lcp = Nested(LCP_Schema, readonly=True, unknown='INCLUDE', description='Data related to the LCP.')
    description = Str(example='Apache HTTP Web Server.', description='Short description of the execution environment,')
    enabled = Boolean(required=True, default=True, example='Yes',
                      description='Indicate if the execution environment is enabled or not')


class Exec_Env_Type_Schema(Base_Schema):
    """Represents an execution environment type."""

    doc = Exec_Env_Type_Document
    id = Str(required=True, example='vm', description='Id of the execution environment type.')
    name = Str(required=True, example='Virtual Machine', description='Name of the execution environment.')
    description = Str(example='Linux container.', description='Short description of the type.')
