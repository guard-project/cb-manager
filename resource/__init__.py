from resource.agent import *
from resource.algorithm import *
from resource.connection import *
from resource.dashboard import *
from resource.data import *
from resource.ebpf_program import *
from resource.event import *
from resource.exec_env import *
from resource.network_link import *
from utils.log import Log
from utils.sequence import wrap

__all__ = [
    'routes'
]

db = [
    Agent_Catalog_Resource, Agent_Catalog_Selected_Resource,
    Agent_Instance_Resource, Agent_Instance_Selected_Resource,
    Algorithm_Resource, Algorithm_Selected_Resource,
    Connection_Resource, Connection_Selected_Resource,
    Dashboard_Resource,
    Data_Resource, Data_Selected_Resource,
    eBPF_Program_Catalog_Resource, eBPF_Program_Catalog_Selected_Resource,
    eBPF_Program_Instance_Resource, eBPF_Program_Instance_Selected_Resource,
    Event_Resource, Event_Selected_Resource,
    Exec_Env_Resource, Exec_Env_Selected_Resource,
    Exec_Env_Type_Resource, Exec_Env_Type_Selected_Resource,
    Network_Link_Resource, Network_Link_Selected_Resource,
    Network_Link_Type_Resource, Network_Link_Type_Selected_Resource
]

tags = []
for Resource in db:
    tags.append(Resource.tag)


def routes(api, spec):
    log = Log.get('resource')
    for res_class in db:
        res = res_class()
        for route in wrap(res_class.routes):
            api.add_route(route, res)
            spec.path(resource=res)
            log.success(f'{route} endpoint configured')
