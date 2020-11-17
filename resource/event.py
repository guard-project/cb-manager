from document.event import Event_Document
from resource.base import Base_Resource
from schema.event import Event_Schema
from schema.response import *
from docstring import docstring

__all__ = [
    'Event_Resource',
    'Event_Selected_Resource'
]


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
