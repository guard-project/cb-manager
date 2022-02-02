from resource.base import BaseResource

from docstring import docstring
from document.algorithm.catalog import AlgorithmCatalogDocument
from schema.algorithm.catalog import AlgorithmCatalogSchema


@docstring(ext="yaml")
class AlgorithmCatalogResource(BaseResource):
    doc = AlgorithmCatalogDocument
    name = "algorithm catalog"
    names = "algorithm catalogs"
    routes = "/catalog/algorithm/"
    schema = AlgorithmCatalogSchema


@docstring(ext="yaml")
class AlgorithmCatalogSelectedResource(AlgorithmCatalogResource):
    routes = "/catalog/algorithm/{_id}"
