from marshmallow.fields import Str

from document.event import EventDocument
from schema.base import BaseSchema


class EventSchema(BaseSchema):
    """Represents the stored events."""

    doc = EventDocument
    id = Str(required=True, example='BXrHRn5RPU55Qh9JwMZn',
             description='Id of the event.')
