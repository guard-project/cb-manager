from resource.base import BaseResource

from docstring import docstring
from document.pipeline import PipelineDocument
from schema.pipeline import PipelineSchema


@docstring(ext='yaml')
class PipelineResource(BaseResource):
    doc = PipelineDocument
    name = 'pipeline'
    names = name
    routes = '/pipeline/'
    schema = PipelineSchema


@docstring(ext='yaml')
class PipelineSelectedResource(PipelineResource):
    routes = '/pipeline/{_id}'
