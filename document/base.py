from elasticsearch_dsl import Document


class BaseDocument(Document):
    class StatusOperation():
        NOT_MODIFIED = 'noop'
        CREATED = 'created'
        UPDATED = 'updated'
        DELETED = 'deleted'

    @classmethod
    def get_ids(cls):
        search = cls.search()
        return [doc.meta.id for doc in search[0:search.count()].execute()]
