from elasticsearch_dsl import Document, InnerDoc


class BaseDocument(Document):
    class StatusOperation():
        NOT_MODIFIED = 'noop'
        CREATED = 'created'
        UPDATED = 'updated'
        DELETED = 'deleted'

    @classmethod
    def get_ids(cls):
        search = cls.search()
        return [doc.meta.id for doc in search[:search.count()].execute()]

    @classmethod
    def get_or_new(cls, id):
        obj = cls.get(id=id, ignore=404)
        if obj is None:
            obj = cls(meta={'id': id})
        return obj


class BaseInnerDoc(InnerDoc):
    @classmethod
    def get_or_new(cls, id, container):
        res = list(filter(lambda x: x.id == id, container))
        if res:
            return res[0]
        out = cls(id=id)
        container.append(out)
        return out
