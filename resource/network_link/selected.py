from document.network_link import NetworkLinkDocument
from resource.base import BaseResource
from schema.network_link import NetworkLinkSchema
from utils import swagger


@swagger(method='get',
         sum='Network Link Read (Single)',
         desc='Get the network link with the given `id` and filtered by the query in the request body.',
         resp='Network link with the given `id` and filtered by the query in the request body.')
@swagger(method='post',
         sum='Network Link Creation (Single)',
         desc='Create a new network link with the given `id` .',
         resp='Network link with the given `id` created.')
@swagger(method='delete',
         sum='Network Link Delete (Single)',
         desc='Delete the network link with the given `id` and filtered by the query in the request body.',
         resp='Network link with the given `id` and filtered by the query in the request body deleted.',)
@swagger(method='put',
         sum='Network Link Update (Single)',
         desc='Update the network link with the given `id`.',
         resp='Network link with the given `id` updated.')
class NetworkLinkSelectedResource(BaseResource):
    doc_cls = NetworkLinkDocument
    doc_name = 'Network Link'
    routes = '/config/network-link/{id}'
    schema_cls =NetworkLinkSchema
