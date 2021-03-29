from resource.base import Base_Resource

from docstring import docstring
from document.connection import Connection_Document
from schema.connection import Connection_Schema


@docstring(ext='yaml')
class Connection_Resource(Base_Resource):
    doc = Connection_Document
    name = 'connection'
    names = 'connections'
    routes = '/connection/'
    schema = Connection_Schema


@docstring(ext='yaml')
class Connection_Selected_Resource(Connection_Resource):
    routes = '/connection/{id}'
