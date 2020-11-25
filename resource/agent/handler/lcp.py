from document.agent.catalog import Agent_Catalog_Document
from document.exec_env import Exec_Env_Document
from lib.response import Unprocessable_Entity_Response
from requests import post as post_req
from requests.auth import HTTPBasicAuth as HTTP_Basic_Auth
from resource.base.handler.lcp import LCP as Base_LCP
from toolz import valmap
from utils.log import Log
from utils.sequence import expand, extract, is_dict, wrap

__all__ = [
    'LCP'
]

# TODO add resource to instance
# TODO check if work everything


class LCP(Base_LCP):
    def __init__(self, catalog, req, resp):
        self.log = Log.get('agent-instance-lcp')
        self.req = req
        self.resp = resp
        self.req_lcp = []
        self.actions = []
        self.parameters = []
        self.resources = []
        self.catalogs = dict(actions={}, parameters={}, resources={})
        operations = wrap(self.req.get('operations', []))
        for req_op in operations:
            req_lcp_op = {}
            self.req_lcp.append(req_lcp_op)
            self.__prepare(req_lcp_op, 'actions', catalog=catalog.actions,
                           data=req_op.get('actions', []), transform_handler=self.__transform_action)
            self.__prepare(req_lcp_op, 'parameters', catalog=catalog.parameters,
                           data=req_op.get('parameters', []), transform_handler=self.__transform_parameter)
            self.__prepare(req_lcp_op, 'resources', catalog=catalog.resources,
                           data=req_op.get('resources', []), transform_handler=self.__transform_resource)
        self.num = len(operations)

    @classmethod
    def handler(cls, instance, req, resp):
        agent_catalog = cls.from_doc(document=Agent_Catalog_Document, id=instance.agent_catalog_id,
                                     label='Agent Catalog', resp=resp)
        exec_env = cls.from_doc(document=Exec_Env_Document, id=instance.exec_env_id,
                                label='Execution Environment', resp=resp)
        if all([agent_catalog, exec_env]):
            return LCP(catalog=agent_catalog, req=req, resp=resp).__apply(instance=instance,
                                                                          exec_env=exec_env)
        return False

    def __apply(self, instance, exec_env):
        if self.num > 0:
            username, password = exec_env.lcp.username, exec_env.lcp.password
            resp_lcp = post_req(f'http://{exec_env.hostname}:{exec_env.lcp.port}/config',
                                auth=HTTP_Basic_Auth(username, password), json=self.req_lcp)
            if resp_lcp.content:
                try:
                    resp_lcp_data = resp_lcp.json()
                    if resp_lcp.status_code >= 300 or (is_dict(resp_lcp) and resp_lcp_data.get('error', False)):
                        Unprocessable_Entity_Response(resp_lcp_data) \
                            .add(self.resp)
                        return False
                    else:
                        save_actions = self.__save(instance=instance,
                                                   data=resp_lcp_data,
                                                   type='action',
                                                   catalogs=self.catalogs['actions'],
                                                   handler=self.__save_action)
                        save_parameters = self.__save(instance=instance,
                                                      data=resp_lcp_data,
                                                      type='parameter',
                                                      catalogs=self.catalogs['parameters'],
                                                      handler=self.__save_parameter)
                        save_resources = self.__save(instance=instance,
                                                     data=resp_lcp_data,
                                                     type='resource',
                                                     catalogs=self.catalogs['resources'],
                                                     handler=self.__save_resource)
                        if save_actions or save_parameters or save_resources:
                            instance.save()
                        self.resp.extend(wrap(resp_lcp_data))
                        return True
                except Exception as e:
                    msg = f'Response from LCP({exec_env.meta.id}@{exec_env.hostname}:{exec_env.lcp.port}) not valid'
                    self.log.exception(msg, e)
                    uer = Unprocessable_Entity_Response(msg, exception=e)
                    uer.add(self.resp)
                    return False
            else:
                msg = f'Request to LCP({exec_env.meta.id}@{exec_env.hostname}:{exec_env.lcp.port}) not executed'
                Unprocessable_Entity_Response(msg).add(self.resp)
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
                config.update(id=id)
                if type == 'action':
                    config['output_format'] = data_item.get('output_format', 'plain')
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

    def __transform_action(self, action, data):
        return valmap(lambda x: self.__frmt(x, data), action)

    def __transform_parameter(self, parameter, data):
        p = expand(parameter, value=data.get('value', None))
        return valmap(lambda x: self.__frmt(x, data), p)

    def __transform_resource(self, resource, data):
        r = expand(resource, content=data.get('content', None))
        return valmap(lambda x: self.__frmt(x, data), r)

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

    def __save_action(self, instance, doc, result, error):
        save = False
        if doc.status is not None:
            instance.status = doc.status if not error else 'unknown'
            save = True
        if not error:
            data = extract(result,
                           id='id',
                           data='stdout',
                           timestamp='timestamp')
            instance.edit_action(data)
            save = True
        return save

    def __save_parameter(self, instance, doc, result, error):
        if not error:
            data = extract(result,
                           id='id',
                           timestamp='timestamp')
            val = result.get('value', None)
            if is_dict(val):
                data.update(**extract(val, value='new'))
            else:
                data.update(value=val)
            instance.edit_parameter(data)
            return True
        return False

    def __save_resource(self, instance, doc, result, error):
        if not error:
            data = extract(result,
                           id='id',
                           path='path',
                           content='content',
                           timestamp='timestamp')
            instance.edit_resource(data)
            return True
        return False
