from marshmallow import Schema, validate
from marshmallow.fields import Bool, Nested, Raw, Str

from document.algorithm.catalog import Algorithm_Catalog_Document
from schema.base import Base_Schema
from schema.validate import Unique_List

__all__ = [
    'Algorithm_Catalog_Schema'
]

PARAMETER_TYPES = ['binary', 'boolean', 'choice',
                   'integer', 'number', 'time-duration', 'string']


class Algorithm_Catalog_Parameter_Schema(Schema):
    """Algorithm parameter."""

    id = Str(required=True, example='frequency',
             description='Parameter id.')
    type = Str(required=True, enum=PARAMETER_TYPES, example=PARAMETER_TYPES[0],
               description='Parameter type.',
               validate=validate.OneOf(PARAMETER_TYPES))
    list = Bool(default=False, example=True,
                description='Indicate if the parameter can have multiple values.')
    values = Str(many=True, example='mysql',
                 description='Possible values if the parameter type is choice.')
    description = Str(example='Enable the algorithm.',
                      description='Short description of the parameter.')
    example = Raw(example='10s',
                  description='Example of parameter value.')


class Algorithm_Catalog_Schema(Base_Schema):
    """Represents an algorithm in the catalog."""
    doc = Algorithm_Catalog_Document

    id = Str(required=True, example='ddos-prediction',
             description='Id of the algorithm in the catalog.')
    parameters = Nested(Algorithm_Catalog_Parameter_Schema, many=True, unknown='INCLUDE',
                        description='Parameter properties.',
                        validate=Unique_List.apply('id'),
                        error_messages=Unique_List.error_messages)
    description = Str(example='Predict DDoS attacks.',
                      description='Short description of the algorithm.')
