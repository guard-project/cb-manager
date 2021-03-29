import os

Import_Error = ImportError
path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)
os.chdir(dir_path)

import waitress  # noqa: E402

from about import project, title, version  # noqa: E402
from api import api  # noqa: E402
from lib.elasticsearch import connection as es_conn  # noqa: E402
from reader.arg import Arg_Reader  # noqa: E402

db = Arg_Reader.read()

ident = f'{project} - {title} v:{version}'
print(ident)

if db.version is not None:
    print(db.version)
else:
    es_conn(endpoint=db.es_endpoint, timeout=db.es_timeout,
            retry_period=db.es_retry_period)

    waitress.serve(api(title=title, version=version),
                   host=db.host, port=db.port, expose_tracebacks=False, ident=ident)
