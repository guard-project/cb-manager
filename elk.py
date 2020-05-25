from elasticsearch_dsl import connections
from log import Log
from time import sleep


def connection(endpoint, timeout, retry_period):
    log = Log.get('elk')
    try:
        log.info(f'start connection to Elasticsearch ({endpoint})')
        connections.create_connection(hosts=endpoint, timeout=timeout)
    except Exception as e:
        log.debug(e)
        log.error(f'connection to Elasticsearch ({endpoint}) not possible')
        log.error(f'try again in {retry_period} seconds')
        sleep(retry_period)
        elastic_connection()
    else:
        log.success(f'connection to Elasticsearch ({endpoint}) established')
