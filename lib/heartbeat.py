from threading import Thread, Timer

from requests import post
from requests.exceptions import ConnectionError, ConnectTimeout

from document.exec_env import ExecEnvDocument
from lib.http import HTTP_Status
from lib.token import create_token
from reader.arg import ArgReader
from utils.log import Log


def heartbeat():
    """Heartbeat procedure with the LCPs."""
    search = ExecEnvDocument.search()
    res = search[0:search.count()].execute()
    threads = []
    for exec_env in res:
        if exec_env.lcp:
            thread = Thread(target=heartbeat_exec_env, args=(exec_env,))
            threads.append(thread)
            thread.start()
    for thread in threads:
        thread.join()
    thread = Timer(ArgReader.db.hb_period, heartbeat)
    thread.daemon = True
    thread.start()


def heartbeat_exec_env(exec_env):
    log = Log.get('heartbeat')
    try:
        exec_env_id = exec_env.meta.id
        lcp = exec_env.lcp
        lbl = f'{exec_env_id} (LCP at {exec_env.hostname}:{lcp.port})'
        if exec_env.enabled:
            schema = 'https' if lcp.https else 'http'
            endpoint_lcp = exec_env.lcp.endpoint
            endpoint_lcp = '/' + endpoint_lcp if endpoint_lcp else ''
            req_uri = f'{schema}://{exec_env.hostname}:{lcp.port}{endpoint_lcp}/status'  # noqa F401
            resp = post(req_uri,
                        timeout=ArgReader.db.hb_timeout,
                        headers={'Authorization': create_token()},
                        json={'id': exec_env_id})
            if resp.status_code == HTTP_Status.OK:
                data = resp.json()
                exec_env_id = data.pop('id', None)
                lcp.started = data.get('started', None)
                lcp.last_heartbeat = data.get('last_heartbeat', None)
                log.success(f'Connection established with exec-env {lbl}')
            else:
                lcp.last_heartbeat = None
                log.warning(f'Connection reset with exec-env {lbl}')
                log.notice(f'Response: {resp.content}')
            if not lcp.https:
                lcp.https = False
            exec_env.save()
        else:
            log.notice(f'Exec-env {lbl} not enabled')
    except ConnectTimeout:
        log.error(f'Connection timeout with exec-env {lbl}')
    except ConnectionError:
        log.error(f'Connection refused with exec-env {lbl}')
    except Exception as exception:
        log.exception(
            f'Exception during connection with exec-env {lbl}', exception)
