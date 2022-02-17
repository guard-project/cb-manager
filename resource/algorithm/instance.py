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
    ignore_fields = ["operations"]


@docstring(ext="yaml")
class AlgorithmInstanceSelectedResource(AlgorithmInstanceResource):
    routes = "/instance/algorithm/{_id}"
