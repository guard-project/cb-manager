from document.algorithm import Algorithm_Document
from marshmallow.fields import Str
from schema.base import Base_Schema

__all__ = [
    'Algorithm_Schema'
]


class Algorithm_Schema(Base_Schema):
    """Represents the algorithms."""
    doc = Algorithm_Document

    id = Str(required=True, example='BXrHRn5RPU55Qh9JwMZn',
             description='Id of the algorithm.')
