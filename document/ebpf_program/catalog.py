from elasticsearch_dsl import Boolean, Nested, Text

from document.base import BaseDocument, BaseInnerDoc


class _eBPFProgramCatalogConfigMetricOpenMetricsMetadataLabelInnerDoc(
    BaseInnerDoc
):
    """eBPF program open metrics label."""

    name = Text(required=True)
    value = Text(required=True)


class _eBPFProgramCatalogConfigMetricOpenMetricsMetadataInnerDoc(BaseInnerDoc):
    """eBPF program open metrics metadata."""

    type = Text(required=True)
    help = Text()
    labels = Nested(
        _eBPFProgramCatalogConfigMetricOpenMetricsMetadataLabelInnerDoc
    )


class _eBPFProgramCatalogConfigMetricInnerDoc(BaseInnerDoc):
    """eBPF program metric data."""

    name = Text(required=True)
    map_name = Text()  # FIXME required=True (map-name the correct name)
    open_metrics_metadata = Nested(
        _eBPFProgramCatalogConfigMetricOpenMetricsMetadataInnerDoc
    )  # noqa: E501


class _eBPFProgramCatalogConfigInnerDoc(BaseInnerDoc):
    """eBPF program parameter configuration."""

    code = Text(required=True)
    metrics = Nested(_eBPFProgramCatalogConfigMetricInnerDoc)


class _eBPFProgramCatalogParameterInnerDoc(BaseInnerDoc):
    """eBPF program parameter."""

    id = Text(required=True)
    # possible values: integer, number, string, choice, boolean
    type = Text(required=True)
    list = Boolean()
    values = Text()  # when type = choice
    description = Text()
    example = Text()


class _eBPFProgramCatalogDocument(BaseDocument):
    """Represents an eBPF program in the catalog."""

    # id already defined by Elasticsearch
    config = Nested(_eBPFProgramCatalogConfigInnerDoc, required=True)
    parameters = Nested(_eBPFProgramCatalogParameterInnerDoc)
    description = Text()

    class Index:
        """Elasticsearch configuration."""

        name = "ebpf-program-catalog"
