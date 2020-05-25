from elasticsearch_dsl import Document, InnerDoc, Nested, Text


class AgentInstanceParameterInnerDoc(InnerDoc):
    value = Text(required=True)


class AgentInstanceDocument(Document):
    agent_catalog_id = Text(required=True)
    exec_env_id = Text(required=True)
    status = Text(required=True)
    parameters = Nested(AgentInstanceParameterInnerDoc)

    class Index:
        name = 'agent-instance'
