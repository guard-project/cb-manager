from elasticsearch_dsl import Boolean, InnerDoc, Nested, Text

from document.base import BaseDocument


class eBPFProgramCatalogConfigMetricOpenMetricsMetadataLabelInnerDoc(InnerDoc):
    """eBPF program open metrics label."""

    name = Text(required=True)
    value = Text(required=True)


class eBPFProgramCatalogConfigMetricOpenMetricsMetadataInnerDoc(InnerDoc):
    """eBPF program open metrics metadata."""

    type = Text(required=True)
    help = Text()
    labels = Nested(
        eBPFProgramCatalogConfigMetricOpenMetricsMetadataLabelInnerDoc)


class eBPFProgramCatalogConfigMetricInnerDoc(InnerDoc):
    """eBPF program metric data."""

    name = Text(required=True)
    map_name = Text()  # FIXME required=True (map-name the correct name)
    open_metrics_metadata = Nested(eBPFProgramCatalogConfigMetricOpenMetricsMetadataInnerDoc)  # noqa: E501


class eBPFProgramCatalogConfigInnerDoc(InnerDoc):
    """eBPF program parameter configuration."""

    code = Text(required=True)
    metrics = Nested(eBPFProgramCatalogConfigMetricInnerDoc)


class eBPFProgramCatalogParameterInnerDoc(InnerDoc):
    """eBPF program parameter."""

    id = Text(required=True)
    # possible values: integer, number, string, choice, boolean
    type = Text(required=True)
    list = Boolean()
    values = Text()  # when type = choice
    description = Text()
    example = Text()


class eBPFProgramCatalogDocument(BaseDocument):
    """Represents an eBPF program in the catalog."""

    # id already defined by Elasticsearch
    config = Nested(eBPFProgramCatalogConfigInnerDoc, required=True)
    parameters = Nested(eBPFProgramCatalogParameterInnerDoc)
    description = Text()

    class Index:
        """Elasticsearch configuration."""

        name = 'ebpf-program-catalog'
