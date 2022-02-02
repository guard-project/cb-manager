from resource.base.handler.lcp import LCP as BaseLCP

from requests import post as post_req
from toolz import valmap

from document.agent.catalog import AgentCatalogDocument
from document.exec_env import ExecEnvDocument
from lib.response import UnprocEntityResponse
from lib.token import create_token
from utils.log import Log
from utils.sequence import expand, is_dict, wrap

# TODO add resource to instance
# TODO check if work everything


MSG_RESP_NOT_VALID = 'Response from LCP({id}@{hostname}:{port}) not valid'
MSG_REQ_LCP_NOT_EXEC = 'Request to LCP({id}@{hostname}:{port}) not executed'


class LCP(BaseLCP):
    def __init__(self, catalog, req, resp):
        self.log = Log.get('agent-instance-lcp')
        self.req = req
        self.resp = resp
        self.req_lcp = []
        self.actions = []
        self.parameters = []
        self.resources = []
        self.catalogs = {'actions': {}, 'parameters': {}, 'resources': {}}
        operations = wrap(self.req.get('operations', []))
        for req_op in operations:
            req_lcp_op = {}
            self.req_lcp.append(req_lcp_op)
            self.__prepare(req_lcp_op, 'actions', catalog=catalog.actions,
                           data=req_op.get('actions', []),
                           transform_handler=self.__transform_action)
            self.__prepare(req_lcp_op, 'parameters',
                           catalog=catalog.parameters,
                           data=req_op.get('parameters', []),
                           transform_handler=self.__transform_parameter)
            self.__prepare(req_lcp_op, 'resources', catalog=catalog.resources,
                           data=req_op.get('resources', []),
                           transform_handler=self.__transform_resource)
        self.num = len(operations)

    @classmethod
    def handler(cls, instance, req, resp):
        agent_catalog = cls.from_doc(document=AgentCatalogDocument,
                                     doc_id=instance.agent_catalog_id,
                                     label='Agent Catalog', resp=resp)
        exec_env = cls.from_doc(document=ExecEnvDocument,
                                id=instance.exec_env_id,
                                label='Execution Environment', resp=resp)
        if all([agent_catalog, exec_env]):
            lcp = LCP(catalog=agent_catalog, req=req, resp=resp)
            return lcp.__apply(instance=instance,
                               exec_env=exec_env)
        return False

    def __apply(self, instance, exec_env):
        if self.num > 0:
            schema = 'https' if exec_env.lcp.https else 'http'
            _hostname, _port = exec_env.hostname, exec_env.lcp.port
            endpoint_lcp = exec_env.lcp.endpoint
            endpoint_lcp = f'/{endpoint_lcp}' if endpoint_lcp else ''
            req_uri = f'{schema}://{_hostname}{_port}{endpoint_lcp}/config'
            resp_lcp = post_req(req_uri,
                                headers={'Authorization': create_token()},
                                json=self.req_lcp)
            if resp_lcp.content:
                try:
                    resp_lcp_data = resp_lcp.json()
                    if (resp_lcp.status_code >= 300 or
                            (is_dict(resp_lcp) and
                             resp_lcp_data.get('error', False))):
                        UnprocEntityResponse(resp_lcp_data) \
                            .add(self.resp)
                        return False
                    else:
                        _cat = self.catalogs['actions']
                        save_act = self.__save(instance,
                                               data=resp_lcp_data,
                                               typology='action',
                                               catalogs=_cat,
                                               handler=self.__save_act)
                        _cat = self.catalogs['parameters']
                        save_params = self.__save(instance,
                                                  data=resp_lcp_data,
                                                  typology='parameter',
                                                  catalogs=_cat,
                                                  handler=self.__save_params)
                        _cat = self.catalogs['resources']
                        save_res = self.__save(instance,
                                               data=resp_lcp_data,
                                               typology='resource',
                                               catalogs=_cat,
                                               handler=self.__save_res)
                        if save_act or save_params or save_res:
                            instance.save()
                        self.resp.extend(wrap(resp_lcp_data))
                        return True
                except Exception as exception:
                    _msg = MSG_RESP_NOT_VALID.format(exec_env.meta.id,
                                                     exec_env.hostname,
                                                     exec_env.lcp.port)
                    self.log.exception(_msg, exception)
                    UnprocEntityResponse(_msg,
                                         exception=exception).add(self.resp)
                    return False
            else:
                _msg = MSG_REQ_LCP_NOT_EXEC.format(exec_env.meta.id,
                                                   exec_env.hostname,
                                                   exec_env.lcp.port)
                UnprocEntityResponse(_msg).add(self.resp)
                return False
        return False

    def __prepare(self, req_op, typology, catalog, data, transform_handler):
        req_op[typology] = []
        for data_item in wrap(data):
            data_id = data_item.get('id', None)
            is_lcp_from_catalog = LCP.from_catalog(catalog=catalog, id=data_id,
                                                   label=typology.title(),
                                                   resp=self.resp)
            if (
                catalog_doc := self.catalogs[typology].get(data_id, None)
                or is_lcp_from_catalog
            ):
                self.catalogs[typology][data_id] = catalog_doc
                cfg_dict = catalog_doc.config.to_dict()
                config = transform_handler(cfg_dict, data_item)
                config.update(**data_item)
                self.log.info(f'Prepare {typology}: {config}')
                req_op[typology].append(config)

    def __frmt(self, prop, data):
        if isinstance(prop, (list, tuple)):
            return [self.__frmt(i, data) for i in prop]
        try:
            return prop.format(**data)
        except Exception:
            self.log.warn(f'Not possible to format {prop}')
            return prop

    def __transform_action(self, action, data):
        return valmap(lambda x: self.__frmt(x, data), action)

    def __transform_parameter(self, parameter, data):
        param = expand(parameter, value=data.get('value', None))
        return valmap(lambda x: self.__frmt(x, data), param)

    def __transform_resource(self, resource, data):
        res = expand(resource, content=data.get('content', None))
        return valmap(lambda x: self.__frmt(x, data), res)

    def __save(self, instance, data, typology, catalogs, handler):
        results = filter(lambda r: r.get('type', None) == typology, data)
        save = False
        for result in results:
            item_id = result.get('id', None)
            doc = catalogs.get(item_id, None)
            error = result.get('error', False)
            if handler(instance, doc, result, error):
                save = True
        return save

    def __save_act(self, instance, doc, result, error):
        save = False
        if doc.status is not None:
            instance.status = doc.status if not error else 'unknown'
            save = True
        if not error:
            instance.edit_action(result)
            save = True
        return save

    def __save_params(self, instance, _, result, error):
        if not error:
            instance.edit_parameter(result)
            return True
        return False

    def __save_res(self, instance, _, result, error):
        if not error:
            instance.edit_resource(result)
            return True
        return False
