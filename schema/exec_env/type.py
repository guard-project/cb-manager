from marshmallow import Schema
from marshmallow.fields import String


class ExecEnvTypeSchema(Schema):
    """
    Represents an execution environment type.
    """
    id = String(required=True,
                description='ID of the execution environment type.',
                example='vm')
    name = String(required=True,
                  description='Name of the execution environment.',
                  example='Virtual Machine')
