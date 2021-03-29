from resource.base import Base_Resource

from docstring import docstring
from document.data import Data_Document
from schema.data import Data_Schema


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
