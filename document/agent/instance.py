from elasticsearch_dsl import Date
from elasticsearch_dsl import InnerDoc as Inner_Doc
from elasticsearch_dsl import Nested, Text

from document.base import Base_Document


class Agent_Instance_Action_Inner_Doc(Inner_Doc):
    """Action of the agent instance installed in an execution environment."""

    id = Text(required=True)
    timestamp = Date(required=True)


class Agent_Instance_Parameter_Inner_Doc(Inner_Doc):
    """Parameter of the agent instance installed in an execution environment."""

    id = Text(required=True)
    timestamp = Date(required=True)
    # value


class Agent_Instance_Resource_Inner_Doc(Inner_Doc):
    """Resource of the agent instance installed in an execution environment."""

    id = Text(required=True)
    timestamp = Date(required=True)
    path = Text(required=True)
    content = Text(required=True)


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
        action.pop('type', None)
        self.actions.append(Agent_Instance_Action_Inner_Doc(**action))
        return so.UPDATED

    def edit_parameter(self, parameter):
        so = self.Status_Operation
        id = parameter.get('id', None)
        ts = parameter.get('timestamp', None)
        value = parameter.get('value', {})
        new_value = value.get('new', None)
        if new_value is not None:
            for p in self.parameters:
                if p.id == id:
                    if p.value.new != new_value or p.timestamp != ts:
                        p.value = value
                        p.timestamp = ts
                        return so.UPDATED
                    return so.NOT_MODIFIED
            parameter.pop('type', None)
            self.parameters.append(Agent_Instance_Parameter_Inner_Doc(**parameter))
            return so.UPDATED
        return so.NOT_MODIFIED

    def edit_resource(self, resource):
        so = self.Status_Operation
        id = resource.get('id', None)
        ts = resource.get('timestamp', None)
        data = resource.get('data', {})
        path = data.get('path', None)
        cnt = data.get('content', None)
        for r in self.resources:
            if r.id == id:
                if r.id != id or r.path != path or r.content != cnt or r.timestamp != ts:
                    r.path = path
                    r.content = cnt
                    r.timestamp = ts
                    return so.UPDATED
                return so.NOT_MODIFIED
        resource.pop('type', None)
        self.resources.append(Agent_Instance_Resource_Inner_Doc(**resource))
        return so.UPDATED
