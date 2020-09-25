from document.agent.instance import Agent_Instance_Document
from lib.http import HTTP_Method
from resource.base import Base_Resource
from resource.agent.handler.lcp import LCP
from schema.agent.instance import Agent_Instance_Schema
from schema.response import *
from docstring import docstring

__all__ = [
    'Agent_Instance_Resource',
    'Agent_Instance_Selected_Resource'
]


@docstring(ext='yaml')
class Agent_Instance_Resource(Base_Resource):
    doc = Agent_Instance_Document
    name = 'agent instance'
    names = 'agent instances'
    routes = '/instance/agent/'
    schema = Agent_Instance_Schema
    lcp_handler = dict(post=LCP.handler, put=LCP.handler)
    ignore_fields = ['operations']


@docstring(ext='yaml')
class Agent_Instance_Selected_Resource(Agent_Instance_Resource):
    routes = '/instance/agent/{id}'
