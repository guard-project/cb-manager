from elasticsearch_dsl import Date, Nested, Text

from document.base import BaseDocument, BaseInnerDoc


class AgentInstanceActionInnerDoc(BaseInnerDoc):
    """Action of the agent instance installed in an execution environment."""

    id = Text(required=True)
    timestamp = Date(required=True)


class AgentInstanceParameterValueInnerDoc(BaseInnerDoc):
    """Parameter value of the agent instanceInnerDoc installed
    in an execution environment."""

    new = Text(required=True)
    old = Text(required=True)


class AgentInstanceParameterInnerDoc(BaseInnerDoc):
    """Parameter of the agent instance installed
    in an execution environment."""

    id = Text(required=True)
    timestamp = Date(required=True)
    value = Nested(AgentInstanceParameterValueInnerDoc)


class AgentInstanceResourceInnerDoc(BaseInnerDoc):
    """Resource of the agent instance installed in an execution environment."""

    id = Text(required=True)
    timestamp = Date(required=True)
    content = Text(required=True)


class AgentInstanceDocument(BaseDocument):
    """Represents an agent instance installed in an execution environment."""

    # id already defined by Elasticsearch
    agent_catalog_id = Text(required=True)
    exec_env_id = Text(required=True)
    status = Text(required=True)
    actions = Nested(AgentInstanceActionInnerDoc)
    parameters = Nested(AgentInstanceParameterInnerDoc)
    resources = Nested(AgentInstanceResourceInnerDoc)
    description = Text()

    class Index:
        """Elasticsearch configuration."""

        name = "agent-instance"

    def edit_action(self, action):
        status_op = self.StatusOperation
        # FIXME avoid to pop field but insert in ES explicitly
        action.pop("type", None)
        self.actions.append(AgentInstanceActionInnerDoc(**action))
        return status_op.UPDATED

    def edit_parameter(self, parameter):
        status_op = self.StatusOperation
        param_id = parameter.get("id", None)
        timestamp = parameter.get("timestamp", None)
        value = parameter.get("value", {})
        val_new = value.get("new", None)
        val_old = value.get("old", None)
        if val_new is not None:
            val_new = str(val_new)
            val_old = str(val_old)
            for param in self.parameters:
                if param.id == param_id:
                    if param.value.new != val_new:
                        param.value.old = val_old
                        param.value.new = val_new
                        param.timestamp = timestamp
                        return status_op.UPDATED
                    return status_op.NOT_MODIFIED
            param_doc = AgentInstanceParameterInnerDoc
            value_doc = AgentInstanceParameterValueInnerDoc
            self.parameters.append(
                param_doc(
                    id=param_id,
                    timestamp=timestamp,
                    value=value_doc(new=val_new, old=val_old),
                )
            )
            return status_op.UPDATED
        return status_op.NOT_MODIFIED

    def edit_resource(self, resource):
        status_op = self.StatusOperation
        res_id = resource.get("id", None)
        timestamp = resource.get("timestamp", None)
        data = resource.get("data", {})
        cnt = data.get("content", None)
        for res in self.resources:
            if res.id == res_id:
                if res.content != cnt:
                    res.content = cnt
                    res.timestamp = timestamp
                    return status_op.UPDATED
                return status_op.NOT_MODIFIED
        _res_doc = AgentInstanceResourceInnerDoc
        self.resources.append(
            _res_doc(
                id=res_id,
                timestamp=timestamp,
                content=cnt))
        return status_op.UPDATED

    @staticmethod
    def from_agent_instance(agent_instance, exec_env_id):
        _id = agent_instance.pop("id", None)
        agent_instance.pop("type", None)
        agent_instance.pop("hasAgentType", None)
        agent_instance["exec_env_id"] = exec_env_id
        obj = AgentInstanceDocument.get_or_new(id=_id)
        for field, data in agent_instance.items():
            setattr(obj, field, data)
        obj.save()
