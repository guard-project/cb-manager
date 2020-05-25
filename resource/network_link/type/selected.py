from document.network_link.type import NetworkLinkTypeDocument
from resource.base import BaseResource
from schema.network_link.type import NetworkLinkTypeSchema
from utils import swagger


@swagger(method='get',
         sum='Network Link Type Read (Single)',
         desc='Get the network link type with the given `id` and filtered by the query in the request body.',
         resp='Network link type with the given `id` and filtered by the query in the request body.')
@swagger(method='post',
         sum='Network Link Type Creation (Single)',
         desc='Create a new network link type with the given `id` .',
         resp='Network link type with the given `id` created.')
@swagger(method='delete',
         sum='Network Link Type Delete (Single)',
         desc='Delete the network link type with the given `id` and filtered by the query in the request body.',
         resp='Network link type with the given `id` and filtered by the query in the request body deleted.')
@swagger(method='put',
         sum='Network Link Type Update (Single)',
         desc='Update the network link type with the given `id`.',
         resp='Network link type with the given `id` updated.')
class NetworkLinkTypeSelectedResource(BaseResource):
    doc_cls = NetworkLinkTypeDocument
    doc_name = 'Network Link Type'
    routes = '/config/network-link-type/{id}'
    schema_cls =NetworkLinkTypeSchema
