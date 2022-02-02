from marshmallow.fields import Str

from document.pipeline import PipelineDocument
from schema.base import BaseSchema
from utils.datetime import DateTime


class PipelineSchema(BaseSchema):
    """Represents the stored pipelines."""

    doc = PipelineDocument
    id = Str(
        required=True, example="BXrHRn5RPU55Qh9JwMZn", description="Id of the pipeline."
    )
    updated_at = DateTime(
        description="Date of last update of the pipeline in Unix timestamp format.",  # noqa: E501
        format="timestamp",
        example=1617278285,
    )
    created_at = DateTime(
        required=True,
        readonly=True,
        example=1617278285,
        format="timestamp",
        description="Date of creation of the pipeline in Unix timestamp format.",
    )  # noqa: E501
    name = Str(
        description="Used by the UI to create a new pipeline.",
        example="test pipeline guard-vdpi ud",
    )
    status = Str(required=True, description="Pipeline status.", example="started")
    user = Str(
        description="User/Entity owner/manager/responsible of the pipeline.",  # noqa: E501
        example="Minds & Sparks",
    )
