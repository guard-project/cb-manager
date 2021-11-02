from resource.base.handler.lcp import LCP as BaseLCP

from requests import delete as delete_req
from requests import post as post_req
from requests import put as put_req

from document.ebpf_program.catalog import eBPFProgramCatalogDocument
from document.exec_env import ExecEnvDocument
from lib.response import UnprocEntityResponse
from lib.token import create_token
from utils.log import Log
from utils.sequence import wrap

MSG_RESP_NOT_VALID = 'Response from LCP({}@{}:{}) not valid'
MSG_REQ_NOT_EXEC = 'Request to LCP({}@{}:{}) not executed'

# FIXME parameters add to instance
# TODO check if work everything


class LCP(BaseLCP):
    def __init__(self, catalog, req, resp):
        self.log = Log.get('ebpf-program-instance-lcp')
        self.req = req
        self.resp = resp
        self.req_lcp = {}
        self.catalog = catalog

    @classmethod
    def post(cls, instance, req, resp):
        def __data(instance, catalog):
            return dict(id=instance.meta.id,
                        interface=req.get('interface', None),
                        **catalog.config.to_dict())
        cls.__handler(instance=instance, req=req, resp=resp,
                      caller=post_req, data=__data)

    @classmethod
    def put(cls, instance, req, resp):
        def __data(instance, catalog):
            return dict(id=instance.meta.id,
                        interface=req.get('interface', None),
                        **catalog.config.to_dict())
        cls.__handler(instance=instance, req=req, resp=resp,
                      caller=put_req, data=__data)

    @ classmethod
    def delete(cls, instance, req, resp):
        def __data(instance, _):
            return {'id': instance.meta.id}
        cls.__handler(instance=instance, req=req, resp=resp,
                      caller=delete_req, data=__data)

    @ classmethod
    def __handler(cls, instance, req, resp, caller, data):
        document = eBPFProgramCatalogDocument
        _id = instance.ebpf_program_catalog_id
        label = 'eBPF Program Catalog'
        ebpf_program_catalog = cls.from_doc(document, _id, label, resp)
        exec_env = cls.from_doc(document=ExecEnvDocument,
                                id=instance.exec_env_id,
                                label='Execution Environment', resp=resp)
        if all([ebpf_program_catalog, exec_env]):
            LCP(catalog=ebpf_program_catalog,
                req=req, resp=resp).__apply(instance=instance,
                                            exec_env=exec_env,
                                            caller=caller, data=data)

    def __apply(self, instance, exec_env, caller, data):
        hostname, port = exec_env.hostname, exec_env.lcp.port
        schema = 'https' if exec_env.lcp.https else 'http'
        ep_lcp = '/' + exec_env.lcp.endpoint if exec_env.lcp.endpoint else ''
        resp_caller = caller(f'{schema}://{hostname}:{port}{ep_lcp}/code',
                             headers={'Authorization': create_token()},
                             json=data(instance, self.catalog))
        if resp_caller.content:
            try:
                self.resp.extend(wrap(resp_caller.json()))
            except Exception as exception:
                _msg = MSG_RESP_NOT_VALID.format(exec_env.meta.id,
                                                 exec_env.hostname,
                                                 exec_env.lcp.port),
                self.log.exception(_msg, exception)
                UnprocEntityResponse(_msg, exception).add(self.resp)
        else:  # noqa F401
            UnprocEntityResponse(MSG_REQ_NOT_EXEC.format(exec_env.meta.id,
                                                         exec_env.hostname,
                                                         exec_env.lcp.port)).add(self.resp)  # noqa: E501
