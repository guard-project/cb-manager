from elasticsearch_dsl import Document

__all__ = [
    'Base_Document'
]


class Base_Document(Document):
    class Status_Operation():
        NOT_MODIFIED = 'noop'
        CREATED = 'created'
        UPDATED = 'updated'
        DELETED = 'deleted'

    @classmethod
    def get_ids(cls):
        s = cls.search()
        return [doc.meta.id for doc in s[0:s.count()].execute()]
