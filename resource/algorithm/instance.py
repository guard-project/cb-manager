from resource.algorithm.handler.lcp import LCP
from resource.base import BaseResource

from docstring import docstring
from document.algorithm.instance import AlgorithmInstanceDocument
from schema.algorithm.instance import AlgorithmInstanceSchema


@docstring(ext="yaml")
class AlgorithmInstanceResource(BaseResource):
    doc = AlgorithmInstanceDocument
    name = "algorithm instance"
    names = "algorithm instances"
    routes = "/instance/algorithm/"
    schema = AlgorithmInstanceSchema
    lcp_handler = {"post": LCP.handler, "put": LCP.handler}
    ignore_fields = ["operations"]


@docstring(ext="yaml")
class AlgorithmInstanceSelectedResource(AlgorithmInstanceResource):
    routes = "/instance/algorithm/{_id}"
