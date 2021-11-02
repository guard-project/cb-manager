from marshmallow import Schema
from marshmallow.fields import Nested, Raw, Str

from document.algorithm.catalog import AlgorithmCatalogDocument
from document.algorithm.instance import AlgorithmInstanceDocument
from schema.base import BaseSchema
from schema.validate import In, UniqueList


class AlgorithmInstanceParameterSchema(Schema):
    """Parameter of the algorithm instance."""

    id = Str(required=True, example='period', description='Parameter id.')
    value = Raw(required=True, example='10s', description='Paremeter value.'),


class AlgorithmInstanceOperationSchema(BaseSchema):
    """Represents the operations to perform with the algorithm instance."""

    parameters = Nested(AlgorithmInstanceParameterSchema, many=True,
                        unknown='INCLUDE',
                        description='List of algorithm instance parameters.',
                        validate=UniqueList.apply('id'),
                        error_messages=UniqueList.error_messages)


class AlgorithmInstanceSchema(BaseSchema):
    """Represents an algorithm instance."""

    doc = AlgorithmInstanceDocument
    id = Str(required=True, example='ddos-predictor-1',
             description='Id of the algorithm instance.')
    algorithm_catalog_id = Str(required=True, readonly=True,
                               example='ddos-predictor',
                               description='Id of the algorithm in the catalog.',  # noqa: E501
                               validate=In.apply(
                                   AlgorithmCatalogDocument.get_ids),
                               error_messages=In.error_messages)
    operations = Nested(AlgorithmInstanceOperationSchema,
                        unknown='INCLUDE', many=True,
                        description='List of algorithm instance operations.')
    description = Str(example='Collect system metrics from execution environments.',  # noqa: E501
                      description='Short description of the algorithm installed in the execution environment.')  # noqa:E501
