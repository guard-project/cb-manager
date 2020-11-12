from document.base import Base_Document
from elasticsearch_dsl import Boolean, InnerDoc as Inner_Doc, Nested, Text

__all__ = [
    'Agent_Catalog_Document'
]

class Agent_Catalog_Action_Config_Inner_Doc(Inner_Doc):
    """Agent action configuration."""
    cmd = Text(required=True)
    args = Text()
    daemon = Boolean()


class Agent_Catalog_Action_Inner_Doc(Inner_Doc):
    """Agent action."""
    config = Nested(Agent_Catalog_Action_Config_Inner_Doc, required=True)
    status = Text()
    description = Text()
    example = Text()


class Agent_Catalog_Parameter_Config_Inner_Doc(Inner_Doc):
    """Agent parameter configuration."""
    schema = Text(required=True)
    source = Text(required=True)
    path = Text(required=True)


class Agent_Catalog_Parameter_Inner_Doc(Inner_Doc):
    """Agent parameter."""
    id = Text(required=True)
    # possible values: integer, number, time-duration, string, choice, boolean, binary
    type = Text(required=True)
    config = Nested(Agent_Catalog_Parameter_Config_Inner_Doc, required=True)
    list = Boolean()
    values = Text()  # when type = choice
    description = Text()
    example = Text()


class Agent_Catalog_Resource_Config_Inner_Doc(Inner_Doc):
    """Agent resource configuration."""
    path = Text(required=True)


class Agent_Catalog_Resource_Inner_Doc(Inner_Doc):
    """Agent resource."""
    id = Text(required=True)
    config = Nested(Agent_Catalog_Resource_Config_Inner_Doc, required=True)
    description = Text()
    example = Text()


class Agent_Catalog_Document(Base_Document):
    """Represents an agent in the catalog."""
    # id already defined by Elasticsearch
    actions = Nested(Agent_Catalog_Action_Inner_Doc)
    parameters = Nested(Agent_Catalog_Parameter_Inner_Doc)
    resources = Nested(Agent_Catalog_Resource_Inner_Doc)
    description = Text()

    class Index:
        """Elasticsearch configuration."""
        name = 'agent-catalog'
