from resource.agent.catalog import (AgentCatalogResource,
                                    AgentCatalogSelectedResource)
from resource.agent.instance import (AgentInstanceResource,
                                     AgentInstanceSelectedResource)
from resource.algorithm.catalog import (AlgorithmCatalogResource,
                                        AlgorithmCatalogSelectedResource)
from resource.algorithm.instance import (AlgorithmInstanceResource,
                                         AlgorithmInstanceSelectedResource)
from resource.connection import ConnectionResource, ConnectionSelectedResource
from resource.dashboard import DashboardResource
from resource.data import DataResource, DataSelectedResource
from resource.ebpf_program.catalog import (eBPFProgramCatalogResource,
                                           eBPFProgramCatalogSelectedResource)
from resource.ebpf_program.instance import (
    eBPFProgramInstanceResource, eBPFProgramInstanceSelectedResource)
from resource.event import EventResource, EventSelectedResource
from resource.exec_env import (ExecEnvResource, ExecEnvSelectedResource,
                               ExecEnvTypeResource,
                               ExecEnvTypeSelectedResource)
from resource.network_link import (NetworkLinkResource,
                                   NetworkLinkSelectedResource,
                                   NetworkLinkTypeResource,
                                   NetworkLinkTypeSelectedResource)
from resource.pipeline import PipelineResource, PipelineSelectedResource

from utils.log import Log
from utils.sequence import wrap

db = [
    AgentCatalogResource, AgentCatalogSelectedResource,
    AgentInstanceResource, AgentInstanceSelectedResource,
    AlgorithmCatalogResource, AlgorithmCatalogSelectedResource,
    AlgorithmInstanceResource, AlgorithmInstanceSelectedResource,
    ConnectionResource, ConnectionSelectedResource,
    DashboardResource,
    DataResource, DataSelectedResource,
    eBPFProgramCatalogResource, eBPFProgramCatalogSelectedResource,
    eBPFProgramInstanceResource, eBPFProgramInstanceSelectedResource,
    EventResource, EventSelectedResource,
    ExecEnvResource, ExecEnvSelectedResource,
    ExecEnvTypeResource, ExecEnvTypeSelectedResource,
    NetworkLinkResource, NetworkLinkSelectedResource,
    NetworkLinkTypeResource, NetworkLinkTypeSelectedResource,
    PipelineResource, PipelineSelectedResource
]

tags = [Resource.tag for Resource in db]


def routes(api, spec):
    log = Log.get('resource')
    for res_class in db:
        res = res_class()
        for route in wrap(res_class.routes):
            api.add_route(route, res)
            spec.path(resource=res)
            log.success(f'{route} endpoint configured')
