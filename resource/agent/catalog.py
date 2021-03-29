from resource.base import Base_Resource

from docstring import docstring
from document.agent.catalog import Agent_Catalog_Document
from schema.agent.catalog import Agent_Catalog_Schema


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
