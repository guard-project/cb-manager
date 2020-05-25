from document.agent.instance import AgentInstanceDocument
from resource.base import BaseResource
from schema.agent.instance import AgentInstanceSchema
from utils import swagger

import resource.agent.instance.operations

@swagger(method='get',
         sum='Agent Instance Read (Multiple)',
         desc="""Get the list of agent instances installed in the execution-environments
                 filtered by the query in the request body.""",
         resp="""List of agent instances installed in the execution-environment
                 filtered by the query in the request body.""")
@swagger(method='post',
         sum='Agent Instance Install (Multiple)',
         desc='Install new agent instances in the execution-environments.',
         resp='Agent instances installed in the execution environments.')
@swagger(method='delete',
         sum='Agent Instance Uninstall (Multiple)',
         desc="""Remove the agent instances filtered by the query in the request body from the
                 execution-environments.""",
         resp='Agent instances filtered by the query in the request body uninstalled.')
@swagger(method='put',
         sum='Agent Instance Update (Multiple)',
         desc='Update the agent instances in the execution-environments.',
         resp='Agent instances updated.')
class AgentInstanceResource(BaseResource):
    doc_cls = AgentInstanceDocument
    doc_name = 'Agent Instance'
    routes = '/config/agent/',
    schema_cls =AgentInstanceSchema

    def on_post(self, req, resp, id=None):
        self.on_base_post(req, resp, id)
        operations.send(req, resp, match_status='created')

    def on_put(self, req, resp, id=None):
        self.on_base_put(req, resp, id, nested_fields=['parameters'])
        operations.send(req, resp, match_status='updated')

    def on_delete(self, req, resp, id=None):
        self.on_base_delete(req, resp, id)
        operations.send(req, resp, match_status='deleted')
