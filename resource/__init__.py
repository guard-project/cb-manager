from resource.agent.catalog import (AgentCatalogResource,
                                    AgentCatalogSelectedResource)
from resource.agent.instance import (AgentInstanceResource,
                                     AgentInstanceSelectedResource)
from resource.algorithm.catalog import (AlgorithmCatalogResource,
                                        AlgorithmCatalogSelectedResource)
from resource.algorithm.instance import (AlgorithmInstanceResource,
                                         AlgorithmInstanceSelectedResource)
from resource.chain import ChainResource
from resource.connection import ConnectionResource, ConnectionSelectedResource
from resource.data import DataResource, DataSelectedResource
from resource.dev import DevResource
from resource.ebpf_program.catalog import (_eBPFProgramCatalogResource,
                                           _eBPFProgramCatalogSelectedResource)
from resource.ebpf_program.instance import (
    _eBPFProgramInstanceResource, _eBPFProgramInstanceSelectedResource)
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
    AgentCatalogResource,
    AgentCatalogSelectedResource,
    AgentInstanceResource,
    AgentInstanceSelectedResource,
    AlgorithmCatalogResource,
    AlgorithmCatalogSelectedResource,
    AlgorithmInstanceResource,
    AlgorithmInstanceSelectedResource,
    ChainResource,
    ConnectionResource,
    ConnectionSelectedResource,
    DevResource,
    DataResource,
    DataSelectedResource,
    _eBPFProgramCatalogResource,
    _eBPFProgramCatalogSelectedResource,
    _eBPFProgramInstanceResource,
    _eBPFProgramInstanceSelectedResource,
    EventResource,
    EventSelectedResource,
    ExecEnvResource,
    ExecEnvSelectedResource,
    ExecEnvTypeResource,
    ExecEnvTypeSelectedResource,
    NetworkLinkResource,
    NetworkLinkSelectedResource,
    NetworkLinkTypeResource,
    NetworkLinkTypeSelectedResource,
    PipelineResource,
    PipelineSelectedResource,
]

tags = [Resource.tag for Resource in db]


def routes(api, spec):
    log = Log.get("resource")
    for res_class in db:
        res = res_class()
        for route in wrap(res_class.routes):
            api.add_route(route, res)
            spec.path(resource=res)
            log.success(f"{route} endpoint configured")
