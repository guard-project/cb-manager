from document.agent.catalog import Agent_Catalog_Document
from lib.http import HTTP_Method
from resource.base import Base_Resource
from schema.agent.catalog import Agent_Catalog_Schema
from schema.response import *
from docstring import docstring

__all__ = [
    'Agent_Catalog_Resource',
    'Agent_Catalog_Selected_Resource'
]

@docstring(ext='yaml')
class Agent_Catalog_Resource(Base_Resource):
    doc = Agent_Catalog_Document
    name = 'agent catalog'
    names = 'agent catalogs'
    routes = '/catalog/agent/'
    schema = Agent_Catalog_Schema


@docstring(ext='yaml')
class Agent_Catalog_Selected_Resource(Agent_Catalog_Resource):
    routes = '/catalog/agent/{id}'
