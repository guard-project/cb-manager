import os

Import_Error = ImportError
path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)
os.chdir(dir_path)

while True:
    from utils.exception import reload_import
    try:
        from about import title, version
        from api import api
        from lib.elasticsearch import connection as es_conn
        from reader.arg import Arg_Reader
        from werkzeug.serving import run_with_reloader
        import waitress
        break
    except ImportError as error:
        reload_import(error)

db = Arg_Reader.read()

print(f'{title} version:{version}')

if db.version is not None:
    print(db.version)
else:
    es_conn(endpoint=db.es_endpoint, timeout=db.es_timeout,
            retry_period=db.es_retry_period)

    @run_with_reloader
    def run_server():
        waitress.serve(api(title=title, version=version,
                           dev_username=db.dev_username, dev_password=db.dev_password),
                       host=db.host, port=db.port, expose_tracebacks=False)

    run_server()
