from marshmallow.fields import List

from utils.sequence import wrap


class ListOrOne(List):
    def _deserialize(self, value, attr, data, **kwargs):
        if value:
            if isinstance(value, str):
                value = value.replace("\r", "").splitlines()
            else:
                value = wrap(value)
        return super(ListOrOne, self)._deserialize(value, attr, data, **kwargs)
