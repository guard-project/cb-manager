from elasticsearch_dsl import connections
from time import sleep
from utils.log import Log


def connection(endpoint, timeout, retry_period):
    log = Log.get('elastic-search')
    try:
        log.info(f'Start connection to Elasticsearch ({endpoint})')
        connections.create_connection(hosts=endpoint, timeout=timeout)
    except Exception as exception:
        log.exception(f'Connection to Elasticsearch ({endpoint}) not possible', exception)
        log.warn(f'Try again in {retry_period} seconds')
        sleep(retry_period)
        connection(endpoint, timeout, retry_period)
    else:
        log.success(f'Connection to Elasticsearch ({endpoint}) established')
