from marshmallow import Schema, validate
from marshmallow.fields import Bool, Nested, Raw, Str

from document.ebpf_program.catalog import eBPFProgramCatalogDocument
from schema.agent.catalog import PARAMETER_TYPES
from schema.base import BaseSchema
from schema.validate import UniqueList
from utils.schema import ListOrOne


class eBPFProgramCatalogConfigMetricOpenMetricsMetadataLabelSchema(Schema):
    """eBPF program Open Metrics metadata label."""

    name = Str(required=True, example='IP_PROTO', description='Label name.')
    value = Str(required=True, example='UDP', description='Label value.')


class eBPFProgramCatalogConfigMetricOpenMetricsMetadataSchema(Schema):
    """eBPF program Open Metrics metadata."""

    type = Str(required=True, example='counter', description='Metric type.')
    help = Str(example='This metric represents the number of packets that has travelled trough this probe.',  # noqa: E501
               description='Metric help.')
    labels = Nested(eBPFProgramCatalogConfigMetricOpenMetricsMetadataLabelSchema,  # noqa: E501
                    many=True, unknown='INCLUDE',
                    description='Labels of Open Metrics Metadata.',
                    validate=UniqueList.apply('name'),
                    error_messages=UniqueList.error_messages)


class eBPFProgramCatalogConfigMetricSchema(Schema):
    """eBPF program metric."""

    name = Str(required=True, example='packets_total',
               description='Metric name.')
    map_name = Str(required=True, example='PKT_COUNTER', data_key='map-name',
                   description='Mapping value in the code.')
    open_metrics_metadata = Nested(eBPFProgramCatalogConfigMetricOpenMetricsMetadataSchema,  # noqa: E501
                                   data_key='open-metrics-metadata',
                                   unknown='INCLUDE',
                                   description='Open Metrics Metadata.')


class eBPFProgramCatalogConfigSchema(Schema):
    """eBPF program configuration."""

    code = ListOrOne(Str, required=True,
                     description='Code of the eBPF program.')
    metrics = Nested(eBPFProgramCatalogConfigMetricSchema, many=True,
                     unknown='INCLUDE', description='eBPF program metrics.',
                     validate=UniqueList.apply('name'),
                     error_messages=UniqueList.error_messages)


class eBPFProgramCatalogParameterSchema(Schema):
    """eBPF program configuration."""

    id = Str(required=True, example='interface', description='Parameter id.')
    type = Str(required=True, description='Parameter type.',
               enum=PARAMETER_TYPES, example='integer',
               validate=validate.OneOf(PARAMETER_TYPES))
    list = Bool(default=False, example=True,
                description='Indicate if the parameter can have multiple values.')  # noqa: E501
    values = ListOrOne(Str, example='yes',
                       description='Possible values if the parameter type is choice.')  # noqa: E501
    description = Str(example='Network Interface to attach.',
                      description='Short description of the parameter.')
    example = Raw(example='eno0', description='Example of parameter value.')


class eBPFProgramCatalogSchema(BaseSchema):
    """Represents an eBPF program in the catalog."""

    doc = eBPFProgramCatalogDocument
    id = Str(required=True, example='packet-capture',
             description='Id of the eBPF_Program_ in the catalog.')
    config = Nested(eBPFProgramCatalogConfigSchema,
                    required=True, unknown='INCLUDE')
    parameters = Nested(eBPFProgramCatalogParameterSchema, many=True,
                        unknown='INCLUDE', validate=UniqueList.apply('id'),
                        error_messages=UniqueList.error_messages)
    description = Str(example='Transparent service to capture packets flowing through the interface it is attached to, apply filters and obtain capture in .pcap format.',  # noqa: E501
                      description='Description of eBPF program.')
