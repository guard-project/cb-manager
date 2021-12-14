from resource.base import BaseResource

from docstring import docstring
from document.connection import ConnectionDocument
from schema.connection import ConnectionSchema


@docstring(ext='yaml')
class ConnectionResource(BaseResource):
    doc = ConnectionDocument
    name = 'connection'
    names = 'connections'
    routes = '/connection/'
    schema = ConnectionSchema


@docstring(ext='yaml')
class ConnectionSelectedResource(ConnectionResource):
    routes = '/connection/{_id}'
