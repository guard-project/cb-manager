from document.base import Base_Document
from elasticsearch_dsl import Date, InnerDoc as Inner_Doc, Nested, Text

__all__ = [
    'eBPF_Program_Instance_Document'
]

class eBPF_Program_Instance_Parameter_Inner_Doc(Inner_Doc):
    """Parameter of the eBPF Program instance installed in an execution environment."""
    id = Text(required=True)
    # value = Raw() # FIXME Raw?
    timestamp = Date(required=True)


class eBPF_Program_Instance_Document(Base_Document):
    """Represents an eBPF program installed in an execution environment."""
    # id already defined by Elasticsearch
    ebpf_program_catalog_id = Text(required=True)
    exec_env_id = Text(required=True)
    parameters = Nested(eBPF_Program_Instance_Parameter_Inner_Doc)
    description = Text()

    class Index:
        """Elasticsearch configuration."""
        name = 'ebpf-program-instance'

    def edit_parameter(self, parameter):
        so = self.Status_Operation
        id = parameter.get('id', None)
        for p in self.parameters:
            val = parameter.get('value', None)
            ts = parameter.get('timestamp', None)
            if p.id == id:
                if p.value != val or p.timestamp != ts:
                    p.value = val
                    p.timestamp = ts
                    return so.UPDATED
                return so.NOT_MODIFIED
        self.parameters.append(eBPF_Program_Instance_Parameter_Inner_Doc(**parameter))
        return so.UPDATED
