from elasticsearch_dsl import Date
from elasticsearch_dsl import InnerDoc as Inner_Doc
from elasticsearch_dsl import Nested, Text

from document.base import Base_Document

__all__ = [
    'Algorithm_Instance_Document'
]


class Algorithm_Instance_Parameter_Inner_Doc(Inner_Doc):
    """Parameter of the algorithm instance."""
    id = Text(required=True)
    timestamp = Date(required=True)
    # value


class Algorithm_Instance_Document(Base_Document):
    """Represents an algorithm instance."""
    # id already defined by Elasticsearch
    algorithm_catalog_id = Text(required=True)
    parameters = Nested(Algorithm_Instance_Parameter_Inner_Doc)
    description = Text()

    class Index:
        """Elasticsearch configuration."""
        name = 'algorithm-instance'

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
            self.parameters.append(Algorithm_Instance_Parameter_Inner_Doc(**parameter))
            return so.UPDATED
        return so.NOT_MODIFIED
