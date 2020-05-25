from document.agent.instance import AgentInstanceDocument
from resource.base import BaseResource
from schema.agent.instance import AgentInstanceSchema
from utils import swagger


@swagger(method='get',
         sum='Agent Instance Read (Single)',
         desc="""Get the agent instance with the given `id` installed in the execution-environments
                 filtered by the query in the request body.""",
         resp="""Agent instance with the given `id` installed in the execution-environment filtered
                 by the query in the request body.""")
@swagger(method='post',
         sum='Agent Instance Creation (Single)',
         desc='Install a new agent instance in the execution-environments with the given `id` .',
         resp='Agent instance with the given `id` in the execution environments created.')
@swagger(method='delete',
         sum='Agent Instance Deletion (Single)',
         desc="""Remove the agent instance with the given `id` and filtered by the query
                 in the request body from the execution-environments.""",
         resp='Agent instance with the given `id` and filtered by the query in the request body deleted.')
@swagger(method='put',
         sum='Agent Instance Update (Single)',
         desc='Update the agent instance in the execution-environments with the given `id` .',
         resp='Agent instance with the given `id` updated.')
class AgentInstanceSelectedResource(BaseResource):
    doc_cls = AgentInstanceDocument
    doc_name = 'Agent Instance'
    routes = '/config/agent/{id}',
    schema_cls =AgentInstanceSchema
