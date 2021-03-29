from resource.base import Base_Resource
from resource.ebpf_program.handler.lcp import LCP

from docstring import docstring
from document.ebpf_program.instance import eBPF_Program_Instance_Document
from schema.ebpf_program.instance import eBPF_Program_Instance_Schema


@docstring(ext='yaml')
class eBPF_Program_Instance_Resource(Base_Resource):
    doc = eBPF_Program_Instance_Document
    name = 'eBPF program'
    names = 'eBPF programs'
    routes = '/instance/ebpf-program/'
    schema = eBPF_Program_Instance_Schema
    lcp_handler = dict(post=LCP.post, put=LCP.put, delete=LCP.delete)
    ignore_fields = ['parameters']


@docstring(ext='yaml')
class eBPF_Program_Instance_Selected_Resource(eBPF_Program_Instance_Resource):
    routes = '/instance/ebpf-program/{id}'
