from lib.response import NotFoundResponse
from utils.log import Log

MSG_ID_NOT_FOUND = "{label} with id={doc_id} not found."


class LCP(object):
    @staticmethod
    def from_doc(document, doc_id, label, resp):
        try:
            return document.get(id=doc_id)
        except Exception as exception:
            _msg = MSG_ID_NOT_FOUND.format(label, doc_id)
            LCP.__log().exception(_msg, exception)
            NotFoundResponse(_msg, exception).add(resp)
            return None

    @staticmethod
    def from_catalog(catalog, doc_id, label, resp):
        def __filter_id(data):
            return data.id == doc_id

        ret = list(filter(__filter_id, catalog))
        if len(ret) == 1:
            return ret[0]
        else:
            NotFoundResponse(MSG_ID_NOT_FOUND.format(label, doc_id)).add(resp)
            return None

    @staticmethod
    def __log():
        return Log.get("lcp")
