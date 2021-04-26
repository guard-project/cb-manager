from marshmallow.fields import Str

from document.pipeline import Pipeline_Document
from schema.base import Base_Schema
from utils.datetime import DateTime as Date_Time


class Pipeline_Schema(Base_Schema):
    """Represents the stored pipelines."""

    doc = Pipeline_Document
    id = Str(required=True, example='BXrHRn5RPU55Qh9JwMZn', description='Id of the pipeline.')
    updated_at = Date_Time(description='Date of last update of the pipeline in Unix timestamp format.', format='timestamp', example=1617278285)
    created_at = Date_Time(required=True, readonly=True, example=1617278285, format='timestamp',
                           description='Date of creation of the pipeline in Unix timestamp format.')
    name = Str(description='Used by the UI to create a new pipeline.', example='test pipeline guard-vdpi ud')
    status = Str(required=True, description='Pipeline status.', example='started')
    user = Str(description='User/Entity owner/manager/responsible of the pipeline.', example='Minds & Sparks')
