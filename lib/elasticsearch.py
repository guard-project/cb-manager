from elasticsearch_dsl import connections
from time import sleep
from utils.log import Log


def connection(endpoint, timeout, retry_period):
    try:
        log = Log.get('elastic-search')
        log.info(f'start connection to Elasticsearch ({endpoint})')
        connections.create_connection(hosts=endpoint, timeout=timeout)
    except Exception as exception:
        log.error(f'Exception: {exception}')
        log.error(f'connection to Elasticsearch ({endpoint}) not possible')
        log.error(f'try again in {retry_period} seconds')
        sleep(retry_period)
        connection(endpoint, timeout, retry_period)
    else:
        log.success(f'connection to Elasticsearch ({endpoint}) established')
