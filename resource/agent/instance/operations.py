from document.agent.catalog import AgentCatalogDocument
from document.exec_env import ExecEnvDocument
from http import HTTPStatus
from log import Log
from utils import wrap

from resource.agent.instance.action import execute as execute_action
from resource.agent.instance.parameter import execute as execute_parameter


def data(req, resp):
    return list(zip(wrap(req.context.get('json', [])), resp.media))


def get(document, id, name, result):
    log = Log.get('operations')
    try:
        return document.get(id=id)
    except Exception as e:
        log.debug(e)
        result.append({
            'status': 'error',
            'reason': f'{name} {id} unknown.',
            'http_status_code': HTTPStatus.NOT_FOUND
        })
        return None


def send(req, resp, match_status):
    for req_item, resp_item in data(req, resp):
        if resp_item.get('status', None) == match_status:
            resp_item['operations'] = resp_op = []
            resp_data = resp_item.get('data')
            agent_catalog = get(document=AgentCatalogDocument, id=resp_data.get('agent_catalog_id', None),
                                name='Agent Catalog', result=resp_op)
            exec_env = get(document=ExecEnvDocument, id=resp_data.get('exec_env_id', None),
                           name='Execution Environment', result=resp_op)
            if agent_catalog and exec_env:
                execute_action(catalog=agent_catalog.actions, id=req_item.get('status', None),
                               exec_env=exec_env, result=resp_op)
                execute_parameter(catalog=agent_catalog.parameters, data=req_item.get('parameters', []),
                                  exec_env=exec_env, result=resp_op)
