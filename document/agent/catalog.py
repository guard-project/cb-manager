from elasticsearch_dsl import Boolean, InnerDoc, Nested, Text

from document.base import BaseDocument


class AgentCatalogActionConfigInnerDoc(InnerDoc):
    """Agent action configuration."""

    cmd = Text(required=True)
    args = Text()
    daemon = Boolean()


class AgentCatalogActionInnerDoc(InnerDoc):
    """Agent action."""

    config = Nested(AgentCatalogActionConfigInnerDoc, required=True)
    status = Text()
    description = Text()
    example = Text()


class AgentCatalogParameterConfigInnerDoc(InnerDoc):
    """Agent parameter configuration."""

    schema = Text(required=True)
    source = Text(required=True)
    path = Text(required=True)


class AgentCatalogParameterInnerDoc(InnerDoc):
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


class AgentCatalogResourceConfigInnerDoc(InnerDoc):
    """Agent resource configuration."""

    path = Text(required=True)


class AgentCatalogResourceInnerDoc(InnerDoc):
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

        name = 'agent-catalog'
