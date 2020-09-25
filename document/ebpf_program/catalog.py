from document.base import Base_Document
from elasticsearch_dsl import Boolean, InnerDoc as Inner_Doc, Nested, Text

__all__ = [
    'eBPF_Program_Catalog_Document'
]


class eBPF_Program_Catalog_Config_Metric_Open_Metrics_Metadata_Label_Inner_Doc(Inner_Doc):
    """eBPF program open metrics label."""
    name = Text(required=True)
    value = Text(required=True)


class eBPF_Program_Catalog_Config_Metric_Open_Metrics_Metadata_Inner_Doc(Inner_Doc):
    """eBPF program open metrics metadata."""
    type = Text(required=True)
    help = Text()
    labels = Nested(eBPF_Program_Catalog_Config_Metric_Open_Metrics_Metadata_Label_Inner_Doc)


class eBPF_Program_Catalog_Config_Metric_Inner_Doc(Inner_Doc):
    """eBPF program metric data."""
    name = Text(required=True)
    map_name = Text(required=True)
    open_metrics_metadata = Nested(
        eBPF_Program_Catalog_Config_Metric_Open_Metrics_Metadata_Inner_Doc)


class eBPF_Program_Catalog_Config_Inner_Doc(Inner_Doc):
    """eBPF program parameter configuration."""
    code = Text(required=True)
    metrics = Nested(eBPF_Program_Catalog_Config_Metric_Inner_Doc)


class eBPF_Program_Catalog_Parameter_Inner_Doc(Inner_Doc):
    """eBPF program parameter."""
    id = Text(required=True)
    # possible values: integer, number, string, choice, boolean
    type = Text(required=True)
    list = Boolean()
    values = Text()  # when type = choice
    description = Text()
    example = Text()


class eBPF_Program_Catalog_Document(Base_Document):
    """Represents an eBPF program in the catalog."""
    # id already defined by Elasticsearch
    config = Nested(eBPF_Program_Catalog_Config_Inner_Doc, required=True)
    parameters = Nested(eBPF_Program_Catalog_Parameter_Inner_Doc)
    description = Text()

    class Index:
        """Elasticsearch configuration."""
        name = 'ebpf-program-catalog'
