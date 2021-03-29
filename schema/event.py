from marshmallow.fields import Str

from document.event import Event_Document
from schema.base import Base_Schema


class Event_Schema(Base_Schema):
    """Represents the stored events."""

    doc = Event_Document
    id = Str(required=True, example='BXrHRn5RPU55Qh9JwMZn', description='Id of the event.')
