from .config import ConfigResource
from .agent_catalog import AgentParameterDocument
from .exec_env_type import ExecEnvTypeDocument
from elasticsearch_dsl import Document, Text, Object


class ExecEnvDocument(Document):
    hostname = Text()
    type = Object(AgentParameterDocument, required=True)

    class Index:
        name = 'exec-env'


class ExecEnvResource(ConfigResource):
    doc_cls = ExecEnvDocument
    doc_name = 'Execution Environment'
