from copy import deepcopy
from elasticsearch import RequestError as Request_Error, NotFoundError as Not_Found_Error
from lib.http import HTTP_Method
from lib.response import *
from reader.arg import Arg_Reader
from reader.query import Query_Reader
from schema.query_request import Query_Request_Schema
from time import sleep
from utils.log import Log
from utils.sequence import is_list, wrap

__all__ = [
    'Base_Minimal_Resource',
    'Base_Resource'
]


class Base_Minimal_Resource(object):
    tag = []
    doc = None
    schema = None


class Base_Resource(Base_Minimal_Resource):
    lcp_handler = {}
    ignore_fields = []

    def __init__(self):
        if self.doc is not None:
            self.log = Log.get(self.doc.Index.name)
            err_es_init = True
            while err_es_init:
                try:
                    msg = f'start initialization index {self.doc.Index.name}'
                    self.log.info(msg)
                    self.doc.init()
                    msg = f'index {self.doc.Index.name} initialized'
                    self.log.success(msg)
                    err_es_init = False
                except Exception as e:
                    self.log.exception(e)
                    msg = f'initialization index {self.doc.Index.name} not possible'
                    self.log.error(msg)
                    msg = f'waiting for {Arg_Reader.db.es_retry_period} seconds and try again'
                    self.log.info(msg)
                    sleep(Arg_Reader.db.es_retry_period)
        else:
            Log.get(self.__class__.__name__).warning('doc not set')

    def on_base_get(self, req, resp, id=None):
        req_data = req.media or {}
        qrs = Query_Request_Schema(method=HTTP_Method.GET, unknown='INCLUDE')
        resp_data, valid = qrs.validate(data=req_data, id=id)
        if valid:
            try:
                qr = Query_Reader(index=self.doc.Index.name)
                s = qr.parse(query=req_data, id=id)
                resp_data = [dict(hit.to_dict(), id=hit.meta.id)
                             for hit in s.execute()]
                if len(resp_data) > 0:
                    resp_data, valid = self.schema(many=True, partial=True, unknown='INCLUDE',
                                            method=HTTP_Method.GET).validate(data=resp_data,
                                                                             response_type=Content_Response)
                    resp_data.apply(resp)
                else:
                    msg = f'{self.name.capitalize()} based on the request {{query}} not found'
                    Not_Found_Response(msg, query=req_data).apply(resp)
            except Exception as e:
                self.log.exception(e)
                msg = f'Not possible to get {self.names} with the request {{query}}'
                Unprocessable_Entity_Response(msg, exception=e,
                                              query=req_data).apply(resp)
        else:
            resp_data.apply(resp)

    def on_base_post(self, req, resp, id=None):
        req_data = req.media or {}
        resp_data, valid = self.schema(many=is_list(req_data), unknown='INCLUDE',
                                       method=HTTP_Method.POST).validate(data=req_data, id=id)
        if valid:
            req_data_wrap = wrap(req_data)
            if len(req_data_wrap) > 0:
                for req_data in req_data_wrap:
                    try:
                        req_data_lcp = deepcopy(req_data)
                        req_data_id = req_data.pop('id', id)
                        self.rm_ignore_fields(req_data)
                        obj = self.doc(meta=dict(id=req_data_id),
                                       **req_data)
                        obj.save()
                        msg = f'{self.name.capitalize()} with the id={req_data_id} correctly created'
                        resp_data_lcp = []
                        resp_data = Created_Response(msg)
                        hndl = self.get_lcp_handler(HTTP_Method.POST)
                        hndl(instance=obj, req=req_data_lcp, resp=resp_data_lcp)
                        if len(resp_data_lcp) > 0:
                            resp_data.update(operation=resp_data_lcp)
                        resp_data.add(resp)
                    except Exception as e:
                        self.log.exception(e)
                        msg = f'Not possible to create a {self.name} with the id={req_data_id}'
                        Unprocessable_Entity_Response(msg,
                                                      exception=e).add(resp)
            else:
                msg = f'No content to create {self.names} based the {{request}}'
                No_Content_Response(msg, request=req_data).apply(resp)
        else:
            resp_data.apply(resp)

    def on_base_put(self, req, resp, id=None):
        so = self.doc.Status_Operation
        req_data = req.media or {}
        resp_data, valid = self.schema(many=is_list(req_data), unknown='INCLUDE',
                                       partial=True, method=HTTP_Method.PUT).validate(data=req_data, id=id)
        if valid:
            req_data_wrap = wrap(req_data)
            if len(req_data_wrap) > 0:
                for req_data in req_data_wrap:
                    try:
                        req_data_lcp = deepcopy(req_data)
                        req_data_id = req_data.pop('id', id)
                        if len(req_data) == 0:
                            msg = f'Update for {self.name} with id={req_data_id} not necessary'
                            Not_Modified_Response(msg).add(resp)
                        else:
                            self.rm_ignore_fields(req_data)
                            modified = False
                            obj = self.doc.get(id=req_data_id)
                            if len(req_data) > 0:
                                res = obj.update(**req_data)
                                if res == so.UPDATED:
                                    modified = True
                            resp_data_lcp = []
                            hndl = self.get_lcp_handler(HTTP_Method.PUT)
                            modified = hndl(instance=obj, req=req_data_lcp,
                                            resp=resp_data_lcp) or modified
                            if modified:
                                msg = f'{self.name.capitalize()} with the id={req_data_id} correctly updated'
                                resp_data = Ok_Response(msg)
                            else:
                                msg = f'{self.name.capitalize()} with the id={req_data_id} no need to update'
                                resp_data = Not_Modified_Response(msg)
                            if len(resp_data_lcp) > 0:
                                resp_data.update(operation=resp_data_lcp)
                            resp_data.add(resp)
                    except Exception as e:
                        self.log.exception(e)
                        msg = f'Not possible to update a {self.name} with the id={req_data_id}'
                        Unprocessable_Entity_Response(msg,
                                                      exception=e).add(resp)
            else:
                msg = f'No content to update {self.name} based on the {{request}}'
                No_Content_Response(msg, exception=e,
                                    request=req_data).apply(resp)
        else:
            resp_data.apply(resp)

    def on_base_delete(self, req, resp, id=None):
        req_data = req.media or {}
        qrs = Query_Request_Schema(method=HTTP_Method.DELETE)
        resp_data, valid = qrs.validate(data=req_data, id=id)
        if resp:
            try:
                qr = Query_Reader(index=self.doc.Index.name)
                s = qr.parse(query=req_data, id=id)
                hits = s.execute()
                if len(hits) > 0:
                    for hit in hits:
                        try:
                            obj = self.doc.get(id=hit.meta.id)
                            obj.delete()
                            msg = f'{self.name.capitalize()} with the id={hit.meta.id} correctly deleted'
                            resp_data_lcp = []
                            resp_data = Reset_Content_Response(msg)
                            hndl = self.get_lcp_handler(HTTP_Method.DELETE)
                            hndl(instance=obj, req=hit, resp=resp_data_lcp)
                            if len(resp_data_lcp) > 0:
                                resp_data.update(operation=resp_data_lcp)
                            resp_data.add(resp)
                        except Exception as e:
                            self.log.exception(e)
                            msg = f'Not possible to delete the {self.name} with the id={hit.meta.id}'
                            Unprocessable_Entity_Response(msg,
                                                          exception=e).add(resp)
                else:
                    msg = f'{self.names.capitalize()} based on the request {{query}} not found'
                    Not_Found_Response(msg, query=req_data).apply(resp)
            except Exception as e:
                self.log.exception(e)
                msg = f'Not possible to delete {self.names} with the request {{query}}'
                Unprocessable_Entity_Response(msg, exception=e,
                                              query=req_data).apply(resp)
        else:
            resp_data.apply(resp)

    def rm_ignore_fields(self, data):
        for ign_f in self.ignore_fields:
            if data.pop(ign_f, None) is not None:
                m = f'field {ign_f} in the request ignored when update {self.names}'
                self.log.info(m)

    @ classmethod
    def get_lcp_handler(cls, method):
        def __default(instance, req, resp):
            return resp

        return cls.lcp_handler.get(method, __default)
