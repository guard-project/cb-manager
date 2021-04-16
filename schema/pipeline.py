from marshmallow.fields import DateTime as Date_Time
from marshmallow.fields import Str

from document.pipeline import Pipeline_Document
from schema.base import Base_Schema


class Pipeline_Schema(Base_Schema):
    """Represents the stored pipelines."""

    doc = Pipeline_Document
    id = Str(required=True, example='BXrHRn5RPU55Qh9JwMZn', description='Id of the pipeline.')
    updated_at = Date_Time(description='', description='Date of last update of the pipeline in Unix timestamp format.', example=1617278285)
    created_at = Date_Time(required=True, readonly=True, description='Date of creation of the pipeline in Unix timestamp format.', example=1617278285)
    name = Str(description='Used by the UI to create a new pipeline.', example='test pipeline guard-vdpi ud')
    status = Str(required=True, description='Pipeline status.', example='started')
    user = Str(description='', description='User/Entity owner/manager/responsible of the pipeline.', example='Minds & Sparks')
