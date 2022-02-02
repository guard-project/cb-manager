from marshmallow import Schema, validates_schema
from marshmallow.exceptions import ValidationError as Validation_Error

from lib.http import HTTPMethod
from lib.response import NotAcceptableResponse, OkResponse
from schema.validate import UniqueList
from utils.sequence import is_dict, is_list

MSG_ID_ONE_RECORD_MANAGED = "When the id is present in the request uri only one record can be managed."  # noqa F401
MSG_PRESENT_REQ_URI = "Present in the request uri."
MSG_SAME_ID_MULT_TIMES = "Same id present multiple times in the request."
MSG_ID_FOUND = "Id already found."
MSG_ID_NOT_FOUND = "Id not found."
MSG_READONLY_FIELD = "Readonly field."


class BaseSchema(Schema):
    doc = None

    def __init__(self, *args, method=None, check_unique_id=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.method = method
        self.check_unique_id = check_unique_id

    def validate(self, data, response_type=OkResponse, item_id=None):
        try:
            if item_id is not None:
                if is_list(data):
                    raise Validation_Error({"id": MSG_ID_ONE_RECORD_MANAGED})
                elif item_id in data:
                    raise Validation_Error({"id": MSG_PRESENT_REQ_URI})
                else:
                    data.update(id=item_id)
            if (
                self.check_unique_id
                and is_list(data)
                and not UniqueList.apply("id")(data)
            ):
                raise Validation_Error({"id": MSG_SAME_ID_MULT_TIMES})
            self.load(data)
            return response_type(data), True
        except Validation_Error as val_err:

            def __norm(block):
                for field in block.keys():
                    if is_list(block[field]):
                        block[field] = block[field].pop()
                    elif is_dict(block[field]):
                        __norm(block[field])
                return block

            _msg = __norm(val_err.normalized_messages())
            return NotAcceptableResponse(_msg), False

    @validates_schema(skip_on_field_errors=False)
    def __validate_id(self, data, **kwargs):
        if self.doc is not None:
            data_id = data.get("id", None)
            ids = self.doc.get_ids()
            if self.method == HTTPMethod.POST and data_id in ids:
                raise Validation_Error({"id": MSG_ID_FOUND})
            elif (
                self.method in [HTTPMethod.PUT, HTTPMethod.DELETE]
                and data_id not in ids
            ):
                raise Validation_Error({"id": MSG_ID_NOT_FOUND})

    @validates_schema(skip_on_field_errors=False)
    def __validate_readonly(self, data, **kwargs):
        if self.method == HTTPMethod.PUT:
            for field, props in self.declared_fields.items():
                if (
                    props.metadata.get("readonly", False)
                    and data.get(field, None) is not None
                ):
                    raise Validation_Error({field: MSG_READONLY_FIELD})
