from threading import Thread, Timer

from requests import post
from requests.exceptions import ConnectionError, ConnectTimeout

from document.exec_env import Exec_Env_Document
from lib.http import HTTP_Status
from lib.token import create_token
from reader.arg import Arg_Reader
from utils.log import Log


def heartbeat():
    """Heartbeat procedure with the LCPs."""
    s = Exec_Env_Document.search()
    res = s[0:s.count()].execute()
    threads = []
    for exec_env in res:
        if exec_env.lcp:
            t = Thread(target=heartbeat_exec_env, args=(exec_env,))
            threads.append(t)
            t.start()
    for t in threads:
        t.join()
    t = Timer(Arg_Reader.db.hb_period, heartbeat)
    t.daemon = True
    t.start()


def heartbeat_exec_env(exec_env):
    log = Log.get('heartbeat')
    try:
        id = exec_env.meta.id
        lcp = exec_env.lcp
        lbl = f'{id} (LCP at {exec_env.hostname}:{lcp.port})'
        if exec_env.enabled:
            schema = 'https' if lcp.https else 'http'
            resp = post(f'{schema}://{exec_env.hostname}:{lcp.port}/status', timeout=Arg_Reader.db.hb_timeout,
                        headers={'Authorization': create_token()}, json={'id': id})
            if resp.status_code == HTTP_Status.OK:
                data = resp.json()
                id = data.pop('id', None)
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
        log.exception(f'Exception during connection with exec-env {lbl}', exception)
