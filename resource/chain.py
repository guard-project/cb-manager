from glob import has_magic
from resource.base import BaseMinimalResource

from document.agent.instance import AgentInstanceDocument
from document.connection import ConnectionDocument
from document.exec_env import ExecEnvDocument
from document.network_link import NetworkLinkDocument
from lib.response import (BadRequestResponse, NotFoundResponse, OkResponse,
                          UnprocEntityResponse)


class ChainResource(BaseMinimalResource):
    routes = "/chain/{_id}"

    def __delete_agent_instance(self, exec_env_id, resp):
        self.__delete_doc(AgentInstanceDocument, exec_env_id, resp)

    def __delete_connection(self, exec_env_id, resp):
        self.__delete_doc(ConnectionDocument, exec_env_id, resp,
                          trigger_fn=self.__delete_network_link)

    def __delete_doc(self, doc, target_val, resp, target='exec_env_id',
                     trigger_fn=None):
        search = doc.search()
        items = search[:search.count()].execute()
        for item in items:
            val = item.meta.id if target == "_id" else getattr(item, target)
            if val == target_val:
                try:
                    item.delete()
                    if trigger_fn is not None:
                        trigger_fn(item, resp)
                except Exception as e:
                    print(e)
                    UnprocEntityResponse(
                        f"Failed to delete {doc.__name__} with id={item.meta.id}") \
                        .add(resp)

    def __delete_network_link(self, conn, resp):
        self.__delete_doc(NetworkLinkDocument,
                          conn.network_link_id, resp, target='_id')

    def __delete_exec_env(self, _id, resp):
        exec_env = ExecEnvDocument.get(id=_id, ignore=404)
        if exec_env is None:
            NotFoundResponse(
                f"Exec env with id={_id} not found").apply(resp)
        else:
            if hasattr(exec_env, 'root') and exec_env.root and _id != exec_env.root:
                self.__delete_exec_env(exec_env.root, resp)
            try:
                sons = exec_env.lcp.sons
            except Exception:
                sons = []
            for id_son in sons:
                self.__delete_exec_env(id_son, resp)
            self.__delete_agent_instance(_id, resp)
            self.__delete_connection(_id, resp)
            exec_env.delete()

    def on_delete(self, _, resp, _id=None):
        if _id is None:
            BadRequestResponse().apply(resp)
        else:
            self.__delete_exec_env(_id, resp)
            OkResponse(f'Chain {_id} deleted').apply(resp)
