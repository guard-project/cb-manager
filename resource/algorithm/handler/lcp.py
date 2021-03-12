from resource.base.handler.lcp import LCP as Base_LCP

from requests import post as post_req
from requests.auth import HTTPBasicAuth as HTTP_Basic_Auth
from toolz import valmap

from document.algorithm.catalog import Algorithm_Catalog_Document
from document.exec_env import Exec_Env_Document
from lib.response import Unprocessable_Entity_Response
from utils.log import Log
from utils.sequence import expand, extract, is_dict, wrap

__all__ = [
    'LCP'
]


class LCP(Base_LCP):
    def __init__(self, catalog, req, resp):
        self.log = Log.get('algorithm-instance-lcp')
        self.req = req
        self.resp = resp
        self.req_lcp = []
        self.parameters = []
        self.catalogs = dict(actions={}, parameters={}, resources={})
        operations = wrap(self.req.get('operations', []))
        for req_op in operations:
            req_lcp_op = {}
            self.req_lcp.append(req_lcp_op)
            self.__prepare(req_lcp_op, 'parameters', catalog=catalog.parameters,
                           data=req_op.get('parameters', []), transform_handler=self.__transform_parameter)
        self.num = len(operations)

    @classmethod
    def handler(cls, instance, req, resp):
        algorithm_catalog = cls.from_doc(document=Algorithm_Catalog_Document, id=instance.algorithm_catalog_id,
                                         label='Algorithm Catalog', resp=resp)
        if algorithm_catalog:
            return LCP(catalog=algorithm_catalog, req=req, resp=resp).__apply(instance=instance)
        return False

    def __apply(self, instance):
        if self.num > 0:
            try:
                save_parameters = self.__save(instance=instance,
                                              type='parameter',
                                              catalogs=self.catalogs['parameters'],
                                              handler=self.__save_parameter)
                if save_parameters:
                    instance.save()
                return True
            except Exception as e:
                msg = f'Request not valid'
                self.log.exception(msg, e)
                uer = Unprocessable_Entity_Response(msg, exception=e)
                uer.add(self.resp)
                return False
        return False

    def __prepare(self, req_op, type, catalog, data, transform_handler):
        catalog_docs = []
        req_op[type] = []
        for data_item in wrap(data):
            id = data_item.get('id', None)
            catalog_doc = self.catalogs[type].get(id, None) or LCP.from_catalog(catalog=catalog, id=id,
                                                                                label=type.title(), resp=self.resp)
            if catalog_doc:
                self.catalogs[type][id] = catalog_doc
                d = catalog_doc.config.to_dict()
                config = transform_handler(d, data_item)
                config.update(**data_item)
                self.log.info(f'Prepare {type}: {config}')
                req_op[type].append(config)
        return catalog_docs

    def __frmt(self, x, data):
        if isinstance(x, (list, tuple)):
            return [self.__frmt(i, data) for i in x]
        else:
            try:
                return x.format(**data)
            except Exception as e:
                self.log.exception(f'Not possible to format {x}', e)
                return x

    def __transform_parameter(self, parameter, data):
        p = expand(parameter, value=data.get('value', None))
        return valmap(lambda x: self.__frmt(x, data), p)

    def __save(self, instance, data, type, catalogs, handler):
        results = filter(lambda r: r.get('type', None) == type, data)
        save = False
        for result in results:
            id = result.get('id', None)
            doc = catalogs.get(id, None)
            error = result.get('error', False)
            if handler(instance, doc, result, error):
                save = True
        return save

    def __save_parameter(self, instance, doc, result, error):
        if not error:
            instance.edit_parameter(result)
            return True
        return False
