from document.exec_env.type import ExecEnvTypeDocument
from resource.base import BaseResource
from schema.exec_env.type import ExecEnvTypeSchema
from utils import swagger


@swagger(method='get',
         sum='Execution Environment Type Read (Single)',
         desc="""Get the execution environment type with the given `id` and filtered by the
                 query in the request body.""",
          resp='Execution environment type with the given `id` and filtered by the query in the request body.')
@swagger(method='post',
         sum='Execution Environment Type Creation (Single)',
         desc='Create new execution environment type with the given `id`.',
         resp='Execution environment type with the given `id` created.')
@swagger(method='delete',
         sum='Execution Environment Type Delete (Single)',
         desc="""Delete the execution environment type with the given `id` and filtered by
                 the query in the request body.""",
         resp="""Execution environment type with the given `id` and filtered by the query
                 in the request body deleted.""")
@swagger(method='put',
         sum='Execution Environment Type Update (Single)',
         desc='Update the execution environment type with the given `id`.',
         resp='Execution environment type with the given `id` updated.')
class ExecEnvTypeSelectedResource(BaseResource):
    doc_cls = ExecEnvTypeDocument
    doc_name = 'Execution Environment Type'
    routes = '/config/exec-env-type/{id}'
    schema_cls =ExecEnvTypeSchema

