from resource.agent.handler.lcp import LCP
from resource.base import BaseResource

from docstring import docstring
from document.agent.instance import AgentInstanceDocument
from schema.agent.instance import AgentInstanceSchema


@docstring(ext='yaml')
class AgentInstanceResource(BaseResource):
    doc = AgentInstanceDocument
    name = 'agent instance'
    names = 'agent instances'
    routes = '/instance/agent/'
    schema = AgentInstanceSchema
    lcp_handler = {'post': LCP.handler, 'put': LCP.handler}
    ignore_fields = ['operations']


@docstring(ext='yaml')
class AgentInstanceSelectedResource(AgentInstanceResource):
    routes = '/instance/agent/{_id}'
