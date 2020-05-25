from http import HTTPStatus
from requests import post
from requests.auth import HTTPBasicAuth

def get(catalog, id, result):
    ret = list(filter(lambda x: x.id == id, catalog))
    if len(ret) == 1:
        return ret[0]
    else:
        result.append({
            'type': 'parameter',
            'status': 'error',
            'reason': f'Parameter {id} unknown.',
            'http_status_code': HTTPStatus.NOT_FOUND
        })
        return None


def execute(catalog, data, exec_env, result):
    for param_data in data:
        param = get(catalog=catalog, id=param_data.get('id', None), result=result)
        if param:
            resp = post(f'http://{exec_env.hostname}:{exec_env.lcp.port}/config',
                        auth=HTTPBasicAuth(exec_env.lcp.username, exec_env.lcp.password),
                        json={ 'parameters': dict(**param.config.to_dict(), value=param_data['value']) })
            result.append(resp.json())
