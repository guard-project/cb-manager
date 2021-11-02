from resource.base import BaseResource

from docstring import docstring
from document.ebpf_program.catalog import eBPFProgramCatalogDocument
from schema.ebpf_program.catalog import eBPFProgramCatalogSchema


@docstring(ext='yaml')
class eBPFProgramCatalogResource(BaseResource):
    doc = eBPFProgramCatalogDocument
    name = 'eBPF program catalog'
    names = 'eBPF program catalogs'
    routes = '/catalog/ebpf-program/'
    schema = eBPFProgramCatalogSchema


@docstring(ext='yaml')
class eBPFProgramCatalogSelectedResource(eBPFProgramCatalogResource):
    routes = '/catalog/ebpf-program/{id}'
