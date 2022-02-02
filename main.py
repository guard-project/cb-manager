import os

path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)
os.chdir(dir_path)

import waitress  # noqa: E402
from rich import pretty, traceback  # noqa: E402
from rich.console import Console  # noqa: E402
from rich.panel import Panel  # noqa: E402

pretty.install()
traceback.install(show_locals=False)

from about import project, title, version  # noqa: E402
from api import api  # noqa: E402
from lib.elasticsearch import connection as es_conn  # noqa: E402
from reader.arg import ArgReader  # noqa: E402
from utils.log import Log  # noqa: E402

data_base = ArgReader.read()

if data_base.version is not None:
    print(data_base.version)
else:
    ident = f"{project} - {title} v:{version}"
    console = Console()
    console.print(Panel.fit(ident))
    Log.init(config=data_base.log_config)
    es_conn(
        endpoint=data_base.es_endpoint,
        timeout=data_base.es_timeout,
        retry_period=data_base.es_retry_period,
    )
    api_instance = api(title=title, version=version)
    Log.get("api").success(
        f"Accept requests at {data_base.host}:{data_base.port}"
    )
    waitress.serve(
        api_instance,
        host=data_base.host,
        port=data_base.port,
        expose_tracebacks=False,
        ident=ident,
        _quiet=True,
    )
