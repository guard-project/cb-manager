from document.ebpf_program.catalog import eBPF_Program_Catalog_Document
from marshmallow import Schema, validate
from marshmallow.fields import Bool, Nested, Raw, Str
from schema.agent.catalog import PARAMETER_TYPES
from schema.base import Base_Schema
from schema.validate import Unique_List
from utils.schema import List_or_One

__all__ = [
    'eBPF_Program_Catalog_Schema'
]


class eBPF_Program_Catalog_Config_Metric_Open_Metrics_Metadata_Label_Schema(Schema):
    """eBPF program Open Metrics metadata label."""

    name = Str(required=True, example='IP_PROTO',
               description='Label name.')
    value = Str(required=True, example='UDP',
                description='Label value.')


class eBPF_Program_Catalog_Config_Metric_Open_Metrics_Metadata_Schema(Schema):
    """eBPF program Open Metrics metadata."""

    type = Str(required=True, example='counter',
               description='Metric type.')
    help = Str(example='This metric represents the number of packets that has travelled trough this probe.',
               description='Metric help.')
    labels = Nested(eBPF_Program_Catalog_Config_Metric_Open_Metrics_Metadata_Label_Schema, many=True, unknown='INCLUDE',
                    description='Labels of Open Metrics Metadata.',
                    validate=Unique_List.apply('name'),
                    error_messages=Unique_List.error_messages)


class eBPF_Program_Catalog_Config_Metric_Schema(Schema):
    """eBPF program metric."""

    name = Str(required=True, example='packets_total',
               description='Metric name.')
    map_name = Str(required=True, example='PKT_COUNTER',data_key='map-name',
                   description='Mapping value in the code.')
    open_metrics_metadata = Nested(eBPF_Program_Catalog_Config_Metric_Open_Metrics_Metadata_Schema,
                                   data_key='open-metrics-metadata',
                                   unknown='INCLUDE', description='Open Metrics Metadata.')


class eBPF_Program_Catalog_Config_Schema(Schema):
    """eBPF program configuration."""

    code = List_or_One(Str, required=True,
                       description='Code of the eBPF program.')
    metrics = Nested(eBPF_Program_Catalog_Config_Metric_Schema, many=True, unknown='INCLUDE',
                     description='eBPF program metrics.',
                     validate=Unique_List.apply('name'),
                     error_messages=Unique_List.error_messages)


class eBPF_Program_Catalog_Parameter_Schema(Schema):
    """eBPF program configuration."""

    id = Str(required=True, example='interface',
             description='Parameter id.')
    type = Str(required=True, description='Parameter type.', enum=PARAMETER_TYPES, example='integer',
               validate=validate.OneOf(PARAMETER_TYPES))
    list = Bool(default=False, example=True,
                description='Indicate if the parameter can have multiple values.')
    values = Str(many=True, example='yes',
                 description='Possible values if the parameter type is choice.')
    description = Str(example='Network Interface to attach.',
                      description='Short description of the parameter.')
    example = Raw(example='eno0',
                  description='Example of parameter value.')


class eBPF_Program_Catalog_Schema(Base_Schema):
    """Represents an eBPF program in the catalog."""
    doc = eBPF_Program_Catalog_Document

    id = Str(required=True, example='packet-capture',
             description='Id of the eBPF_Program_ in the catalog.')
    config = Nested(eBPF_Program_Catalog_Config_Schema,
                    required=True, unknown='INCLUDE')
    parameters = Nested(eBPF_Program_Catalog_Parameter_Schema, many=True, unknown='INCLUDE',
                        validate=Unique_List.apply('id'),
                        error_messages=Unique_List.error_messages)
    description = Str(example="""Transparent service to capture packets flowing through the interface it
                                 is attached to, apply filters and obtain capture in .pcap format.""",
                      description='Description of eBPF program.')
