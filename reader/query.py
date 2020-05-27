from elasticsearch_dsl import Q, Search
from log import Log

import falcon
import elasticsearch
import utils


class QueryReader:
    def __init__(self, index):
        self.s = Search(index=index)

    def parse(self, query, id=None):
        try:
            self._select(query)
            self.s.query = self._where(query, id=id)
            self._order(query)
            self._limit(query)
        except elasticsearch.RequestError as req_error:
            raise falcon.HTTPBadRequest(
                title=req_error.error,
                description=req_error.info
            )
        except falcon.HTTPBadRequest as http_bad_req:
            raise http_bad_req
        except Exception as e:
            raise falcon.HTTPBadRequest(
                title='Not valid JSON',
                description='The request has a not valid JSON body.'
            )
        return self.s

    def _select(self, query):
        self.s = self.s.source(query.get('select', None))

    def _where(self, query, id=None):
        q = Q()
        for op, clause in query.get('where', {}).items():
            if op == 'and':
                for sub_op, sub_clause in clause.items():
                    q = q & self._where({'where': {sub_op: sub_clause}})
            elif op == 'or':
                for sub_op, sub_clause in clause.items():
                    q = q | self._where({'where': {sub_op: sub_clause}})
            elif op == 'not':
                q = ~self._where(clause)
            else:
                prop = utils.fix_target(clause.get('target', None))
                expr = clause.get('expr', None)
                if prop is not None and expr is not None:
                    if op == 'equals':
                        q = Q('term', **{prop: expr})
                    elif op == 'reg-exp':
                        q = Q('regexp', **{prop: dict(value=expr)})
                    elif op == 'wildcard':
                        q = Q('wildcard', **{prop: dict(value=expr)})
                    elif op in ['lt', 'lte', 'gt', 'gte']:
                        q = Q('range', **{prop: {op: expr}})
                    else:
                        raise falcon.HTTPBadRequest(
                            title = 'Operation unknown',
                            description=f'{op} unknown'
                        )
                else:
                    raise falcon.HTTPBadRequest(
                        title='Request not valid',
                        description=f'{op} clause with not valid/missing data'
                    )
        if id is not None:
            q = q & Q('term', _id=id)
        return q

    def _order(self, query):
        sort_list = []
        for order in query.get('order', []):
            prop = fix_target(order.get('target', None))
            mode = order.get('mode', None)
            if prop is not None and mode is not None:
                sort_list.append(prop if mode == 'asc' else f'-{prop}')
            else:
                raise falcon.HTTPBadRequest(
                    title='Request not valid',
                    description=f'order with not valid/missing data'
                )
        self.s = self.s.sort(*sort_list)

    def _limit(self, query):
        limit = query.get('limit', {})
        start = limit.get('from', None)
        end = limit.get('to', None)
        if end is None:
            if start is not None:
                self.s = self.s[start:]
        else:
            self.s = self.s[start:(end + 1)]
