from agent_catalog import AgentCatalog
from app import api, ns_config
from document import Document
from elasticsearch_dsl import Text, Boolean
from error import Error
from exec_env import ExecEnv
from flask import request
from flask_api import status
from flask_restplus import fields, Resource
from validate import Validate

status_values = ['start', 'stop']

class AgentInstance(Document):
    agent_catalog_id = Text()
    exec_env_id = Text()
    status = Text()

    class Index:
        name = 'agent-instance'

    @staticmethod
    def get_name():
        return 'Agent instance'

    @staticmethod
    def get_url():
        return 'agent'

    @staticmethod
    def get_properties():
        return {
            'name': { 'check': Validate.is_name, 'reason': 'Name not valid', 'required': True },
            'agent_catalog_id': { 'check': AgentCatalog.exists, 'reason': f'{AgentCatalog.get_name()} not found', 'required': True },
            'exec_env_id': { 'check': ExecEnv.exists, 'reason': f'{ExecEnv.get_name()} not found', 'required': True },
            'status': { 'check': Validate.is_single_choice(*status_values), 'reason': f"Status not valid (acceptable values: {', '.join(status_values)})", 'required': False}
        }

    @staticmethod
    def apply(data):
        if 'status' not in data: data['status'] = 'stop'

ref = AgentInstance.init_with_try()

model = api.model(ref.Index.name, {
    'id':  fields.String(description ='Unique ID', required = True, example = 'filebeat-apache'),
    'agent_catalog_id': fields.String(description = f'AgentCatalog.get_name() ID', required = True, example = 'filebeat'),
    'exec_env_id': fields.String(description = f'{ExecEnv.get_name()} ID', required = True, example = 'exec-env-apache'),
    'status': fields.String(description = 'Status of the agent', required = False, enum = status_values)
}, description = f'Represent the agent instance installed in the {ExecEnv.get_name()}s', additionalProperties = True)

@ns_config.route(f'/{ref.get_url()}')
@ns_config.response(status.HTTP_401_UNAUTHORIZED, 'Unauthorized operation', Error.unauth_op_model)
@ns_config.response(status.HTTP_403_FORBIDDEN, 'Authentication required', Error.auth_model)
class AgentInstanceResource(Resource):
    @ns_config.doc(description = f'Get the list of all {ref.get_name()}s')
    @ns_config.response(status.HTTP_200_OK, f'List of {ref.get_name()}s', fields.List(fields.Nested(model)))
    def get(self):
        return ref.read_all()

    @ns_config.doc(description = f'Add a new {ref.get_name()}')
    @ns_config.expect(model, description = f'{ref.get_name()} to add', required = True)
    @ns_config.response(status.HTTP_201_CREATED, f'{ref.get_name()} correctly added', Document.response_model)
    @ns_config.response(status.HTTP_406_NOT_ACCEPTABLE, 'Request not acceptable', Error.not_acceptable_model)
    @ns_config.response(status.HTTP_409_CONFLICT, f'{ref.get_name()} with the same ID already found', Error.found_model)
    def post(self):
        return ref.created()

@ns_config.route(f'/{ref.get_url()}-id')
@ns_config.response(status.HTTP_401_UNAUTHORIZED, 'Unauthorized operation', Error.unauth_op_model)
@ns_config.response(status.HTTP_403_FORBIDDEN, 'Authentication required', Error.auth_model)
class AgentInstanceResource_id(Resource):
    @ns_config.doc(description = f'Get the list of all {ref.get_name()} IDs')
    @ns_config.response(status.HTTP_200_OK, f'List of {ref.get_name()} IDs', fields.List(fields.String(description = f'{ref.get_name()} ID', example = 'network-link-a')))
    def get(self):
        return ref.read_all_id()

@ns_config.route(f'/{ref.get_url()}/{ref.get_id_url()}')
@ns_config.response(status.HTTP_401_UNAUTHORIZED, 'Unauthorized operation', Error.unauth_op_model)
@ns_config.response(status.HTTP_403_FORBIDDEN, 'Authentication required', Error.auth_model)
@ns_config.response(status.HTTP_404_NOT_FOUND, f'{ref.get_name()} with the given ID not found', Error.found_model)
class AgentInstanceResource_sel(Resource):
    @ns_config.doc(description = f'Get the {ref.get_name()} with the given ID')
    @ns_config.response(status.HTTP_200_OK, f'{ref.get_name()} with the given ID', model)
    def get(self, id):
        return ref.read(id)

    @ns_config.doc(description = f'Update the {ref.get_name()} with the given ID')
    @ns_config.response(status.HTTP_202_ACCEPTED, f'{ref.get_name()} with the given ID currectly updated', Document.response_model)
    @ns_config.response(status.HTTP_406_NOT_ACCEPTABLE, 'Not acceptable request', Error.not_acceptable_model)
    def put(self, id):
        return ref.updated(id)

    @ns_config.doc(description = f'Delete the {ref.get_name()} with the given ID')
    @ns_config.response(status.HTTP_202_ACCEPTED, f'{ref.get_name()} with the given ID currectly deleted', Document.response_model)
    def delete(self, id):
        return ref.deleted(id)