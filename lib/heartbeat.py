from reader.arg import Arg_Reader
from datetime import datetime, timedelta
from document.exec_env import Exec_Env_Document
from lib.http import HTTP_Status
from requests import post
from threading import Thread, Timer
from utils.datetime import datetime_from_str, datetime_to_str
from utils.hash import generate_password, hash
from utils.log import Log

__all__ = [
    'heartbeat'
]


def heartbeat():
    """Heartbeat procedure with the LCPs."""
    s = Exec_Env_Document.search()
    res = s.execute()
    threads = []
    for exec_env in res:
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
        if exec_env.enabled:
            resp = post(f'http://{exec_env.hostname}:{lcp.port}/status',
                        timeout=Arg_Reader.db.hb_timeout,
                        json=dict(id=id, username=lcp.username, password=lcp.password))
            if resp.status_code == HTTP_Status.OK:
                data = resp.json()
                id = data.pop('id', None)
                lcp.started = data.get('started', None)
                lcp.last_heartbeat = data.get('last_heartbeat', None)
                lcp.username = data.get('username', None)
                lcp.password = data.get('password', None)
                log.success(f'LCP Connection with {id} established')
            else:
                log.warning(f'Reset LCP connection with {id}')
                log.notice(f'response: {resp.content}')
                lcp.username = lcp.password = lcp.last_heartbeat = None
        else:
            exec_env.enabled = False # if the field is None in the record
            log.notice(f'Exec-env {id} at {exec_env.hostname} not enabled')
    except Exception as exception:
        log.error(f'Exception: {exception}')
        lcp.username = lcp.password = lcp.last_heartbeat = None
    else:
        exec_env.save()
