from resource.base import Base_Resource

from docstring import docstring
from document.pipeline import Pipeline_Document
from schema.pipeline import Pipeline_Schema
from schema.response import *

__all__ = [
    'Pipeline_Resource',
    'Pipeline_Selected_Resource'
]


@docstring(ext='yaml')
class Pipeline_Resource(Base_Resource):
    doc = Pipeline_Document
    name = 'pipeline'
    names = name
    routes = '/pipeline/'
    schema = Pipeline_Schema


@docstring(ext='yaml')
class Pipeline_Selected_Resource(Pipeline_Resource):
    routes = '/pipeline/{id}'
