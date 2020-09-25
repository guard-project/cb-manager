.. _agent-catalog:

Agent Catalog
=============

Contains the available agents to be installed in the :ref:`exec-env`.


Schema
------

+-----------------+-----------------+----------+----------+--------------+-----------------------------------------------------+
| Field           | Type            | Required | Readonly | Auto Managed | Example                                             |
+=================+=================+==========+==========+==============+=====================================================+
| ``id``          | String          | True     | True     | False        | firewall                                            |
+-----------------+-----------------+----------+----------+--------------+-----------------------------------------------------+
| ``actions``     | List(Action)    | False    | False    | False        |                                                     |
+-----------------+-----------------+----------+----------+--------------+-----------------------------------------------------+
| ``parameters``  | List(Parameter) | False    | False    | False        |                                                     |
+-----------------+-----------------+----------+----------+--------------+-----------------------------------------------------+
| ``resources``   | List(Resource)  | False    | False    | False        |                                                     |
+-----------------+-----------------+----------+----------+--------------+-----------------------------------------------------+
| ``description`` | String          | False    | False    | False        | Monitors and controls incoming and outgoing network |
|                 |                 |          |          |              | traffic based on predetermined security rules.      |
+-----------------+-----------------+----------+----------+--------------+-----------------------------------------------------+


Action Schema
-------------

+-----------------+-----------------------------------------+----------+----------+--------------+-----------------------------------+
| Field           | Type                                    | Required | Readonly | Auto Managed | Example                           |
+=================+=========================================+==========+==========+==============+===================================+
| ``id``          | String                                  | True     | True     | False        | start                             |
+-----------------+-----------------------------------------+----------+----------+--------------+-----------------------------------+
| ``config``      | List(ActionConfig)                      | True     | False    | False        |                                   |
+-----------------+-----------------------------------------+----------+----------+--------------+-----------------------------------+
| ``status``      | Enum(String)[started, stopped, unknown] | False    | False    | False        | started                           |
+-----------------+-----------------------------------------+----------+----------+--------------+-----------------------------------+
| ``description`` | String                                  | False    | False    | False        | Start the execution of the agent. |
+-----------------+-----------------------------------------+----------+----------+--------------+-----------------------------------+


Action Config Schema
--------------------

+------------+--------------+----------+----------+--------------+------------------------+
| Field      | Type         | Required | Readonly | Auto Managed | Example                |
+============+==============+========+==========+================+========================+
| ``cmd``    | String       | True     | False    | False        | service filebeat start |
+------------+--------------+----------+----------+--------------+------------------------+
| ``args``   | List(String) | False    | False    | False        | -v                     |
+------------+--------------+----------+----------+--------------+------------------------+
| ``daemon`` | String       | False    | False    | False        | firewall               |
+------------+--------------+----------+----------+--------------+------------------------+


Parameter Schema
----------------

+-----------------+-------------------+----------+----------+--------------+-------------------+
| Field           | Type              | Required | Readonly | Auto Managed | Example           |
+=================+===================+========+==========+================+===================+
| ``id``          | String            | True     | True     | False        | start             |
+-----------------+-------------------+----------+----------+--------------+-------------------+
| ``type``        | Enum(String) [1]_ | True     | False    | False        | integer           |
+-----------------+-------------------+----------+----------+--------------+-------------------+
| ``config``      | ParameterConfig   | True     | False    | False        |                   |
+-----------------+-------------------+----------+----------+--------------+-------------------+
| ``list``        | Boolean           | False    | False    | False        | False             |
+-----------------+-------------------+----------+----------+--------------+-------------------+
| ``values``      | Enum(String)      | False    | False    | False        | mysql             |
+-----------------+-------------------+----------+----------+--------------+-------------------+
| ``description`` | String            | False    | False    | False        | Enable the agent. |
+-----------------+-------------------+----------+----------+--------------+-------------------+
| ``example``     | String            | False    | False    | False        | 10s               |
+-----------------+-------------------+----------+----------+--------------+-------------------+

.. [1] Possible values are "integer", "number", "time-duration", "string", "choice", "boolean", and "binary".


Parameter Config Schema
-----------------------

+------------+-------------------------------------------+----------+----------+--------------+----------------------------------+
| Field      | Type                                      | Required | Readonly | Auto Managed | Example                          |
+============+===========================================+========+==========+================+==================================+
| ``schema`` | Enum(String)["yaml", "json", "propeties"] | True     | False    | False        | yaml                             |
+------------+-------------------------------------------+----------+----------+--------------+----------------------------------+
| ``source`` | String                                    | False    | False    | False        | /usr/share/filebeat/filebeat.yml |
+------------+-------------------------------------------+----------+----------+--------------+----------------------------------+
| ``path``   | Lis(String)                               | False    | False    | False        | enabled                          |
+------------+-------------------------------------------+----------+----------+--------------+----------------------------------+


Resource Schema
---------------

+-----------------+----------------+----------+----------+--------------+---------------------+
| Field           | Type           | Required | Readonly | Auto Managed | Example             |
+=================+================+========+==========+================+=====================+
| ``id``          | String         | True     | True     | False        | filebeat-config     |
+-----------------+----------------+----------+----------+--------------+---------------------+
| ``config``      | ResourceConfig | True     | False    | False        |                     |
+-----------------+----------------+----------+----------+--------------+---------------------+
| ``description`` | String         | False    | False    | False        | Configuration file. |
+-----------------+----------------+----------+----------+--------------+---------------------+
| ``example``     | String         | False    | False    | False        |                     |
+-----------------+----------------+----------+----------+--------------+---------------------+


Resource Config Schema
----------------------

+----------+-------------+----------+----------+--------------+-----------------------------------+
| Field    | Type        | Required | Readonly | Auto Managed | Example                           |
+==========+=============+==========+==========+==============+===================================+
| ``path`` | Lis(String) | False    | False    | False        | /usr/share/filebeat/filebeat.yml  |
+----------+-------------+----------+----------+--------------+-----------------------------------+

.. warning::

    - It is not possible to update *readonly* fields.
    - it is not possible to set the *Auto managed* fields.

.. note::

    - ``id`` is required but it is auto-generated if not provided.
      It is recommended to provide a friendly for simplify the retrieve of connected date in other indices.


Create
------

To create a new agent in the catalog use the following |REST| call:

.. http:post:: /catalog/agent/(string:id)


    with the request body in |JSON| format:

    .. sourcecode:: http

        POST /catalog/agent HTTP/1.1
        Host: cb-manager.example.com
        Content-Type: application/json

        {
            "id": "<agent-id>",
            "actions": [
                {
                    "id": "<action-id>",
                    "status": "<action-status>",
                    "config": {
                        "cmd": "<action-cmd>"
                    },
                    "description": "<action-human-readable-description>",
                    "example": "<action-example>"
                }
            ],
            "parameters": [
                {
                    "id": "<parameter-id>",
                    "type": "<parameter-type>",
                    "config": {
                        "schema": "<parameter-schema>",
                        "source": "<parameter-source>",
                        "path": [
                            "<parameter-path>"
                        ]
                    },
                    "description": "<parameter-human-readable-description>",
                    "example": "<parameter-example>",
                }
            ],
            "resources": [
                {
                    "id": "<resource-id>",
                    "config": {
                        "path": "<resource-path>"
                    },
                    "description": "<resource-human-readable-description>",
                    "example": "<resource-example>",
                }
            ]
        }

    :param id: optional agent id.

    :reqheader Authorization: HTTP Basic Authentication with username and password.
    :reqheader Content-Type: application/json

    :resheader Content-Type: application/json

    :status 201: Agents correctly created.
    :status 204: No content to create agents for the catalog based on the request.
    :status 400: Request not valid.
    :status 401: Authentication failed.
    :status 406: Request validation failed.
    :status 415: Media type not supported.
    :status 422: Not possible to create ore or more agents for the catalog based on the request.
    :status 500: Server not available to satisfy the request.

    Replace the data with the correct values, for example <agent-id> with ``nprobe``.

    .. note:

        It is possible to add additional data specific for this agent.

    If the creation is correctly executed the response is:

    .. sourcecode:: http

        HTTP/1.1 201 Created
        Content-Type: application/json

        [
            {
                "status": "Created",
                "code": 201,
                "error": false,
                "message": "Agent catalog with id=<agent-id> correctly created"
            }
        ]

    Otherwise, if, for example, an agent with the given ``id`` is already found in the catalog, this is the response:

    .. sourcecode:: http

        HTTP/1.1 406 Not Acceptable
        Content-Type: application/json

        [
            {
                "status": "Not Acceptable",
                "code": 406,
                "error": true,
                "message": "Id already found"
            }
        ]

    If some required data is missing (for example ``type`` of one ``parameter``), the response could be:

    .. sourcecode:: http

        HTTP/1.1 406 Not Acceptable
        Content-Type: application/json

        [
            {
                "status": "Not Acceptable",
                "code": 406,
                "error": true,
                "message": {
                    "parameter.type": "required"
                }
            }
        ]

Read
----

To get the list of the agents available in the catalog:

.. http:get:: /catalog/agent/(string: id)

    The response includes all the agents.

    It is possible to filter the results using the following request body:

    .. sourcecode:: http

        GET /catalog/agent HTTP/1.1
        Host: cb-manager.example.com
        Content-Type: application/json

        {
            "select": [ "parameters" ],
            "where": {
                "equals": {
                    "target:" "id",
                    "expr": "<agent-id>"
                }
            }
        }

    :param id: optional agent id from the catalog.

    :reqheader Authorization: HTTP Basic Authentication with username and password.
    :reqheader Content-Type: application/json

    :resheader Content-Type: application/json

    :status 200: List of agents from the catalog filtered by the query in the request body.
    :status 400: Request not valid.
    :status 401: Authentication failed.
    :status 404: Data based on the request query not found.
    :status 406: Request validation failed.
    :status 415: Media type not supported.
    :status 422: Not possible to get agents from the catalog with the request query.
    :status 500: Server not available to satisfy the request.

    In this way, it will be returned only the ``parameters`` of the agent in the catalog with ``id`` = "<agent-id>".


Update
------

To update an agent in the catalog, use:

.. http:put:: /catalog/agent/(string:id)

    .. sourcecode:: http

        PUT /catalog/agent HTTP/1.1
        Host: cb-manager.example.com
        Content-Type: application/json

        {
            "id": "<agent-id>",
            "parameters": [
                {
                    "id": "<parameter-id>",
                    "type": "<new-parameter-type>"
                }
            ],
            "actions": [
                {
                    "id": "<new-action-id>",
                    "config": {
                        "cmd": "<new-action-cmd>"
                    }
                }
            ]
        }

    :param id: optional agent id.

    :reqheader Authorization: HTTP Basic Authentication with username and password.
    :reqheader Content-Type: application/json

    :resheader Content-Type: application/json

    :status 200: All agents in the catalog correctly updated.
    :status 204: No content to update agents in the catalog based on the request.
    :status 304: Update for one or more agents in the catalog not necessary.
    :status 400: Request not valid.
    :status 401: Authentication failed.
    :status 406: Request validation failed.
    :status 415: Media type not supported.
    :status 422: Not possible to update one or more agents in the catalog based on the request.
    :status 500: Server not available to satisfy the request.

    This example

    1. updates the new ``type`` of the ``parameter`` with ``id`` = "<parameter-id>";
    2. adds a new action

    of the agent with ``id`` = "<agent-id>".

    .. note:

        Also during the update it is possible to add additional data (not related to actions or parameters) for the specific agent.

    A possible response is:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json

        [
            {
                "status": "OK",
                "code": 200,
                "error": false,
                "message": "Agent catalog with id=<agent-id> correctly updated"
            }
        ]

    Instead, if the are not changes the response is:

    .. sourcecode:: http

        HTTP/1.1 304 Not Modified
        Content-Type: application/json

        [
            {
                "status": "Not Modified",
                "code": 304,
                "error": false,
                "message": "Update for agent catalog with id=<agent-id> not necessary"
            }
        ]


Delete
------

To delete agents from the catalog, use:

.. http:delete:: /catalog/agent/(string:id)

    .. sourcecode:: http

        DELETE /catalog/agent HTTP/1.1
        Host: cb-manager.example.com
        Content-Type: application/json

        {
            "where": {
                "equals": {
                    "target:" "id",
                    "expr": "<agent-id>"
                }
            }
        }

    :param id: optional agent id from the catalog.

    :reqheader Authorization: HTTP Basic Authentication with username and password.
    :reqheader Content-Type: application/json

    :resheader Content-Type: application/json

    :status 205: All agents correctly deleted from the catalog.
    :status 400: Request not valid.
    :status 401: Authentication failed.
    :status 404: Agents based on the request query not found in the catalog.
    :status 406: Request validation failed.
    :status 415: Media type not supported.
    :status 422: Not possible to delete one or more agents from the catalog based on the request query.
    :status 500: Server not available to satisfy the request.

    This request removes from the catalog the agent with ``id`` = "<agent-id>".

    This is a possible response:

    .. sourcecode:: http

        HTTP/1.1 205 Reset Content
        Content-Type: application/json

        [
            {
                "status": "Reset Content",
                "code": 200,
                "error": false,
                "message": "Agent catalog the id=<agent-id> correctly deleted"
            }
        ]

    .. caution::

        Without request body, it removes **all** the agents from the catalog.

Loaded data
-----------

This data is already available:

.. http:get:: /catalog/agent

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json

        [
            {
                "id": "firewall",
                "actions": [
                    {
                        "id": "start",
                        "status": "started",
                        "config": { "cmd": "polycubectl firewall add fw" }
                    },
                    {
                        "id": "stop",
                        "status": "stopped",
                        "config": { "cmd": "polycubectl fw del" }
                    },
                    {
                        "id": "attach",
                        "config": { "cmd": "polycubectl attach fw {port}" }
                    },
                    {
                        "id": "insert",
                        "config": { "cmd": "polycubectl firewall fw chain {chain} insert id={n} src={src} dst={dst} action={action}" }
                    },
                    {
                        "id": "append",
                        "config": { "cmd": "polycubectl firewall fw chain {chain} append src={src} dst={dst} action={action}" }
                    },
                    {
                        "id": "prepend",
                        "config": { "cmd": "polycubectl firewall fw chain {chain} insert src={src} dst={dst} action={action}" }
                    },
                    {
                        "id": "delete",
                        "config": { "cmd": "polycubectl firewall fw chain {chain} rule del {n}" }
                    },
                    {
                        "id": "default",
                        "config": { "cmd": "polycubectl firewall fw chain {chain} set default={action}" }
                    },
                    {
                        "id": "list",
                        "config": { "cmd": "polycubectl firewall fw chain {chain} rule show" }
                    },
                    {
                        "id": "stats",
                        "config": { "cmd": "polycubectl firewall fw chain {chain} stats show" }
                    }
                ]
            },
            [
                {
                    "id": "nprobe",
                    "parameters": [
                        {
                            "id": "network-interface",
                            "type": "string",
                            "example": "eth0",
                            "description": "Set the network interface to probe",
                            "config": {
                                "schema": "properties",
                                "source": "/etc/nprobe/nprobe.conf",
                                "path": [
                                    "-i"
                                ]
                            }
                        },
                        {
                            "id": "capture-direction",
                            "type": "integer",
                            "example": 1,
                            "description": "Specify packet capture direction: 0=RX+TX (default), 1=RX only, 2=TX only",
                            "config": {
                                "schema": "properties",
                                "source": "/etc/nprobe/nprobe.conf",
                                "path": [
                                    "-capture-direction"
                                ]
                            }
                        },
                        {
                            "id": "flow-template",
                            "type": "string",
                            "example": "%IPV4_SRC_ADDR %IPV4_DST_ADDR %IPV4_NEXT_HOP %INPUT_SNMP %OUTPUT_SNMP %IN_PKTS %IN_BYTES %FIRST_SWITCHED %LAST_SWITCHED %L4_SRC_PORT %L4_DST_PORT %TCP_FLAGS %PROTOCOL %SRC_TOS %SRC_AS %DST_AS %IPV4_SRC_MASK %IPV4_DST_MASK",
                            "description": "Specifies the NFv9 template",
                            "config": {
                                "schema": "properties",
                                "source": "/etc/nprobe/nprobe.conf",
                                "path": [
                                    "-T"
                                ]
                            }
                        }
                    ],
                    "actions": [
                        {
                            "id": "start",
                            "status": "started",
                            "config": {
                                "cmd": "sudo systemctl start nprobe"
                            }
                        },
                        {
                            "id": "stop",
                            "status": "stopped",
                            "config": {
                                "cmd": "sudo systemctl stop nprobe"
                            }
                        },
                        {
                            "id": "restart",
                            "status": "started",
                            "config": {
                                "cmd": "sudo systemctl restart nprobe"
                            }
                        }
                    ]
                }
            ]
        ]


.. |JSON| replace:: :abbr:`JSON (JavaScript Object Notation)`
.. |REST| replace:: :abbr:`REST (Representational State Transfer)`
