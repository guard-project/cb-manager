from elasticsearch_dsl import Boolean
from elasticsearch_dsl import InnerDoc as Inner_Doc
from elasticsearch_dsl import Nested, Text

from document.base import Base_Document


class Algorithm_Catalog_Parameter_Inner_Doc(Inner_Doc):
    """Algorithm parameter."""

    id = Text(required=True)
    # possible values: integer, number, time-duration, string, choice, boolean, binary
    type = Text(required=True)
    list = Boolean()
    values = Text()  # when type = choice
    description = Text()
    example = Text()


class Algorithm_Catalog_Document(Base_Document):
    """Represents an algorithm in the catalog."""

    # id already defined by Elasticsearch
    parameters = Nested(Algorithm_Catalog_Parameter_Inner_Doc)
    description = Text()

    class Index:
        """Elasticsearch configuration."""

        name = 'algorithm-catalog'
