from resource.base import BaseResource

from docstring import docstring
from document.ebpf_program.catalog import _eBPFProgramCatalogDocument
from schema.ebpf_program.catalog import _eBPFProgramCatalogSchema


@docstring(ext='yaml')
class _eBPFProgramCatalogResource(BaseResource):
    doc = _eBPFProgramCatalogDocument
    name = 'eBPF program catalog'
    names = 'eBPF program catalogs'
    routes = '/catalog/ebpf-program/'
    schema = _eBPFProgramCatalogSchema


@docstring(ext='yaml')
class _eBPFProgramCatalogSelectedResource(_eBPFProgramCatalogResource):
    routes = '/catalog/ebpf-program/{_id}'
