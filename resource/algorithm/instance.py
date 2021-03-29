from resource.algorithm.handler.lcp import LCP
from resource.base import Base_Resource

from docstring import docstring
from document.algorithm.instance import Algorithm_Instance_Document
from schema.algorithm.instance import Algorithm_Instance_Schema


@docstring(ext='yaml')
class Algorithm_Instance_Resource(Base_Resource):
    doc = Algorithm_Instance_Document
    name = 'algorithm instance'
    names = 'algorithm instances'
    routes = '/instance/algorithm/'
    schema = Algorithm_Instance_Schema
    lcp_handler = dict(post=LCP.handler, put=LCP.handler)
    ignore_fields = ['operations']


@docstring(ext='yaml')
class Algorithm_Instance_Selected_Resource(Algorithm_Instance_Resource):
    routes = '/instance/algorithm/{id}'
