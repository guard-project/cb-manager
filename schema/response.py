from http import HTTPStatus
from marshmallow import Schema
from marshmallow.fields import Dict, Integer, Raw, sString


class ResponseSchema(Schema):
    """
    Response for the item creation.
    """
    status = String(required=True,
                    enum=['created', 'noop', 'updated', 'deleted'],
                    description='Status of the operation.',
                    example='created')
    data = Dict(required=True,
                description='Data of the item.',
                keys=String(required=True,
                            description='Field name.',
                            example='id'),
                values=Raw(required=True,
                           description='Field value.'))
    http_status_code = Integer(required=True,
                               enum=[HTTPStatus.CREATED, HTTPStatus.OK],
                               description='HTTP Status Code',
                               example=HTTPStatus.CREATED)
