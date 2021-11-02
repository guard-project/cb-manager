from elasticsearch_dsl import Date, InnerDoc, Nested, Text

from document.base import BaseDocument


class AlgorithmInstanceParameterInnerDoc(InnerDoc):
    """Parameter of the algorithm instance."""

    id = Text(required=True)
    timestamp = Date(required=True)
    # value


class AlgorithmInstanceDocument(BaseDocument):
    """Represents an algorithm instance."""

    # id already defined by Elasticsearch
    algorithm_catalog_id = Text(required=True)
    parameters = Nested(AlgorithmInstanceParameterInnerDoc)
    description = Text()

    class Index:
        """Elasticsearch configuration."""

        name = 'algorithm-instance'

    def edit_parameter(self, parameter):
        state_op = self.StatusOperation
        param_id = parameter.get('id', None)
        timestamp = parameter.get('timestamp', None)
        value = parameter.get('value', {})
        new_value = value.get('new', None)
        if new_value is not None:
            value['new'] = new_value = str(value['new'])  # FIXME improve
            value['old'] = str(value.get('old', None))
            for param in self.parameters:
                if param.id == param_id:
                    if param.value.new != new_value:
                        param.value = value
                        param.timestamp = timestamp
                        return state_op.UPDATED
                    return state_op.NOT_MODIFIED
            parameter.pop('type', None)
            parameter.pop('data', None)
            parameter['value'] = value
            self.parameters.append(
                AlgorithmInstanceParameterInnerDoc(**parameter))
            return state_op.UPDATED
        return state_op.NOT_MODIFIED
