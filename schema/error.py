from http import HTTPStatus
from marshmallow import Schema
from marshmallow.fields import Integer, String


class ErrorSchema(Schema):
    """
    Response in case of error.
    """
    status = String(required=True,
                    enum=['error'],
                    description='Indicate an error',
                    example='error')
    reason = String(required=True,
                    description='Human readable message that describes the error.',
                    example='Request not valid: two ids provided')
    id = String(required=True,
                description='id of the item.')
    http_status_code = Integer(required=True,
                               enum=[HTTPStatus.CONFLICT],
                               description='HTTP Status code',
                               example=HTTPStatus.CONFLICT)
