from document.data import Data_Document
from resource.base import Base_Resource
from schema.data import Data_Schema
from schema.response import *
from docstring import docstring

__all__ = [
    'Data_Resource',
    'Data_Selected_Resource'
]


@docstring(ext='yaml')
class Data_Resource(Base_Resource):
    doc = Data_Document
    name = 'data'
    names = name
    routes = '/data/'
    schema = Data_Schema


@docstring(ext='yaml')
class Data_Selected_Resource(Data_Resource):
    routes = '/data/{id}'
