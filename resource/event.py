from resource.base import BaseResource

from docstring import docstring
from document.event import EventDocument
from schema.event import EventSchema


@docstring(ext="yaml")
class EventResource(BaseResource):
    doc = EventDocument
    name = "event"
    names = name
    routes = "/event/"
    schema = EventSchema


@docstring(ext="yaml")
class EventSelectedResource(EventResource):
    routes = "/event/{_id}"
