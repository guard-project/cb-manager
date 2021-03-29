from marshmallow.fields import Str

from document.pipeline import Pipeline_Document
from schema.base import Base_Schema


class Pipeline_Schema(Base_Schema):
    """Represents the stored pipelines."""

    doc = Pipeline_Document
    id = Str(required=True, example='BXrHRn5RPU55Qh9JwMZn', description='Id of the pipeline.')
