from document.data import DataDocument
from resource.base import BaseResource
from schema.data import DataSchema
from utils import swagger


@swagger(method='get',
         sum='Data Read (Multiple)',
         desc='Get the list of data filtered by the query in the request body.',
         resp='List of data filtered by the query in the request body.')
@swagger(method='post',
         sum='Data Insert (Multiple)',
         desc='Insert new data.',
         resp='Data inserted.')
@swagger(method='delete',
         sum='Data Delete (Multiple)',
         desc='Delete data filtered by the query in the request body.',
         resp='Data filtered by the query in the request body deleted.')
@swagger(method='put',
         sum='Data Update (Multiple)',
         desc='Update data.',
         resp='Data updated.')
class DataResource(BaseResource):
    doc_cls = DataDocument
    doc_name = 'Data'
    routes = '/data/',
    schema_cls =DataSchema
