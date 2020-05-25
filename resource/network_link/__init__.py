from document.network_link import NetworkLinkDocument
from resource.base import BaseResource
from schema.network_link import NetworkLinkSchema
from utils import swagger


@swagger(method='get',
         sum='Network Link Read (Multiple)',
         desc='Get the list of network links filtered by the query in the request body.',
         resp='List of network links filtered by the query in the request body.')
@swagger(method='post',
         sum='Network Link Creation (Multiple)',
         desc='Create new network links.',
         resp='Network links created.')
@swagger(method='delete',
         sum='Network Link Delete (Multiple)',
         desc='Delete network links filtered by the query in the request body.',
         resp='Network links filtered by the query in the request body deleted.')
@swagger(method='put',
         sum='Network Link Update (Multiple)',
         desc='Update network links.',
         resp='Network links updated.')
class NetworkLinkResource(BaseResource):
    doc_cls = NetworkLinkDocument
    doc_name = 'Network Link'
    routes = '/config/network-link/'
    schema_cls =NetworkLinkSchema
