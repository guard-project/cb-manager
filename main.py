import os
path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)
os.chdir(dir_path)

from api import api
from elk import connection as elk_conn
from reader.arg import ArgReader

import waitress

db = ArgReader.read()

print(f'{db.config.title} version:{db.config.version}')

if db.version is not None:
    print(db.version)
else:
    elk_conn(endpoint=db.es_endpoint, timeout=db.es_timeout, retry_period=db.es_retry_period)
    waitress.serve(api(title=db.config.title, version=db.config.version,
                       dev_username=db.dev_username, dev_password=db.dev_password),
                    host=db.host, port=db.port)
