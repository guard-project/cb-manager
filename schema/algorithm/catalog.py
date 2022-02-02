from marshmallow import Schema, validate
from marshmallow.fields import Bool, Nested, Raw, Str

from document.algorithm.catalog import AlgorithmCatalogDocument
from schema.base import BaseSchema
from schema.validate import UniqueList
from utils.schema import ListOrOne

PARAMETER_TYPES = [
    "binary",
    "boolean",
    "choice",
    "integer",
    "number",
    "time-duration",
    "string",
]


class AlgorithmCatalogActionSchema(Schema):
    """Algorithm parameter."""

    id = Str(required=True, example="frequency", description="Action id.")
    description = Str(
        example="Start the algorithm.",
        description="Short description of the action.",
    )


class AlgorithmCatalogParameterSchema(Schema):
    """Algorithm parameter."""

    id = Str(required=True, example="frequency", description="Parameter id.")
    type = Str(
        required=True,
        enum=PARAMETER_TYPES,
        example=PARAMETER_TYPES[0],
        description="Parameter type.",
        validate=validate.OneOf(PARAMETER_TYPES),
    )
    list = Bool(
        default=False,
        example=True,
        description="Indicate if the parameter can have multiple values.",
    )  # noqa: E501
    values = ListOrOne(
        Str,
        example="mysql",
        description="Possible values if the parameter type is choice.",
    )  # noqa: E501
    description = Str(
        example="Enable the algorithm.",
        description="Short description of the parameter.",
    )
    example = Raw(example="10s", description="Example of parameter value.")


class AlgorithmCatalogSchema(BaseSchema):
    """Represents an algorithm in the catalog."""

    doc = AlgorithmCatalogDocument
    id = Str(
        required=True,
        example="ddos-prediction",
        description="Id of the algorithm in the catalog.",
    )
    actions = Nested(
        AlgorithmCatalogActionSchema,
        unknown="INCLUDE",
        many=True,
        description="Action properties.",
        validate=UniqueList.apply("id"),
        error_messages=UniqueList.error_messages,
    )
    parameters = Nested(
        AlgorithmCatalogParameterSchema,
        unknown="INCLUDE",
        many=True,
        description="Parameter properties.",
        validate=UniqueList.apply("id"),
        error_messages=UniqueList.error_messages,
    )
    encoding_scheme = Str(
        default="base64",
        example="base64",
        description="Encoding scheme used to store the binary data",
    )  # noqa: E501
    description = Str(
        example="Predict DDoS attacks.",
        description="Short description of the algorithm.",
    )
