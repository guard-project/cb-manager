from marshmallow import Schema
from marshmallow.fields import DateTime as Date_Time
from marshmallow.fields import Nested, Raw, Str

from document.ebpf_program.catalog import _eBPFProgramCatalogDocument
from document.ebpf_program.instance import _eBPFProgramInstanceDocument
from document.exec_env import ExecEnvDocument
from schema.base import BaseSchema
from schema.validate import In, UniqueList
from utils.datetime import FORMAT


class _eBPFProgramInstanceParameterSchema(Schema):
    """Parameter of the eBPF program instance
       installed in an execution environment."""

    id = Str(required=True, example='interface', description='Parameter id.')
    value = Raw(required=True, example='en0', description='Paremeter value.'),
    timestamp = Date_Time(format=FORMAT, readonly=True,
                          description='Timestamp of the last time the parameter was set.')  # noqa:E501


class _eBPFProgramInstanceSchema(BaseSchema):
    """Represents an eBPF program instance installed
       in an execution environment."""

    doc = _eBPFProgramInstanceDocument

    id = Str(required=True, example='packet-capture@apache',
             description='Id of the eBPF program installed in an execution environment.')  # noqa: E501
    ebpf_program_catalog_id = Str(required=True, readonly=False,
                                  example='packet-capture',
                                  description='Id of the agent in the catalog.',  # noqa: E501
                                  validate=In.apply(
                                      _eBPFProgramCatalogDocument.get_ids),
                                  error_messages=In.error_messages)
    exec_env_id = Str(required=True, readonly=True, example='apache',
                      description='Id of the execution environment where the eBPF program instance is installed',  # noqa: E501
                      validate=In.apply(ExecEnvDocument.get_ids),
                      error_messages=In.error_messages)
    parameters = Nested(_eBPFProgramInstanceParameterSchema, many=True,
                        unknown='INCLUDE',
                        description='List of eBPF program instance parameters.',  # noqa: E501
                        validate=UniqueList.apply('id'),
                        error_messages=UniqueList.error_messages)
    description = Str(example='Collect system metrics from Apache HTTP Web Server.',  # noqa: E501
                      description='Short description of the agent installed in the execution environment.')   # noqa: E501
