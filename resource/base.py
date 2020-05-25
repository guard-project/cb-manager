from document.nested import edit as nested_edit, rm as nested_rm
from elasticsearch import NotFoundError, RequestError
from elasticsearch_dsl.utils import AttrList
from falcon import HTTPBadRequest
from http import HTTPStatus
from log import Log
from reader.arg import ArgReader
from reader.query import QueryReader
from time import sleep
from utils import subset, wrap


class BaseResource(object):
    def __init__(self):
        self.log = Log.get(self.doc_cls.Index.name)
        error_es_initialization = True
        while error_es_initialization:
            try:
                self.log.info(f'start initialization index {self.doc_cls.Index.name}')
                self.doc_cls.init()
            except Exception as e:
                self.log.debug(e)
                self.log.error(f'initialization index {self.doc_cls.Index.name} not possible')
                self.log.info(f'waiting for {ArgReader.db.es_retry_period} seconds and try again')
                sleep(ArgReader.db.es_retry_period)
                self.__init__()
            else:
                self.log.success(f'index {self.doc_cls.Index.name} initialized')
                error_es_initialization = False

    def on_base_get(self, req, resp, id=None):
        try:
            response = QueryReader(index=self.doc_cls.Index.name).parse(
                query=req.context.get('json', {}), id=id
            ).execute()
            resp.media = [dict(hit.to_dict(), id=hit.meta.id) for hit in response]
        except RequestError as req_error:
            raise HTTPBadRequest(
                title=req_error.error,
                description=req_error.info
            )

    def on_base_post(self, req, resp, id=None):
        res = []
        query = req.context.get('json', [])
        if id is not None:
            if type(query) is list:
                raise HTTPBadRequest(
                    title='id provided',
                    description=f'Request can create only 1 new {self.doc_name}'
                )
            single = True
        else:
            single = False
        for data in wrap(query):
            data_id = data.pop('id', None)
            if data_id is not None and single:
                res.append({
                    'status': 'error',
                    'reason': f'Request not valid: two ids provided',
                    'id': [data_id, id],
                    'http_status_code': HTTPStatus.CONFLICT
                })
            else:
                try:
                    if data_id is not None:
                        obj = self.doc_cls.get(id=data_id, ignore=404)
                        meta = { 'id': data_id }
                    else:
                        obj = None
                        meta = {}
                    if obj is None:
                        obj = self.doc_cls(meta=meta, **data)
                        status = obj.save()
                        res.append({
                            'status': status,
                            'data': { 'id': obj.meta.id, **obj.to_dict() },
                            'http_status_code': HTTPStatus.CREATED
                        })
                    else:
                        res.append({
                            'status': 'error',
                            'reason': f'{self.doc_name} with the given [id] already found',
                            'id': obj.meta.id,
                            'http_status_code': HTTPStatus.CONFLICT
                        })
                except Exception as e:
                    self.log.debug(e)
                    res.append({
                        'status': 'error',
                        'reason': f'Not possible create {self.doc_name} with the given [data]',
                        'data': { 'id': id, **data },
                        'http_status_code': HTTPStatus.UNPROCESSABLE_ENTITY
                    })
        resp.media = res

    def on_base_delete(self, req, resp, id=None):
        try:
            res = []
            response = QueryReader(index=self.doc_cls.Index.name).parse(
                query=req.context.get('json', {}), id=id
            ).execute()
            for hit in response:
                try:
                    obj = self.doc_cls.get(id=hit.meta.id)
                    data = obj.to_dict()
                    obj.delete()
                    res.append({
                        'status': 'deleted',
                        'data': { **data, 'id': hit.meta.id },
                        'http_status_code': HTTPStatus.OK
                    })
                except Exception as e:
                    self.log.debug(e)
                    res.append({
                        'status': 'error',
                        'reason': f'Not possible to delete element with the given [id]',
                        'id': hit.meta.id,
                        'http_status_code': HTTPStatus.CONFLICT
                    })
            resp.media = res
        except elasticsearch.RequestError as req_error:
            raise HTTPBadRequest(
                title=req_error.error,
                description=req_error.info
            )

    def on_base_put(self, req, resp, id=None, nested_fields=[]):
        res = []
        query = req.context.get('json', [])
        if id is not None:
            if type(query) is list:
                raise HTTPBadRequest(
                    title='id provided',
                    description=f'Request can create only 1 new {self.doc_name}'
                )
            single = True
        else:
            single = False
        for data in wrap(query):
            data_id = data.pop('id', None)
            if data_id is None and not single:
                res.append({
                    'status': 'error',
                    'reason': 'Request not valid: id property not found',
                    'http_status_code': HTTPStatus.NOT_FOUND
                })
            elif data_id is not None and single:
                res.append({
                    'status': 'error',
                    'reason': f'Request not valid: two ids provided',
                    'id': [data_id, id],
                    'http_status_code': HTTPStatus.CONFLICT
                })
            else:
                try:
                    obj = self.doc_cls.get(id=data_id)
                    if len(data) == 0:
                        status = 'noop'
                    else:
                        status = 'noop'
                        for nested_field in nested_fields:
                            nested_data = wrap(data.get(nested_field, []))

                            status_rm = nested_rm(obj, data=nested_data, field=nested_field)
                            status_edit = nested_edit(obj, data=nested_data, field=nested_field)

                            if 'updated' in [status_rm, status_edit]:
                                status = 'updated'
                        subset_data = subset(data, *nested_fields, negation=True)
                        if len(subset_data) > 0:
                            status_data = obj.update(**subset_data)
                            if status_data == 'updated':
                                status = status_data
                        res.append({
                            'status': status,
                            'data': { **obj.to_dict(), 'id': data_id },
                            'http_status_code': HTTPStatus.OK
                        })
                except NotFoundError as not_found_error:
                    self.log.debug(not_found_error)
                    res.append({
                        'status': 'error',
                        'reason': f'{self.doc_name} with the given [id] not found',
                        'id': data_id,
                        'http_status_code': HTTPStatus.NOT_FOUND
                    })
        resp.media = res
