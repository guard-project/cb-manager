from marshmallow import Schema
from marshmallow.fields import Nested, Raw, Str

from document.algorithm.catalog import Algorithm_Catalog_Document
from document.algorithm.instance import Algorithm_Instance_Document
from document.exec_env import Exec_Env_Document
from schema.base import Base_Schema
from schema.validate import In, Unique_List

__all__ = [
    'Algorithm_Instance_Schema'
]


class Algorithm_Instance_Parameter_Schema(Schema):
    """Parameter of the algorithm instance."""

    id = Str(required=True, example='period',
             description='Parameter id.')
    value = Raw(required=True, example='10s',
                description='Paremeter value.'),


class Algorithm_Instance_Operation_Schema(Base_Schema):
    """Represents the operations to perform with the algorithm instance."""

    parameters = Nested(Algorithm_Instance_Parameter_Schema, many=True, unknown='INCLUDE',
                        description='List of algorithm instance parameters.',
                        validate=Unique_List.apply('id'),
                        error_messages=Unique_List.error_messages)


class Algorithm_Instance_Schema(Base_Schema):
    """Represents an algorithm instance."""
    doc = Algorithm_Instance_Document

    id = Str(required=True, example='ddos-predictor-1',
             description='Id of the algorithm instance.')
    algorithm_catalog_id = Str(required=True, readonly=True, example='ddos-predictor',
                               description='Id of the algorithm in the catalog.',
                               validate=In.apply(
                                   Algorithm_Catalog_Document.get_ids),
                               error_messages=In.error_messages)
    exec_env_id = Str(required=True, readonly=True, example='apache',
                      description='Id of the execution environment where the algorithm instance is installed.',
                      validate=In.apply(Exec_Env_Document.get_ids),
                      error_messages=In.error_messages)
    operations = Nested(Algorithm_Instance_Operation_Schema, unknown='INCLUDE',
                        description='List of algorithm instance operations.')
    description = Str(example='Collect system metrics from execution environments.',
                      description='Short description of the algorithm installed in the execution environment.')
