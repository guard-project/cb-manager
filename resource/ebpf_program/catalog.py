from document.ebpf_program.catalog import eBPF_Program_Catalog_Document
from lib.http import HTTP_Method
from resource.base import Base_Resource
from schema.ebpf_program.catalog import eBPF_Program_Catalog_Schema
from schema.response import *
from docstring import docstring

__all__ = [
    'eBPF_Program_Catalog_Resource',
    'eBPF_Program_Catalog_Selected_Resource'
]


@docstring(ext='yaml')
class eBPF_Program_Catalog_Resource(Base_Resource):
    doc= eBPF_Program_Catalog_Document
    name = 'eBPF program catalog'
    names = 'eBPF program catalogs'
    routes = '/catalog/ebpf-program/'
    schema = eBPF_Program_Catalog_Schema


@docstring(ext='yaml')
class eBPF_Program_Catalog_Selected_Resource(eBPF_Program_Catalog_Resource):
    routes = '/catalog/ebpf-program/{id}'
