from document.algorithm import Algorithm_Document
from resource.base import Base_Resource
from schema.algorithm import Algorithm_Schema
from schema.response import *
from docstring import docstring

__all__ = [
    'Algorithm_Resource',
    'Algorithm_Selected_Resource'
]


@docstring(ext='yaml')
class Algorithm_Resource(Base_Resource):
    doc = Algorithm_Document
    name = 'algorithm'
    names = name
    routes = '/algorithm/'
    schema = Algorithm_Schema


@docstring(ext='yaml')
class Algorithm_Selected_Resource(Algorithm_Resource):
    routes = '/algorithm/{id}'
