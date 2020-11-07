from document.ebpf_program import *
from document.exec_env import Exec_Env_Document
from marshmallow import Schema
from marshmallow.fields import DateTime as Date_Time, Nested, Raw, Str
from schema.base import Base_Schema
from schema.ebpf_program.catalog import eBPF_Program_Catalog_Schema
from schema.exec_env import Exec_Env_Schema
from schema.validate import In, Unique_List
from utils.datetime import FORMAT

__all__ = [
    'eBPF_Program_Instance_Schema'
]


class eBPF_Program_Instance_Parameter_Schema(Schema):
    """Parameter of the eBPF program instance installed in an execution environment."""

    id = Str(required=True, example='interface',
             description='Parameter id.')
    value = Raw(required=True, example='en0',
                description='Paremeter value.'),
    timestamp = Date_Time(format=FORMAT, readonly=True,
                          description="Timestamp of the last time the parameter was set.")


class eBPF_Program_Instance_Schema(Base_Schema):
    """Represents an eBPF program instance installed in an execution environment."""
    doc = eBPF_Program_Instance_Document

    id = Str(required=True, example='packet-capture@apache',
             description='Id of the eBPF program installed in an execution environment.')
    ebpf_program_catalog_id = Str(required=True, readonly=True, example='packet-capture',
                                  description='Id of the agent in the catalog.',
                                  validate=In.apply(eBPF_Program_Catalog_Document
                                                    .get_ids),
                                  error_messages=In.error_messages)
    exec_env_id = Str(required=True, readonly=True, example='apache',
                      description="""Id of the execution environment where the eBPF program
                                     instance is installed""",
                      validate=In.apply(Exec_Env_Document.get_ids),
                      error_messages=In.error_messages)
    parameters = Nested(eBPF_Program_Instance_Parameter_Schema, many=True, unknown='INCLUDE',
                        description='List of eBPF program instance parameters.',
                        validate=Unique_List.apply('id'),
                        error_messages=Unique_List.error_messages)
    description = Str(example='Collect system metrics from Apache HTTP Web Server.',
                      description='Short description of the agent installed in the execution environment.')
