from resource.base import Base_Resource

from docstring import docstring
from document.network_link import Network_Link_Document, Network_Link_Type_Document
from schema.network_link import Network_Link_Schema, Network_Link_Type_Schema


@docstring(ext='yaml')
class Network_Link_Resource(Base_Resource):
    doc = Network_Link_Document
    name = 'network link'
    names = 'network links'
    routes = '/network-link/'
    schema = Network_Link_Schema


@docstring(ext='yaml')
class Network_Link_Selected_Resource(Network_Link_Resource):
    routes = '/network-link/{id}'


@docstring(ext='yaml')
class Network_Link_Type_Resource(Base_Resource):
    doc = Network_Link_Type_Document
    name = 'network link type'
    names = 'network link types'
    routes = '/type/network-link/'
    schema = Network_Link_Type_Schema


@docstring(ext='yaml')
class Network_Link_Type_Selected_Resource(Network_Link_Type_Resource):
    routes = '/type/network-link/{id}'
