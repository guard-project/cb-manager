from resource.base import BaseResource
from resource.ebpf_program.handler.lcp import LCP

from docstring import docstring
from document.ebpf_program.instance import eBPFProgramInstanceDocument
from schema.ebpf_program.instance import eBPFProgramInstanceSchema


@docstring(ext='yaml')
class eBPFProgramInstanceResource(BaseResource):
    doc = eBPFProgramInstanceDocument
    name = 'eBPF program'
    names = 'eBPF programs'
    routes = '/instance/ebpf-program/'
    schema = eBPFProgramInstanceSchema
    lcp_handler = {'post': LCP.post, 'put': LCP.put, 'delete': LCP.delete}
    ignore_fields = ['parameters']


@docstring(ext='yaml')
class eBPFProgramInstanceSelectedResource(eBPFProgramInstanceResource):
    routes = '/instance/ebpf-program/{id}'
