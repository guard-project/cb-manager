from typing import Callable

from falcon.errors import (
    HTTPBadRequest,
    HTTPInternalServerError,
    HTTPUnsupportedMediaType,
)

from lib.response import (
    BadRequestResponse,
    InternalServerErrorResponse,
    UnsuppMediaTypeResponse,
)


class BaseHandler(object):
    error: Exception
    response: Callable

    @classmethod
    def handler(cls, _, resp, ex: Exception, __) -> None:
        cls.response(exception=ex).apply(resp)
        resp.complete = True

    @classmethod
    def get(cls):
        return cls.error, cls.handler


class BadRequestHandler(BaseHandler):
    error = HTTPBadRequest
    response = BadRequestResponse


class InternalServerErrorHandler(BaseHandler):
    error = HTTPInternalServerError
    response = InternalServerErrorResponse


class UnsupportedMediaTypeHandler(BaseHandler):
    error = HTTPUnsupportedMediaType
    response = UnsuppMediaTypeResponse
