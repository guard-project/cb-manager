from resource.base import Base_Resource

from docstring import docstring
from document.algorithm.catalog import Algorithm_Catalog_Document
from schema.algorithm.catalog import Algorithm_Catalog_Schema
from schema.response import *

__all__ = [
    'Algorithm_Catalog_Resource',
    'Algorithm_Catalog_Selected_Resource'
]


@docstring(ext='yaml')
class Algorithm_Catalog_Resource(Base_Resource):
    doc = Algorithm_Catalog_Document
    name = 'algorithm catalog'
    names = 'algorithm catalogs'
    routes = '/catalog/algorithm/'
    schema = Algorithm_Catalog_Schema


@docstring(ext='yaml')
class Algorithm_Catalog_Selected_Resource(Algorithm_Catalog_Resource):
    routes = '/catalog/algorithm/{id}'
