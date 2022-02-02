from resource.base.handler.lcp import LCP as BaseLCP

from toolz import valmap

from document.algorithm.catalog import AlgorithmCatalogDocument
from lib.response import UnprocEntityResponse
from utils.log import Log
from utils.sequence import expand, wrap

MSG_REQ_NOT_VALID = "Request not valid"


class LCP(BaseLCP):
    def __init__(self, catalog, req, resp):
        self.log = Log.get("algorithm-instance-lcp")
        self.req = req
        self.resp = resp
        self.req_lcp = []
        self.parameters = []
        self.catalogs = {"actions": {}, "parameters": {}, "resources": {}}
        operations = wrap(self.req.get("operations", []))
        for req_op in operations:
            req_lcp_op = {}
            self.req_lcp.append(req_lcp_op)
            self.__prepare(
                req_lcp_op,
                "parameters",
                catalog=catalog.parameters,
                data=req_op.get("parameters", []),
                transform_handler=self.__transform_parameter,
            )
        self.num = len(operations)

    @classmethod
    def handler(cls, instance, req, resp):
        if algorithm_catalog := cls.from_doc(
            document=AlgorithmCatalogDocument,
            doc_id=instance.algorithm_catalog_id,
            label="Algorithm Catalog",
            resp=resp,
        ):
            return LCP(catalog=algorithm_catalog, req=req, resp=resp).__apply(instance)
        return False

    def __apply(self, instance):
        if self.num > 0:
            try:
                _cat = self.catalogs["parameters"]
                if self.__save(
                    instance,
                    typology="parameter",
                    catalogs=_cat,
                    handler=self.__save_parameter,
                ):
                    instance.save()
                return True
            except Exception as exception:
                self.log.exception(MSG_REQ_NOT_VALID, exception)
                UnprocEntityResponse(MSG_REQ_NOT_VALID, exception).add(self.resp)
                return False
        return False

    def __prepare(self, req_op, typology, catalog, data, transform_handler):
        req_op[typology] = []
        for data_item in wrap(data):
            data_id = data_item.get("id", None)
            is_lcp_from_catalog = LCP.from_catalog(
                catalog, id=data_id, label=typology.title(), resp=self.resp
            )
            if (
                catalog_doc := self.catalogs[typology].get(data_id, None)
                or is_lcp_from_catalog
            ):
                self.catalogs[typology][data_id] = catalog_doc
                doc_dict = catalog_doc.config.to_dict()
                config = transform_handler(doc_dict, data_item)
                config.update(**data_item)
                self.log.info(f"Prepare {typology}: {config}")
                req_op[typology].append(config)

    def __frmt(self, var, data):
        if isinstance(var, (list, tuple)):
            return [self.__frmt(i, data) for i in var]
        try:
            return var.format(**data)
        except Exception:
            self.log.warn(f"Not possible to format {var}")
            return var

    def __transform_parameter(self, parameter, data):
        param = expand(parameter, value=data.get("value", None))
        return valmap(lambda x: self.__frmt(x, data), param)

    def __save(self, instance, data, typology, catalogs, handler):
        results = filter(lambda r: r.get("type", None) == typology, data)
        save = False
        for result in results:
            doc_id = result.get("id", None)
            doc = catalogs.get(doc_id, None)
            error = result.get("error", False)
            if handler(instance, doc, result, error):
                save = True
        return save

    def __save_parameter(self, instance, doc, result, error):
        if not error:
            instance.edit_parameter(result)
            return True
        return False
