from http import HTTPStatus
from requests import post
from requests.auth import HTTPBasicAuth


def get(catalog, id, result):
    ret = list(filter(lambda x: x.id == id, catalog))
    if len(ret) == 1:
        return ret[0]
    else:
        result.append({
            'type': 'action',
            'status': 'error',
            'reason': f'Action {id} unknown.',
            'http_status_code': HTTPStatus.NOT_FOUND
        })
        return None


def execute(catalog, id, exec_env, result):
    if id:
        action = get(catalog=catalog, id=id, result=result)
        if action:
            resp = post(f'http://{exec_env.hostname}:{exec_env.lcp.port}/config',
                        auth=HTTPBasicAuth(exec_env.lcp.username, exec_env.lcp.password),
                        json={ 'actions': { "cmd": "ls" } })
            result.append(resp.json())
