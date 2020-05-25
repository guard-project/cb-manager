from reader.arg import ArgReader
from datetime import datetime, timedelta
from document.exec_env import ExecEnvDocument
from http import HTTPStatus
from requests import post
from requests.auth import HTTPBasicAuth
from resource.base import BaseResource
from threading import Timer
from schema.exec_env import ExecEnvSchema
from schema.exec_env.type import ExecEnvTypeSchema
from utils import datetime_to_str, generate_password, hash, swagger


@swagger(method='get',
         sum='Execution Environment Read (Multiple)',
         desc='Get the list of execution environments filtered by the query in the request body.',
         resp='List of execution environments filtered by the query in the request body.')
@swagger(method='post',
         sum='Execution Environment Creation (Multiple)',
         desc='Create new execution environments.',
         resp='Execution environments created.')
@swagger(method='delete',
         sum='Execution Environment Delete (Multiple)',
         desc='Delete execution environments filtered by the query in the request body.',
         resp='Execution environments filtered by the query in the request body deleted.')
@swagger(method='put',
         sum='Execution Environment Update (Multiple)',
         desc='Update execution environments.',
         resp='Execution environments updated.')
class ExecEnvResource(BaseResource):
    doc_cls = ExecEnvDocument
    doc_name = 'Execution Environment'
    routes = '/config/exec-env/'
    schema_cls =ExecEnvSchema

    def __init__(self):
        super().__init__()
        self.heartbeat()

    def heartbeat(self):
        """
        Heartbeat procedure with the LCPs.
        """
        s = ExecEnvDocument.search()
        res = s.execute()
        for exec_env in res:
            try:
                lcp = exec_env.lcp
                lcp_cb_password = generate_password()
                lcp.cb_password = hash(lcp_cb_password)
                lcp.cb_expiration = datetime_to_str(datetime.now() + timedelta(seconds=ArgReader.db.hb_auth_expiration))
                auth = { 'username': lcp.username, 'password': lcp.password } if lcp.last_heartbeat else {}
                resp = post(f'http://{exec_env.hostname}:{lcp.port}/status', timeout=ArgReader.db.hb_timeout,
                           json={ 'id': exec_env.meta.id, **auth, 'cb_password': lcp_cb_password,
                                  'cb_expiration': lcp.cb_expiration })
            except Exception as e:
                self.log.debug(e)
                lcp.username = lcp.password = lcp.last_heartbeat = None
                exec_env.save()
            else:
                try:
                    if resp.status_code == HTTPStatus.OK:
                        data = resp.json()
                        lcp.username = data.get('username', None)
                        lcp.password = data.get('password', None)
                        lcp.last_heartbeat = data.get('last_hearthbeat', None)
                        self.log.success(f'LCP Connection with id = {exec_env.meta.id} established')
                    else:
                        self.log.warning(f'Reset LCP connection with id = {exec_env.meta.id}')
                        lcp.username = lcp.password = lcp.last_heartbeat = None
                except Exception as e:
                    self.log.debug(e)
                    lcp.username = lcp.password = lcp.last_heartbeat = None
                else:
                    exec_env.save()
        t = Timer(ArgReader.db.hb_period, self.heartbeat)
        t.daemon = True
        t.start()
