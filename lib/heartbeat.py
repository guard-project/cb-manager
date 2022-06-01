from threading import Thread, Timer

from requests import get, post
from requests.exceptions import ConnectionError, ConnectTimeout

from document.agent.catalog import AgentCatalogDocument
from document.agent.instance import AgentInstanceDocument
from document.connection import ConnectionDocument
from document.exec_env import ExecEnvDocument
from document.network_link import NetworkLinkDocument
from lib.http import HTTP_Status
from lib.token import create_token
from reader.arg import ArgReader
from utils.log import Log


def heartbeat():
    """Heartbeat procedure with the LCPs."""
    search = ExecEnvDocument.search()
    res = search[: search.count()].execute()
    threads = []
    for exec_env in res:
        if exec_env.lcp:
            thread = Thread(target=heartbeat_exec_env, args=(exec_env,))
            threads.append(thread)
            thread.start()
    for thread in threads:
        thread.join()
    thread = Timer(ArgReader.db.hb_period, heartbeat)
    thread.daemon = True
    thread.start()


def heartbeat_exec_env(exec_env):
    log = Log.get("heartbeat")
    try:
        exec_env_id = exec_env.meta.id
        lcp = exec_env.lcp
        lbl = f"{exec_env_id} (LCP at {exec_env.hostname}:{lcp.port})"
        if exec_env.enabled:
            schema = "https" if lcp.https else "http"
            endpoint_lcp = exec_env.lcp.endpoint
            endpoint_lcp = f"/{endpoint_lcp}" if endpoint_lcp else ""
            req_uri = f"{schema}://{exec_env.hostname}:{lcp.port}{endpoint_lcp}/status"  # noqa F401
            resp = post(
                req_uri,
                timeout=ArgReader.db.hb_timeout,
                headers={"Authorization": create_token()},
                json={"id": exec_env_id},
            )
            if resp.status_code == HTTP_Status.OK:
                data = resp.json()
                exec_env_id = data.pop("id", None)
                lcp.started = data.get("started", None)
                lcp.last_heartbeat = data.get("last_heartbeat", None)
                log.success(f"Connection established with exec-env {lbl}")
            else:
                lcp.last_heartbeat = None
                log.warning(f"Connection reset with exec-env {lbl}")
                log.notice(f"Response: {resp.content}")
            if not lcp.https:
                lcp.https = False
            resp = get(
                f"{schema}://{exec_env.hostname}:{lcp.port}{endpoint_lcp}/poll",  # noqa F401
                timeout=ArgReader.db.hb_timeout,
                headers={"Authorization": create_token()},
            )
            if resp.status_code == HTTP_Status.OK:
                data = resp.json()
                # ExecEnv
                exec_env_data = data.get("exec_env", {})
                exec_env.meta.id = exec_env_data.pop("id")
                # LCP data
                for field, lcp_data in exec_env_data.pop("lcp", {}).items():
                    setattr(exec_env.lcp, field, lcp_data)
                # ExecEnv data
                for field, ee_data in exec_env_data.items():
                    setattr(exec_env, field, ee_data)
                log.success(f"Polling established with exec-env {lbl}")
            else:
                log.warning(f"Polling not possible with exec-env {lbl}")
            exec_env.save()
            if resp.status_code == HTTP_Status.OK:
                # Network Link and Connections:
                exec_env_data = data.get("exec_env", {})
                for net_link in exec_env_data.get('network_links', []):
                    net_link_id = net_link.pop('id')
                    net_link_doc = NetworkLinkDocument.get_or_new(net_link_id)
                    for field, value in net_link.items():
                        setattr(net_link_doc, field, value)
                    net_link_doc.save()
                    conn_id = f'{exec_env_id}@{net_link_id}'
                    conn_doc = ConnectionDocument.get_or_new(conn_id)
                    conn_doc.exec_env_id = exec_env_id
                    conn_doc.network_link_id = net_link_id
                    conn_doc.save()
                    log.success(
                        f"Update network {net_link_id} and "
                        f"connection with {exec_env_id}"
                        f"from {net_link_id}"
                    )
                # Agent Type (Catalog)
                for agent_cat_data in data.get("agentType", []):
                    agent_cat_data_id = agent_cat_data.get("id", None)
                    AgentCatalogDocument.from_agent_type(agent_cat_data)
                    log.success(
                        f"Update agent catalog: {agent_cat_data_id} "
                        f"from {exec_env_id}"
                    )
                # Agent Instances
                for agent_inst_data in data.get("agentInstance", []):
                    agent_inst_data_id = agent_inst_data["id"]
                    agent_inst_data["agent_catalog_id"] = agent_inst_data[
                        "hasAgentType"
                    ]  # noqa E501
                    AgentInstanceDocument.from_agent_instance(
                        agent_inst_data, exec_env_id
                    )
                    log.success(
                        f"Update agent instance: {agent_inst_data_id} "
                        f"from {exec_env_id}"
                    )  # noqa E501
                # LCP Sons
                for lcp_son in data.pop("lcpSons", []):
                    lcp_son_id = lcp_son.pop("id", None)
                    exec_env_son = ExecEnvDocument.get_or_new(lcp_son_id)
                    for field, ee_data in lcp_son.items():
                        setattr(exec_env_son, field, ee_data)
                        exec_env_son.discovered = True
                    exec_env_son.save()
                    log.success(f"Update exec-env/lcp: {lcp_son_id}")
        else:
            log.notice(f"Exec-env {lbl} not enabled")
    except ConnectTimeout:
        log.error(f"Connection timeout with exec-env {lbl}")
    except ConnectionError:
        log.error(f"Connection refused with exec-env {lbl}")
    except Exception as exception:
        log.exception(
            f"Exception during connection with exec-env {lbl}", exception
        )
