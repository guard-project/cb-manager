from lib.response import Not_Found_Response
from utils.log import Log

__all__ = [
    'LCP'
]


class LCP(object):
    @staticmethod
    def from_doc(document, id, label, resp):
        try:
            return document.get(id=id)
        except Exception as e:
            LCP.__log().exception(e)
            msg = f'{label} with id={id} not found.'
            Not_Found_Response(msg, exception=e).add(resp)
            return None

    @staticmethod
    def from_catalog(catalog, id, label, resp):
        def __filter_id(x):
            return x.id == id
        ret = list(filter(__filter_id, catalog))
        if len(ret) == 1:
            return ret[0]
        else:
            msg = f'{label} with id={id} not found.'
            Not_Found_Response(msg).add(resp)
            return None

    @staticmethod
    def __log():
        return Log.get('lcp')
