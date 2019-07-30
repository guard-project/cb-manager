from app import api
from datetime import datetime
from flask_api import status
from flask_restplus import abort, fields
from validate import Validate

class Error:
    unauth_op_model = api.model('unauthorized-operation-error-data', {
        'date': fields.DateTime(description = 'Response datetime', required = True),
        'message': fields.String(description = 'Human readible message that describes the error', required = True, example = 'Operation not allowed'),
    })

    auth_model = api.model('authentication-error-data', {
        'date': fields.DateTime(description = 'Response datetime', required = True),
        'message': fields.String(description = 'Human readible message that describes the error', required = True, example = 'Authentication required'),
    })

    not_acceptable_property_model = api.model('not-acceptable-property-error-data', {
        'property': fields.String(description = 'Name of the property', required = True, example = 'hostname'),
        'reason': fields.String(description = 'Reason for what the value is not acceptable', required = True, example = 'missing'),
        'value': fields.String(description = 'Not acceptable value', required = False, example = 3),
    })

    not_acceptable_model = api.model('not-acceptable-error-data', {
        'date': fields.DateTime(description = 'Response datetime', required = True),
        'message': fields.String(description = 'Human readible message that describes the error', required = True, example = 'Request not acceptable'),
        'target': fields.String(description = 'Object target of the operation', required = True, example = 'ExecEnv'),
        'data': fields.List(fields.Nested(not_acceptable_property_model), description = 'List of not acceptable properties', required = True)
    })

    found_model = api.model('found-error-data', {
        'date': fields.DateTime(description = 'Response datetime', required = True),
        'message': fields.String(description = 'Human readible message that describes the error', required = True, example = 'Network Link Type found'),
        'target': fields.String(description = 'Object name', required = True, example = 'NetworkLinkType'),
        'id': fields.String(description = 'ID of object instance', required = True, example = 'pnt-to-pnt')
    })

    exception_model = api.model('exception-error-data', {
        'date': fields.DateTime(description = 'Response datetime', required = True),
        'exception': fields.String(description = 'Exception message', required = True, example = 'Connection timeout')
    })

    def __init__(self, target):
        self.target = target

    def __abort(self, http_status_code, **kwargs):
        abort(http_status_code, date = datetime.now().strftime('%Y/%m/%d-%H:%M:%S'), **kwargs)

    def validate_properties(self, **data):
        not_accetable_data = []
        for prop, prop_data in self.target.get_properties().items():
            if prop not in data.keys():
                not_accetable_data.append({ 'property': prop, 'reason': 'missing' })
            elif not prop_data['check'](data[prop]):
                not_accetable_data.append({ 'property': prop, 'value': data[prop], 'reason': prop_data['reason'] })
        if len(not_accetable_data) > 0:
            self.__abort(status.HTTP_406_NOT_ACCEPTABLE, date = datetime.now(), message = f'{self.target.get_name()} request not acceptable',
                data = not_accetable_data, target = self.target.__name__)

    def found(self, id):
        self.__abort(status.HTTP_409_CONFLICT, date = datetime.now(), message = f'{self.target.get_name()} found', target = self.target.__name_, id = id)

    def not_found(self, id):
        self.__abort(status.HTTP_404_NOT_FOUND, date = datetime.now(), message = f'{self.target.get_name()} not found', target = self.target.__name_, id = id)

    def generic(self, exception):
        self.__abort(status.HTTP_500_INTERNAL_SERVER_ERROR, date = datetime.now(), exception = f'{exception}')
