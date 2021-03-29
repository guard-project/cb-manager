from resource.base import Base_Resource

from docstring import docstring
from document.ebpf_program.catalog import eBPF_Program_Catalog_Document
from schema.ebpf_program.catalog import eBPF_Program_Catalog_Schema


@docstring(ext='yaml')
class eBPF_Program_Catalog_Resource(Base_Resource):
    doc = eBPF_Program_Catalog_Document
    name = 'eBPF program catalog'
    names = 'eBPF program catalogs'
    routes = '/catalog/ebpf-program/'
    schema = eBPF_Program_Catalog_Schema


@docstring(ext='yaml')
class eBPF_Program_Catalog_Selected_Resource(eBPF_Program_Catalog_Resource):
    routes = '/catalog/ebpf-program/{id}'
