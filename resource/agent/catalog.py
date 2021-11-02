from resource.base import BaseResource

from docstring import docstring
from document.agent.catalog import AgentCatalogDocument
from schema.agent.catalog import AgentCatalogSchema


@docstring(ext='yaml')
class AgentCatalogResource(BaseResource):
    doc = AgentCatalogDocument
    name = 'agent catalog'
    names = 'agent catalogs'
    routes = '/catalog/agent/'
    schema = AgentCatalogSchema


@docstring(ext='yaml')
class AgentCatalogSelectedResource(AgentCatalogResource):
    routes = '/catalog/agent/{id}'
