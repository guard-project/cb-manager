from document.agent.instance import Agent_Instance_Document
from document.ebpf_program.instance import eBPF_Program_Instance_Document
from document.data import Data_Document
from marshmallow import Schema
from marshmallow.fields import DateTime as Date_Time, Str
from schema.agent.instance import Agent_Instance_Schema
from schema.base import Base_Schema
from schema.ebpf_program.instance import eBPF_Program_Instance_Schema
from schema.validate import In
from utils.datetime import FORMAT

__all__ = [
    'Data_Schema'
]


class Data_Schema(Base_Schema):
    """Represents the stored data."""
    doc = Data_Document

    id = Str(required=True, example='BXrHRn5RPU55Qh9JwMZn',
             description='Id of the data.')
    agent_instance_id = Str(readonly=True, example='filebeat@apache',
                            description="""Id of the agent instance in the execution environment
                                           that collected the data""",
                            validate=In.apply(Agent_Instance_Document.get_ids),
                            error_messages=In.error_messages)
    ebpf_program_instance_id = Str(readonly=True, example='packet-capture@apache',
                                   description="""Id of the eBPF program instance in the execution
                                                  environment that collected the data""",
                                   validate=In.apply(eBPF_Program_Instance_Document
                                                     .get_ids),
                                   error_messages=In.error_messages)
    timestamp_event = Date_Time(format=FORMAT, readonly=True, example='2019/02/14 15:23:30',
                                description='Timestamp of the event related to the collected data')
    timestamp_agent = Date_Time(format=FORMAT, readonly=True, example='2019/02/14 15:23:30',
                                description='Timestamp when the agent instance collected the data')
