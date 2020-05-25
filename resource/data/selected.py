from document.data import DataDocument
from resource.base import BaseResource
from schema.data import DataSchema
from utils import swagger


@swagger(method='get',
         sum='Data Read (Single)',
         desc='Get the data with the given `id` and filtered by the query in the request body.',
         resp='Data with the given `id` and filtered by the query in the request body.')
@swagger(method='post',
         sum='Data Insert (Single)',
         desc='Insert new data with the given `id`.',
         resp='Data with the given `id` inserted.')
@swagger(method='delete',
         sum='Data Delete (Single)',
         desc='Delete data with the given `id` and filtered by the query in the request body.',
         resp='Data with the given `id` and filtered by the query in the request body deleted.')
@swagger(method='put',
         sum='Data Update (Single)',
         desc='Update data with the given `id`.',
         resp='Data with the given `id` updated.')
class DataSelectedResource(BaseResource):
    doc_cls = DataDocument
    doc_name = 'Data'
    routes = '/data/{id}',
    schema_cls =DataSchema
