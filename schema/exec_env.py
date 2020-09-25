from document.exec_env import Exec_Env_Document, Exec_Env_Type_Document
from marshmallow import Schema
from marshmallow.fields import DateTime as Date_Time, Integer, Nested, Str
from schema.base import Base_Schema
from schema.validate import In
from utils.datetime import FORMAT

__all__ = [
    'Exec_Env_Schema',
    'Exec_Env_Type_Schema'
]


class LCP_Schema(Schema):
    """Configuration of the LCP running in the execution environment."""

    port = Integer(required=True, example=5000,
                   description='TCP port number of LCP in the execution environment.')
    started = Date_Time(readonly=True, example='2019/02/14 15:23:30',
                        description='Timestamp when the LCP is started')
    last_heartbeat = Date_Time(reaonly=True, example='2019/02/14 15:23:33',
                               description='Timestamp of the expiration of the API access configuration.')
    username = Str(readonly=True, description='Username for the CB to connect to this LCP.')
    password = Str(readonly=True, description='Password for the CB to connect to this LCP.')


class Exec_Env_Schema(Base_Schema):
    """Represents an execution environment."""
    doc = Exec_Env_Document

    id = Str(required=True, example='apache',
             description='Id of the execution environment.')
    hostname = Str(required=True, example='192.168.1.2',
                   description='Hostname of the execution environment.')
    type_id = Str(required=True, example='vm',
                  description='Id of the execution environment type.',
                  validate=In.apply(Exec_Env_Type_Document.get_ids),
                  error_messages=In.error_messages)
    lcp = Nested(LCP_Schema, required=True, readonly=True, unknown='INCLUDE',
                 description='Data related to the LCP.')
    description = Str(example='Apache HTTP Web Server.',
                      description='Short description of the execution environment,')


class Exec_Env_Type_Schema(Base_Schema):
    """Represents an execution environment type."""
    doc= Exec_Env_Type_Document

    id = Str(required=True, example='vm',
             description='Id of the execution environment type.')
    name = Str(required=True, example='Virtual Machine',
               description='Name of the execution environment.')
    description = Str(example='Linux container.',
                      description='Short description of the type.')
