from resource.base import BaseResource

from docstring import docstring
from document.data import DataDocument
from schema.data import DataSchema


@docstring(ext='yaml')
class DataResource(BaseResource):
    doc = DataDocument
    name = 'data'
    names = name
    routes = '/data/'
    schema = DataSchema


@docstring(ext='yaml')
class DataSelectedResource(DataResource):
    routes = '/data/{_id}'
