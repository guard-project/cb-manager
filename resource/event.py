from resource.base import Base_Resource

from docstring import docstring
from document.event import Event_Document
from schema.event import Event_Schema


@docstring(ext='yaml')
class Event_Resource(Base_Resource):
    doc = Event_Document
    name = 'event'
    names = name
    routes = '/event/'
    schema = Event_Schema


@docstring(ext='yaml')
class Event_Selected_Resource(Event_Resource):
    routes = '/event/{id}'
