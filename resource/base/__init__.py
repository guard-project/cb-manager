# Copyright (c) 2020-2022 GUARD
# author: Alex Carrega <alessandro.carrega@cnit.it>

from copy import deepcopy
from time import sleep
from typing import Callable, Optional

from lib.http import HTTPMethod
from lib.response import (
    ContentResponse,
    CreatedResponse,
    NoContentResponse,
    NotFoundResponse,
    NotModifiedResponse,
    OkResponse,
    ResetContentResponse,
    UnprocEntityResponse,
)
from reader.arg import ArgReader
from reader.query import QueryReader
from schema.query_request import QueryRequestSchema
from schema.response import BadRequestResponseSchema  # noqa F401
from schema.response import InternalServerErrorResponseSchema  # noqa F401
from schema.response import NotAcceptableResponseSchema  # noqa F401
from schema.response import NotFoundResponseSchema  # noqa F401
from schema.response import ResetContentResponseSchema  # noqa F401
from schema.response import UnauthorizedResponseSchema  # noqa F401
from schema.response import UnprocessableEntityResponseSchema  # noqa F401
from schema.response import UnsupportedMediaTypeResponseSchema  # noqa F401
from utils.log import Log
from utils.sequence import is_list, wrap

MSG_INIT_INDEX_NOT_POSSIBLE = "Initialization index {} not possible"
MSG_WAITING_CONN = "Waiting for {} seconds and try again"
MSG_NOT_FOUND = "{} based on the request {{query}} not found"
MSG_UPDATE_NOT_NEEDED = "Update for {} with id={} not necessary"

MSG_ERROR = "Some errors occur but the {} with the id={} forcedly {}"
MSG_NO_CONTENT = "No content to {} {} based the {{request}}"
MSG_OK = "{} with the id={} correctly {}"
MSG_NOT_POSSIBLE_ID = "Not possible to {} {} with the id={}"
MSG_NOT_POSSIBLE = "Not possible to {} {} with the request {{query}}"


class BaseMinimalResource(object):
    tag = []
    doc = None
    schema: Optional[Callable] = None


class BaseResource(BaseMinimalResource):
    lcp_handler = {}
    ignore_fields = []
    name = None
    names = None

    def __init__(self):
        if self.doc is not None:
            self.log = Log.get(self.doc.Index.name)
            err_es_init = True
            while err_es_init:
                try:
                    self.log.info(f"Start initialization index {self.doc.Index.name}")
                    self.doc.init()
                    self.log.success(f"Index {self.doc.Index.name} initialized")
                    err_es_init = False
                except Exception as exception:
                    self.log.exception(
                        MSG_INIT_INDEX_NOT_POSSIBLE.format(self.doc.Index.name),
                        exception,
                    )
                    self.log.info(MSG_WAITING_CONN.format(ArgReader.db.es_retry_period))
                    sleep(ArgReader.db.es_retry_period)
        else:
            Log.get(self.__class__.__name__).warning("doc not set")

    def on_base_get(self, req, resp, _id=None):
        req_data = req.media or {}
        qrs = QueryRequestSchema(method=HTTPMethod.GET, unknown="INCLUDE")
        resp_data, valid = qrs.validate(data=req_data, item_id=_id)
        if valid:
            try:
                query_reader = QueryReader(index=self.doc.Index.name)
                search = query_reader.parse(query=req_data, item_id=_id)
                if resp_data := [
                    dict(hit.to_dict(), id=hit.meta.id) for hit in search.execute()
                ]:
                    ContentResponse(resp_data).apply(resp)
                else:
                    NotFoundResponse(
                        MSG_NOT_FOUND.format(self.name.capitalize()), query=req_data
                    ).apply(resp)
            except Exception as exception:
                UnprocEntityResponse(
                    MSG_NOT_POSSIBLE.format("get", self.names),
                    exception,
                    query=req_data,
                ).apply(resp)
        else:
            resp_data.apply(resp)

    def on_base_post(self, req, resp, _id=None):
        req_data = req.media or {}
        sch_obj = self.schema(
            many=is_list(req_data), unknown="INCLUDE", method=HTTPMethod.POST
        )
        resp_data, valid = sch_obj.validate(data=req_data, item_id=_id)
        if valid:
            req_data_wrap = wrap(req_data)
            if len(req_data_wrap) > 0:
                for req_data in req_data_wrap:
                    req_data_lcp = deepcopy(req_data)
                    req_data_id = req_data.pop("id", _id)
                    try:
                        self.rm_ignore_fields(req_data)
                        obj = self.doc(meta={"id": req_data_id}, **req_data)
                        resp_data_lcp = []
                        resp_data = CreatedResponse(
                            MSG_OK.format(
                                self.name.capitalize(), req_data_id, "created"
                            )
                        )
                        hndl = self.get_lcp_handler(HTTPMethod.POST)
                        hndl(instance=obj, req=req_data_lcp, resp=resp_data_lcp)
                        if resp_data_lcp:
                            for rdl in resp_data_lcp:
                                if rdl["error"]:
                                    resp_data = UnprocEntityResponse(
                                        MSG_NOT_POSSIBLE_ID.format(
                                            "create", self.name, req_data_id
                                        )
                                    )  # noqa: E501
                                    break
                            resp_data.update(lcp_response=resp_data_lcp)
                        force = req_data.get("force", False)
                        if not resp_data.error or force:
                            obj.save()
                        if force:
                            resp_data = UnprocEntityResponse(
                                MSG_ERROR.format(self.name, req_data_id, "created")
                            )
                        resp_data.add(resp)
                    except Exception as exception:
                        UnprocEntityResponse(
                            MSG_NOT_POSSIBLE_ID.format(
                                "create",  # noqa: E501
                                self.name,  # noqa: E501
                                req_data_id,
                            ),  # noqa: E501
                            exception,
                        ).add(resp)
            else:
                NoContentResponse(
                    MSG_NO_CONTENT.format("create", self.names), request=req_data
                ).apply(resp)
        else:
            resp_data.apply(resp)

    def on_base_put(self, req, resp, _id=None):
        status_op = self.doc.Status_Operation
        req_data = req.media or {}
        sch_obj = self.schema(
            many=is_list(req_data),
            unknown="INCLUDE",
            partial=True,
            method=HTTPMethod.PUT,
        )
        rsp_dt, valid = sch_obj.validate(data=req_data, item_id=_id)
        if valid:
            req_data_wrap = wrap(req_data)
            if len(req_data_wrap) > 0:
                for req_data in req_data_wrap:
                    req_data_lcp = deepcopy(req_data)
                    req_data_id = req_data.pop("id", _id)
                    try:
                        if len(req_data) == 0:
                            NotModifiedResponse(
                                MSG_UPDATE_NOT_NEEDED.format(self.name, req_data_id)
                            ).add(resp)
                        else:
                            self.rm_ignore_fields(req_data)
                            obj = self.doc.get(id=req_data_id)
                            resp_data_lcp = []
                            hndl = self.get_lcp_handler(HTTPMethod.PUT)
                            modified = hndl(
                                instance=obj, req=req_data_lcp, resp=resp_data_lcp
                            )
                            rsp_dt = OkResponse(
                                MSG_OK.format(
                                    self.name.capitalize(),  # noqa: E501
                                    req_data_id,
                                    "updated",
                                )
                            )
                            if resp_data_lcp:
                                for rdl in resp_data_lcp:
                                    if rdl["error"]:
                                        rsp_dt = UnprocEntityResponse(
                                            MSG_NOT_POSSIBLE_ID.format(
                                                "update",  # noqa: E501
                                                self.name,  # noqa: E501
                                                req_data_id,
                                            )
                                        )  # noqa: E501
                                        break
                                rsp_dt.update(lcp_response=resp_data_lcp)
                            force = req_data.get("force", False)
                            if (not rsp_dt.error or force) and len(req_data) > 0:
                                res = obj.update(**req_data)
                                if res == status_op.UPDATED:
                                    modified = True
                                    if force:
                                        rsp_dt = UnprocEntityResponse(
                                            MSG_ERROR.format(
                                                self.name, req_data_id, "updated"
                                            )
                                        )
                            if not rsp_dt.error and not modified:
                                rsp_dt = NotModifiedResponse(
                                    MSG_UPDATE_NOT_NEEDED.format(self.name, req_data_id)
                                )
                            rsp_dt.add(resp)
                    except Exception as exception:
                        UnprocEntityResponse(
                            MSG_UPDATE_NOT_NEEDED.format(self.name, req_data_id),
                            exception,
                        ).add(resp)
            else:
                NoContentResponse(
                    MSG_NO_CONTENT.format("update", self.name), request=req_data
                ).apply(resp)
        else:
            rsp_dt.apply(resp)

    def on_base_delete(self, req, resp, _id=None):
        req_data = req.media or {}
        qrs = QueryRequestSchema(method=HTTPMethod.DELETE)
        resp_data, _ = qrs.validate(data=req_data, item_id=_id)
        if resp:
            try:
                query_reader = QueryReader(index=self.doc.Index.name)
                search = query_reader.parse(query=req_data, item_id=_id)
                hits = search.execute()
                if len(hits) > 0:
                    for hit in hits:
                        try:
                            obj = self.doc.get(id=hit.meta.id)
                            resp_data_lcp = []
                            resp_data = ResetContentResponse(
                                MSG_OK.format(
                                    self.name.capitalize(), hit.meta.id, "deleted"
                                )
                            )
                            hndl = self.get_lcp_handler(HTTPMethod.DELETE)
                            hndl(instance=obj, req=hit, resp=resp_data_lcp)
                            if resp_data_lcp:
                                for rdl in resp_data_lcp:
                                    if rdl["error"]:
                                        resp_data = UnprocEntityResponse(
                                            MSG_NOT_POSSIBLE_ID.format(
                                                "delete",  # noqa: E501
                                                self.name,  # noqa: E501
                                                hit.meta.id,
                                            )
                                        )  # noqa: E501
                                        break
                                resp_data.update(lcp_response=resp_data_lcp)
                            force = req_data.get("force", False)
                            if not resp_data.error or force:
                                obj.delete()
                            if force:
                                resp_data = UnprocEntityResponse(
                                    MSG_ERROR.format(self.name, hit.meta.id, "deleted")
                                )
                            resp_data.add(resp)
                        except Exception as exception:
                            UnprocEntityResponse(
                                MSG_NOT_POSSIBLE_ID.format(
                                    "delete", self.name, hit.meta.id
                                ),
                                exception,
                            ).add(resp)
                else:
                    NotFoundResponse(
                        MSG_NOT_FOUND.format(self.names.capitalize()), query=req_data
                    ).apply(resp)
            except Exception as exception:
                UnprocEntityResponse(
                    MSG_NOT_POSSIBLE.format("delete", self.names),
                    exception,
                    query=req_data,
                ).apply(resp)
        else:
            resp_data.apply(resp)

    def rm_ignore_fields(self, data):
        for ign_f in self.ignore_fields:
            if data.pop(ign_f, None) is not None:
                self.log.info(
                    f"Field {ign_f} in the request ignored when update {self.names}"
                )  # noqa: E501

    @classmethod
    def get_lcp_handler(cls, method):
        def __default(instance, req, resp):
            return resp

        return cls.lcp_handler.get(method, __default)
