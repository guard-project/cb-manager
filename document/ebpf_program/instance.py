from elasticsearch_dsl import Date, InnerDoc, Nested, Text

from document.base import BaseDocument


class eBPFProgramInstanceParameterInnerDoc(InnerDoc):
    """Parameter of the eBPF Program instance installed
       in an execution environment."""

    id = Text(required=True)
    # value = Raw() # FIXME Raw?
    timestamp = Date(required=True)


class eBPFProgramInstanceDocument(BaseDocument):
    """Represents an eBPF program installed in an execution environment."""

    # id already defined by Elasticsearch
    ebpf_program_catalog_id = Text(required=True)
    exec_env_id = Text(required=True)
    parameters = Nested(eBPFProgramInstanceParameterInnerDoc)
    description = Text()

    class Index:
        """Elasticsearch configuration."""

        name = 'ebpf-program-instance'

    def edit_parameter(self, parameter):
        status_op = self.StatusOperation
        param_id = parameter.get('id', None)
        for param in self.parameters:
            val = parameter.get('value', None)
            timestamp = parameter.get('timestamp', None)
            if param.id == param_id:
                if param.value != val:
                    param.value = val
                    param.timestamp = timestamp
                    return status_op.UPDATED
                return status_op.NOT_MODIFIED
        self.parameters.append(
            eBPFProgramInstanceParameterInnerDoc(**parameter))
        return status_op.UPDATED
