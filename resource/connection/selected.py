from document.connection import ConnectionDocument
from resource.base import BaseResource
from schema.connection import ConnectionSchema
from utils import swagger


@swagger(method='get',
         sum='Connection Read (Single)',
         desc="""Get the connection between execution environments with the given `id` and network links
                 filtered by the query in the request body.""",
          resp="""Connection between execution environments and network links with the given `id` and
                  filtered by the query in the request body.""")
@swagger(method='post',
         sum='Connection Creation (Single)',
         desc='Install a new connection between execution environments and network links with the given `id`.',
         resp='Connections created between execution environments and network links.')
@swagger(method='delete',
         sum='Connection Delete (Single)',
         desc="""Delete the connection between execution environments and network links with the given `id` and
                 filtered by the query in the request body.""",
         resp="""Connection between execution environments
                 and network links with the given `id` filtered by the query in the request body deleted.""")
@swagger(method='put',
         sum='Connection Update (Single)',
         desc='Update the connection between execution environments and network links with the given `id`.', resp='Connection between execution environments and network links with the given `id` updated.')
class ConnectionSelectedResource(BaseResource):
    doc_cls = ConnectionDocument
    doc_name = 'Connection'
    routes = '/config/connection/{id}'
    schema_cls =ConnectionSchema
