from marshmallow.fields import DateTime as Date_Time
from marshmallow.fields import Str

from document.agent.instance import AgentInstanceDocument
from document.data import DataDocument
from document.ebpf_program.instance import eBPFProgramInstanceDocument
from schema.base import BaseSchema
from schema.validate import In
from utils.datetime import FORMAT


class DataSchema(BaseSchema):
    """Represents the stored data."""

    doc = DataDocument
    id = Str(required=True, example='BXrHRn5RPU55Qh9JwMZn',
             description='Id of the data.')
    agent_instance_id = Str(readonly=True, example='filebeat@apache',
                            description='Id of the agent instance in the execution environment that collected the data',  # noqa: E501
                            validate=In.apply(AgentInstanceDocument.get_ids),
                            error_messages=In.error_messages)
    ebpf_program_instance_id = Str(readonly=True,
                                   example='packet-capture@apache',
                                   description='Id of the eBPF program instance in the execution environment that collected the data',  # noqa: E501
                                   validate=In.apply(
                                       eBPFProgramInstanceDocument.get_ids),
                                   error_messages=In.error_messages)
    timestamp_event = Date_Time(format=FORMAT, readonly=True,
                                example='2019/02/14 15:23:30',
                                description='Timestamp of the event related to the collected data')  # noqa:E501
    timestamp_agent = Date_Time(format=FORMAT, readonly=True,
                                example='2019/02/14 15:23:30',
                                description='Timestamp when the agent instance collected the data')  # noqa:E501
