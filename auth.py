from document.exec_env import ExecEnvDocument
from utils import hash


def auth(dev_username, dev_password):
    def handler(username, password):
        auth_data = [(dev_username, dev_password)]
        exec_env = ExecEnvDocument.get(id=username, ignore=404)
        if exec_env is not None and exec_env.lcp.last_heartbeat is not None:
            auth_data.append((exec_env.meta.id, exec_env.lcp.cb_password))
        if (username, hash(password)) in auth_data:
            return {'username': username}
        else:
            False
    return handler
