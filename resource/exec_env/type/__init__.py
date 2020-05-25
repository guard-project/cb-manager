from document.exec_env.type import ExecEnvTypeDocument
from resource.base import BaseResource
from schema.exec_env.type import ExecEnvTypeSchema
from utils import swagger


@swagger(method='get',
         sum='Execution Environment Type Read (Multiple)',
         desc='Get the list of execution environment types filtered by the query in the request body.',
         resp='List of execution environment types filtered by the query in the request body.')
@swagger(method='post',
         sum='Execution Environment Type Creation (Multiple)',
         desc='Create new execution environment types.',
         resp='Execution environment types created.')
@swagger(method='delete',
         sum='Execution Environment Type Delete (Multiple)',
         desc='Delete execution environment types filtered by the query in the request body.',
         resp='Execution environment types filtered by the query in the request body deleted.')
@swagger(method='put',
         sum='Execution Environment Type Update (Multiple)',
         desc='Update execution environment types.',
         resp='Execution environment types updated.')
class ExecEnvTypeResource(BaseResource):
    doc_cls = ExecEnvTypeDocument
    doc_name = 'Execution Environment Type'
    routes = '/config/exec-env-type/'
    schema_cls =ExecEnvTypeSchema
