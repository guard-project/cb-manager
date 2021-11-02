from resource.base import BaseResource

from docstring import docstring
from document.network_link import NetworkLinkDocument, NetworkLinkTypeDocument
from schema.network_link import NetworkLinkSchema, NetworkLinkTypeSchema


@docstring(ext='yaml')
class NetworkLinkResource(BaseResource):
    doc = NetworkLinkDocument
    name = 'network link'
    names = 'network links'
    routes = '/network-link/'
    schema = NetworkLinkSchema


@docstring(ext='yaml')
class NetworkLinkSelectedResource(NetworkLinkResource):
    routes = '/network-link/{id}'


@docstring(ext='yaml')
class NetworkLinkTypeResource(BaseResource):
    doc = NetworkLinkTypeDocument
    name = 'network link type'
    names = 'network link types'
    routes = '/type/network-link/'
    schema = NetworkLinkTypeSchema


@docstring(ext='yaml')
class NetworkLinkTypeSelectedResource(NetworkLinkTypeResource):
    routes = '/type/network-link/{id}'
