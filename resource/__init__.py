from resource.agent.catalog import Agent_Catalog_Resource, Agent_Catalog_Selected_Resource
from resource.agent.instance import Agent_Instance_Resource, Agent_Instance_Selected_Resource
from resource.algorithm.catalog import Algorithm_Catalog_Resource, Algorithm_Catalog_Selected_Resource
from resource.algorithm.instance import Algorithm_Instance_Resource, Algorithm_Instance_Selected_Resource
from resource.connection import Connection_Resource, Connection_Selected_Resource
from resource.dashboard import Dashboard_Resource
from resource.data import Data_Resource, Data_Selected_Resource
from resource.ebpf_program.catalog import eBPF_Program_Catalog_Resource, eBPF_Program_Catalog_Selected_Resource
from resource.ebpf_program.instance import eBPF_Program_Instance_Resource, eBPF_Program_Instance_Selected_Resource
from resource.event import Event_Resource, Event_Selected_Resource
from resource.exec_env import (Exec_Env_Resource, Exec_Env_Selected_Resource, Exec_Env_Type_Resource,
                               Exec_Env_Type_Selected_Resource)
from resource.network_link import (Network_Link_Resource, Network_Link_Selected_Resource, Network_Link_Type_Resource,
                                   Network_Link_Type_Selected_Resource)
from resource.pipeline import Pipeline_Resource, Pipeline_Selected_Resource

from utils.log import Log
from utils.sequence import wrap

db = [
    Agent_Catalog_Resource, Agent_Catalog_Selected_Resource,
    Agent_Instance_Resource, Agent_Instance_Selected_Resource,
    Algorithm_Catalog_Resource, Algorithm_Catalog_Selected_Resource,
    Algorithm_Instance_Resource, Algorithm_Instance_Selected_Resource,
    Connection_Resource, Connection_Selected_Resource,
    Dashboard_Resource,
    Data_Resource, Data_Selected_Resource,
    eBPF_Program_Catalog_Resource, eBPF_Program_Catalog_Selected_Resource,
    eBPF_Program_Instance_Resource, eBPF_Program_Instance_Selected_Resource,
    Event_Resource, Event_Selected_Resource,
    Exec_Env_Resource, Exec_Env_Selected_Resource,
    Exec_Env_Type_Resource, Exec_Env_Type_Selected_Resource,
    Network_Link_Resource, Network_Link_Selected_Resource,
    Network_Link_Type_Resource, Network_Link_Type_Selected_Resource,
    Pipeline_Resource, Pipeline_Selected_Resource
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
