from elasticsearch_dsl import Boolean, Document, InnerDoc, Nested, Text


class AgentCatalogParameterConfigInnerDoc(InnerDoc):
    schema = Text(required=True)
    source = Text(required=True)
    path = Text(required=True)


class AgentCatalogParameterInnerDoc(InnerDoc):
    id = Text(required=True)
    # Possible values: integer, number, time-duration, string, choice, boolean, binary
    type = Text(required=True)
    list = Boolean()
    values = Text() # when choice = type
    example = Text()
    description = Text()
    config = Nested(AgentCatalogParameterConfigInnerDoc)


class AgentCatalogActionConfigInnerDoc(InnerDoc):
    cmd = Text(required=True)


class AgentCatalogActionInnerDoc(InnerDoc):
    config = Nested(AgentCatalogActionConfigInnerDoc)


class AgentCatalogDocument(Document):
    parameters = Nested(AgentCatalogParameterInnerDoc, required=True)
    actions = Nested(AgentCatalogActionInnerDoc, required=True)

    class Index:
        name = 'agent-catalog'
