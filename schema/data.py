from marshmallow import Schema
from marshmallow.fields import DateTime, String


class DataSchema(Schema):
    """
    Represents stored data.
    """
    id = String(required=True,
                description='ID of the data.',
                example='BXrHRn5RPU55Qh9JwMZn')
    exec_env_id = String(description='ID of the execution environment where the data was collected',
                         example='apache')
    agent_instance_id = String(description="""ID of the agent instance in the execution environment
                                            that collected the data""",
                               example='apache')
    timestamp_event = DateTime(description='Timestamp of the event related to the collected data',
                               example='2019_02_14 15:23:30')
    timestamp_agent = DateTime(description='Timestamp when the agent instance collected the data',
                               example='2019_02_14 15:23:30')
