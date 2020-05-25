# nprobe agent

- [nprobe agent](#nprobe-agent)
  - [Catalog](#catalog)
  - [Instance](#instance)
    - [Create](#create)
    - [Update](#update)

## Catalog

Add a new agent in the catalog with the REST POST method {cb_man_endpoint}:/catalog and the following request body:

```json
{
    "id": "nprobe",
    "parameters": [{
        "id": "network-interface",
        "type": "string",
        "example": "eth0",
        "description": "Set the network interface to probe",
        "config": {
            "schema": "properties",
            "source": "/etc/nprobe/nprobe.conf ",
            "path": [
                "-i"
            ]
        }
    },{
        "id": "capture-direction",
        "type": "integer",
        "example": 1,
        "description": "Specify packet capture direction: 0=RX+TX (default), 1=RX only, 2=TX only",
        "config": {
            "schema": "properties",
            "source": "/etc/nprobe/nprobe.conf ",
            "path": [
                "-capture-direction"
            ]
        }
    }],
    "actions": [{
            "id": "start",
            "config": {
                "cmd": "sudo systemctl start nprobe"
            }
        },
        {
            "id": "stop",
            "config": {
                "cmd": "sudo systemctl stop nprobe"
            }
        },
        {
            "id": "restart",
            "config": {
                "cmd": "sub systemctl restart nprobe"
            }
        }
    ]
}
```

{cb_man_endpoint} is the endpoint where the Context Broker Manager is installed.
The above code add a nprobe agent in the catalog with:

- 2 properties: network-interface, capture-direction;
- 3 actions: start, stop, restart.

## Instance

### Create

Add a new instance of nprobe in an exec-env with id = {exec_env_id} using the REST POST method
{context_broker_endpoint}:/config/agent.

```json
{
    "agent_catalog_id": "nprobe",
    "exec_env_id": "{exec_env_id}",
    "status": "stop",
    "parameters": [{
        "id": "network-interface",
        "value": "eth0"
    }],
    "id": "{exec_env_id}-nprobe"
}
```

This agent has the status set to "stop" and only 1 parameter set from the ones available in the catalog.

### Update

Update the configuration of nprobe instance using the REST PUT method {context_broker_endpoint}:/config/agent.

```json
{
    "agent_catalog_id": "nprobe",
    "parameters": [{
        "id": "network-interface",
        "value": "eth1"
    },{
        "id": "capture-direction",
        "value": 2
    }],
}
```

This example changes the value of network-interface parameter to "eth1" and add the capture-direction one.
If the parameter is not present in the specific instance than is added as now one.

To execute one action it is possible to use the REST PUT method {context_broker_endpoint}:/config/agent.

```json
{
    "agent_catalog_id": "nprobe",
    "status": "start"
}
```

With this request the nprobe agent is started using the relative action.
