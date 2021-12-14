from resource.base import BaseResource
from resource.ebpf_program.handler.lcp import LCP

from docstring import docstring
from document.ebpf_program.instance import _eBPFProgramInstanceDocument
from schema.ebpf_program.instance import _eBPFProgramInstanceSchema


@docstring(ext='yaml')
class _eBPFProgramInstanceResource(BaseResource):
    doc = _eBPFProgramInstanceDocument
    name = 'eBPF program'
    names = 'eBPF programs'
    routes = '/instance/ebpf-program/'
    schema = _eBPFProgramInstanceSchema
    lcp_handler = {'post': LCP.post, 'put': LCP.put, 'delete': LCP.delete}
    ignore_fields = ['parameters']


@docstring(ext='yaml')
class _eBPFProgramInstanceSelectedResource(_eBPFProgramInstanceResource):
    routes = '/instance/ebpf-program/{_id}'
