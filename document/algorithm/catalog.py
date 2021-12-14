from elasticsearch_dsl import Boolean, Nested, Text

from document.base import BaseDocument, BaseInnerDoc


class AlgorithmCatalogParameterInnerDoc(BaseInnerDoc):
    """Algorithm parameter."""

    id = Text(required=True)
    # possible values: integer, number, time-duration,
    #                  string, choice, boolean, binary
    type = Text(required=True)
    list = Boolean()
    values = Text()  # when type = choice
    encoding_scheme = Text()
    description = Text()
    example = Text()


class AlgorithmCatalogDocument(BaseDocument):
    """Represents an algorithm in the catalog."""

    # id already defined by Elasticsearch
    parameters = Nested(AlgorithmCatalogParameterInnerDoc)
    description = Text()

    class Index:
        """Elasticsearch configuration."""

        name = 'algorithm-catalog'
