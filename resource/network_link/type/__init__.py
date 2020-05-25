from document.network_link.type import NetworkLinkTypeDocument
from resource.base import BaseResource
from schema.network_link.type import NetworkLinkTypeSchema
from utils import swagger


@swagger(method='get',
         sum='Network Link Type Read (Multiple)',
         desc='Get the list of network link types filtered by the query in the request body.',
         resp='List of network link types filtered by the query in the request body.')
@swagger(method='post',
         sum='Network Link Type Creation (Multiple)',
         desc='Create new network link types.',
         resp='Network link types created.')
@swagger(method='delete',
         sum='Network Link Type Delete (Multiple)',
         desc='Delete network link types filtered by the query in the request body.',
         resp='Network link types filtered by the query in the request body deleted.')
@swagger(method='put',
         sum='Network Link Type Update (Multiple)',
         desc='Update network link types.',
         resp='Network link types updated.')
class NetworkLinkTypeResource(BaseResource):
    doc_cls = NetworkLinkTypeDocument
    doc_name = 'Network Link Type'
    routes = '/config/network-link-type/'
    schema_cls =NetworkLinkTypeSchema
