from elasticsearch_dsl import Boolean, Nested, Text

from document.base import BaseDocument, BaseInnerDoc


class AgentCatalogActionConfigInnerDoc(BaseInnerDoc):
    """Agent action configuration."""

    cmd = Text(required=True)
    args = Text()
    daemon = Boolean()


class AgentCatalogActionInnerDoc(BaseInnerDoc):
    """Agent action."""

    id = Text(required=True)
    config = Nested(AgentCatalogActionConfigInnerDoc, required=True)
    status = Text()
    description = Text()
    example = Text()

    @staticmethod
    def from_agent_type(agent_type, container):
        _id = agent_type.pop("id", None)
        cmd = agent_type.pop("cmd", None)
        obj = AgentCatalogActionInnerDoc.get_or_new(
            id=_id, container=container
        )
        for field, data in agent_type.items():
            setattr(obj, field, data)
        if cmd:
            obj.config = AgentCatalogActionConfigInnerDoc(cmd=cmd)
        return obj


class AgentCatalogParameterConfigInnerDoc(BaseInnerDoc):
    """Agent parameter configuration."""

    schema = Text(required=True)
    source = Text(required=True)
    path = Text(required=True)


class AgentCatalogParameterInnerDoc(BaseInnerDoc):
    """Agent parameter."""

    id = Text(required=True)
    # possible values: integer, number, time-duration,
    #                  string, choice, boolean, binary
    type = Text(required=True)
    config = Nested(AgentCatalogParameterConfigInnerDoc, required=True)
    list = Boolean()
    values = Text()  # when type = choice
    description = Text()
    example = Text()

    @staticmethod
    def from_agent_type(agent_type, container, schema, source):
        path = agent_type.pop("path", None)
        obj = AgentCatalogParameterInnerDoc.get_or_new(
            id=path, container=container
        )
        for field, data in agent_type.items():
            setattr(obj, field, data)
        obj.config = AgentCatalogParameterConfigInnerDoc(
            path=path, schema=schema, source=source
        )
        return obj


class AgentCatalogResourceConfigInnerDoc(BaseInnerDoc):
    """Agent resource configuration."""

    path = Text(required=True)


class AgentCatalogResourceInnerDoc(BaseInnerDoc):
    """Agent resource."""

    id = Text(required=True)
    config = Nested(AgentCatalogResourceConfigInnerDoc, required=True)
    description = Text()
    example = Text()


class AgentCatalogDocument(BaseDocument):
    """Represents an agent in the catalog."""

    # id already defined by Elasticsearch
    actions = Nested(AgentCatalogActionInnerDoc)
    parameters = Nested(AgentCatalogParameterInnerDoc)
    resources = Nested(AgentCatalogResourceInnerDoc)
    description = Text()
    deployment_source = Text()

    class Index:
        """Elasticsearch configuration."""

        name = "agent-catalog"

    @staticmethod
    def from_agent_type(agent_type):
        _id = agent_type.pop("id", None)
        source = agent_type.pop("source")
        schema = agent_type.pop("schema")
        obj = AgentCatalogDocument.get_or_new(id=_id)
        for action in agent_type.pop("actions", []):
            AgentCatalogActionInnerDoc.from_agent_type(
                action, container=obj.actions
            )
        for param in agent_type.pop("parameters", []):
            AgentCatalogParameterInnerDoc.from_agent_type(
                param, container=obj.parameters, schema=schema, source=source
            )
        for field, data in agent_type.items():
            setattr(obj, field, data)
        obj.save()
