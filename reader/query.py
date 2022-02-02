# Copyright (c) 2020-2022 GUARD
# author: Alex Carrega <alessandro.carrega@cnit.it>

from bunch import Bunch
from elasticsearch import RequestError
from elasticsearch_dsl import Q, Search
from falcon.errors import HTTPBadRequest

from utils.log import Log
from utils.sequence import is_dict, is_list

MSG_NOT_VALID_JSON = {
    "title": "Not valid JSON",
    "description": "The request body is not a valid JSON or it is not encoded as UTF-8.",  # noqa: E501
}
MSG_UNKNOWN = "{} unknown"
MSG_REQ_NOT_VALID = {
    "title": "Request not valid",
    "description": "Order with not valid/missing data",
}
MSG_CLAUSE_NOT_VALID = Bunch(
    title="Request not valid",
    description="{} clause with not valid/missing data",
)


class QueryReader:
    def __init__(self, index):
        self.search = Search(index=index)

    def parse(self, query, item_id=None):
        try:
            self.__select(query)
            self.search.query = self.__where(query, _id=item_id)
            self.__order(query)
            self.__limit(query)
        except RequestError as req_err:
            raise HTTPBadRequest(title=req_err.error, description=req_err.info)
        except HTTPBadRequest as http_bad_req:
            raise http_bad_req
        except Exception as exception:
            Log.get("query-reader").error(f"Exception: {exception}")
            raise HTTPBadRequest(**MSG_NOT_VALID_JSON)  # noqa: E501
        return self.search

    def __select(self, query):
        self.search = self.search.source(query.get("select", None))

    def __where(self, query, _id=None):
        query_obj = None
        for operator, clause in query.get("where", {}).items():
            if operator == "and":
                if is_dict(clause):
                    for sub_op, sub_clause in clause.items():
                        if query_obj is None:
                            query_obj = self.__where(
                                {"where": {sub_op: sub_clause}}
                            )
                        else:
                            query_obj = query_obj & self.__where(
                                {"where": {sub_op: sub_clause}}
                            )
                elif is_list(clause):
                    for sub_clause in clause:
                        if query_obj is None:
                            query_obj = self.__where({"where": sub_clause})
                        else:
                            query_obj = query_obj & self.__where(
                                {"where": sub_clause}
                            )
            elif operator == "or":
                if is_dict(clause):
                    for sub_op, sub_clause in clause.items():
                        if query_obj is None:
                            query_obj = self.__where(
                                {"where": {sub_op: sub_clause}}
                            )
                        else:
                            query_obj = query_obj | self.__where(
                                {"where": {sub_op: sub_clause}}
                            )
                elif is_list(clause):
                    for sub_clause in clause:
                        if query_obj is None:
                            query_obj = self.__where({"where": sub_clause})
                        else:
                            query_obj = query_obj | self.__where(
                                {"where": sub_clause}
                            )
            elif operator == "not":
                query_obj = ~self.__where(clause)
            else:
                prop = self.__fix_target(clause.get("target", None))
                expr = clause.get("expr", None)
                if prop is None or expr is None:
                    raise HTTPBadRequest(
                        title=MSG_CLAUSE_NOT_VALID.title,
                        description=MSG_CLAUSE_NOT_VALID.description.format(
                            operator
                        ),
                    )
                if operator == "equals":
                    query_obj = Q("match_phrase", **{prop: expr})
                elif operator == "reg_exp":
                    query_obj = Q("regexp", **{prop: {"value": expr}})
                elif operator == "wildcard":
                    query_obj = Q("wildcard", **{prop: {"value": expr}})
                elif operator in ["lt", "lte", "gt", "gte"]:
                    query_obj = Q("range", **{prop: {operator: expr}})
                else:
                    raise HTTPBadRequest(
                        title=MSG_UNKNOWN.format("Operation"),
                        description=MSG_UNKNOWN.format(operator),
                    )  # noqa: E501
        if _id is not None:
            if query_obj is None:
                query_obj = Q("term", _id=_id)
            else:
                query_obj = query_obj & Q("term", _id=_id)
        return query_obj if query_obj is not None else Q()

    def __order(self, query):
        sort_list = []
        for order in query.get("order", []):
            prop = self.__fix_target(order.get("target", None))
            mode = order.get("mode", None)
            if prop is not None and mode is not None:
                sort_list.append(prop if mode == "asc" else f"-{prop}")
            else:
                raise HTTPBadRequest(**MSG_REQ_NOT_VALID)  # noqa: E501
        self.search = self.search.sort(*sort_list)

    def __limit(self, query):
        limit = query.get("limit", {})
        start = limit.get("from", 0)
        end = limit.get("to", self.search.count() - 1)
        self.search = self.search[start : (end + 1)]  # noqa: E203

    @staticmethod
    def __fix_target(prop):
        return "_id" if prop == "id" else prop
