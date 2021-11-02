from marshmallow import Schema, validate
from marshmallow.fields import Bool, Constant, Integer, Nested, Raw, Str

from lib.response import (BadRequestResponse, ConflictResponse,
                          ContentResponse, CreatedResponse,
                          InternalServerErrorResponse, NoContentResponse,
                          NotAcceptableResponse, NotFoundResponse,
                          NotModifiedResponse, OkResponse,
                          ResetContentResponse, UnauthorizedResponse,
                          UnprocEntityResponse, UnsuppMediaTypeResponse)

RESPONSE_STATUS = [
    BadRequestResponse.status(),
    ConflictResponse.status(),
    ContentResponse.status(),
    CreatedResponse.status(),
    NoContentResponse.status(),
    NotAcceptableResponse.status(),
    NotFoundResponse.status(),
    NotModifiedResponse.status(),
    OkResponse.status(),
    ResetContentResponse.status(),
    UnauthorizedResponse.status(),
    UnprocEntityResponse.status(),
    UnsuppMediaTypeResponse.status()
]

RESPONSE_CODES = [
    BadRequestResponse.code,
    ConflictResponse.code,
    ContentResponse.code,
    CreatedResponse.code,
    NoContentResponse.code,
    NotAcceptableResponse.code,
    NotFoundResponse.code,
    NotModifiedResponse.code,
    OkResponse.code,
    ResetContentResponse.code,
    UnauthorizedResponse.code,
    UnprocEntityResponse.code,
    UnsuppMediaTypeResponse.code
]


class ExceptionResponseSchema(Schema):
    reason = Raw(required=True, example='Connection timeout',
                 description='Exception reason.')
    filename = Str(required=True, example='lib/connection.py',
                   description='Filename where the exception is raised.')
    line = Integer(required=True, example=80,
                   description='Line where the exception is raised.')


class BaseResponseSchema(Schema):
    """Response for the item creation."""

    status = Str(required=True, enum=RESPONSE_STATUS,
                 example=RESPONSE_STATUS[0],
                 description='HTTP Status Code phrase.',
                 validate=validate.OneOf(RESPONSE_STATUS))
    error = Bool(default=False, example=False,
                 description='Indicate the presence of an error')
    message = Str(required=True,
                  example='Request not valid: two ids provided.',
                  description='Human readable message that describes the status of the operation.')  # noqa:E501
    exception = Nested(ExceptionResponseSchema,
                       description='Message of the occurred exception.')
    code = Integer(required=True, enum=RESPONSE_CODES,
                   example=RESPONSE_CODES[0],
                   description='HTTP Status Code.',
                   validate=validate.OneOf(RESPONSE_CODES))


class BadRequestResponseSchema(BaseResponseSchema):
    status = Constant(constant=BadRequestResponse.status())
    error = Constant(constant=BadRequestResponse.error)
    code = Constant(constant=BadRequestResponse.code)


class ConflictResponseSchema(BaseResponseSchema):
    status = Constant(constant=ConflictResponse.status())
    error = Constant(constant=ConflictResponse.error)
    code = Constant(constant=ConflictResponse.code)


class CreatedResponseSchema(BaseResponseSchema):
    status = Constant(CreatedResponse.status())
    error = Constant(CreatedResponse.error)
    code = Constant(CreatedResponse.code)


class InternalServerErrorResponseSchema(BaseResponseSchema):
    status = Constant(InternalServerErrorResponse.status())
    error = Constant(InternalServerErrorResponse.error)
    code = Constant(InternalServerErrorResponse.code)


class NoContentResponseSchema(BaseResponseSchema):
    status = Constant(NoContentResponse.status())
    error = Constant(NoContentResponse.error)
    code = Constant(NoContentResponse.code)


class NotAcceptableResponseSchema(BaseResponseSchema):
    status = Constant(NotAcceptableResponse.status())
    error = Constant(NotAcceptableResponse.error)
    code = Constant(NotAcceptableResponse.code)


class NotFoundResponseSchema(BaseResponseSchema):
    status = Constant(NotFoundResponse.status())
    error = Constant(NotFoundResponse.error)
    code = Constant(NotFoundResponse.code)


class NotModifiedResponseSchema(BaseResponseSchema):
    status = Constant(NotModifiedResponse.status())
    error = Constant(NotModifiedResponse.error)
    code = Constant(NotModifiedResponse.code)


class OkResponseSchema(BaseResponseSchema):
    status = Constant(OkResponse.status())
    error = Constant(OkResponse.error)
    code = Constant(OkResponse.code)


class ContentResponseSchema(OkResponseSchema):
    status = Constant(ContentResponse.status())
    error = Constant(ContentResponse.error)
    code = Constant(ContentResponse.code)


class ResetContentResponseSchema(BaseResponseSchema):
    status = Constant(ResetContentResponse.status())
    error = Constant(ResetContentResponse.error)
    code = Constant(ResetContentResponse.code)


class UnauthorizedResponseSchema(BaseResponseSchema):
    status = Constant(UnauthorizedResponse.status())
    error = Constant(UnauthorizedResponse.error)
    code = Constant(UnauthorizedResponse.code)


class UnprocessableEntityResponseSchema(BaseResponseSchema):
    status = Constant(UnprocEntityResponse.status())
    error = Constant(UnprocEntityResponse.error)
    code = Constant(UnprocEntityResponse.code)


class UnsupportedMediaTypeResponseSchema(BaseResponseSchema):
    status = Constant(UnsuppMediaTypeResponse.status())
    error = Constant(UnsuppMediaTypeResponse.error)
    code = Constant(UnsuppMediaTypeResponse.code)
