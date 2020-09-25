from document.connection import Connection_Document
from resource.base import Base_Resource
from schema.connection import Connection_Schema
from schema.response import *
from docstring import docstring

__all__ = [
    'Connection_Resource',
    'Connection_Selected_Resource'
]


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
