from document.base import Base_Document
from elasticsearch_dsl import Date, InnerDoc as Inner_Doc, Nested, Text

__all__ = [
    'Agent_Instance_Document'
]


class Agent_Instance_Action_Inner_Doc(Inner_Doc):
    """Action of the agent instance installed in an execution environment."""
    id = Text(required=True)
    # data = Raw(required=True) # FIXME Raw?
    timestamp = Date(required=True)

class Agent_Instance_Parameter_Inner_Doc(Inner_Doc):
    """Parameter of the agent instance installed in an execution environment."""
    id = Text(required=True)
    # cvalue = Raw(required=True) # FIXME Raw?
    timestamp = Date(required=True)


class Agent_Instance_Resource_Inner_Doc(Inner_Doc):
    """Resource of the agent instance installed in an execution environment."""
    id = Text(required=True)
    path = Text(required=True)
    content = Text(required=True)
    timestamp = Date(required=True)


class Agent_Instance_Document(Base_Document):
    """Represents an agent instance installed in an execution environment."""
    # id already defined by Elasticsearch
    agent_catalog_id = Text(required=True)
    exec_env_id = Text(required=True)
    status = Text(required=True)
    actions = Nested(Agent_Instance_Action_Inner_Doc)
    parameters = Nested(Agent_Instance_Parameter_Inner_Doc)
    resources = Nested(Agent_Instance_Resource_Inner_Doc)
    description = Text()

    class Index:
        """Elasticsearch configuration."""
        name = 'agent-instance'

    def edit_action(self, action):
        so = self.Status_Operation
        id = action.get('id', None)
        for a in self.actions:
            dt = action.get('data', None)
            ts = action.get('timestamp', None)
            if a.id == id:
                if a.data != dt or a.timestamp != ts:
                    a.data = dt
                    a.timestamp = ts
                    return so.UPDATED
                return so.NOT_MODIFIED
        self.actions.append(Agent_Instance_Action_Inner_Doc(**action))
        return so.UPDATED

    def edit_parameter(self, parameter):
        so = self.Status_Operation
        id = parameter.get('id', None)
        for p in self.parameters:
            val = parameter.get('value', None)
            ts = parameter.get('timestamp', None)
            if p.id == id:
                if p.value != val or p.timestamp != ts:
                    p.value = val
                    p.timestamp = ts
                    return so.UPDATED
                return so.NOT_MODIFIED
        self.parameters.append(Agent_Instance_Parameter_Inner_Doc(**parameter))
        return so.UPDATED

    def edit_resource(self, data):
        so = self.Status_Operation
        id = data.get('id', None)
        for r in self.resources:
            path = data.get('path', None)
            cnt = data.get('content', None)
            ts = data.get('timestamp', None)
            if r.id == id:
                if r.id != id or r.path != path or r.content != cnt or r.timestamp != ts:
                    r.path = path
                    r.content = cnt
                    r.timestamp = ts
                    return so.UPDATED
                return so.NOT_MODIFIED
        self.resources.append(Agent_Instance_Resource_Inner_Doc(**data))
        return so.UPDATED
