.. _agent-instance:

Agent Instance
==============

Contains the :ref:`agent-catalog` instances installed in the :ref:`exec-env`.


Schema
------

+----------------------+-----------------------------------------+----------+----------+--------------+------------------------------+
| Field                | Type                                    | Required | Readonly | Auto Managed | Example                      |
+======================+=========================================+==========+==========+==============+==============================+
| ``id``               | String                                  | True     | True     | False        | firewall@mysql-server        |
+----------------------+-----------------------------------------+----------+----------+--------------+------------------------------+
| ``agent_catalog_id`` | String                                  | True     | True     | False        | firewall                     |
+----------------------+-----------------------------------------+----------+----------+--------------+------------------------------+
| ``exec_env_id``      | String                                  | True     | True     | False        | mysql-server                 |
+----------------------+-----------------------------------------+----------+----------+--------------+------------------------------+
| ``status``           | Enum(String){started, stopped, unknown} | True     | True     | False        | started                      |
+----------------------+-----------------------------------------+----------+----------+--------------+------------------------------+
| ``operations``       | List(Operation)                         | False    | True     | False        |                              |
+----------------------+-----------------------------------------+----------+----------+--------------+------------------------------+
| ``description``      | String                                  | False    | False    | False        | Collect system metrics       |
|                      |                                         |          |          |              | from execution environments. |
+----------------------+-----------------------------------------+----------+----------+--------------+------------------------------+


Operation Schema
----------------

+----------------+-----------------+----------+----------+--------------+---------+
| Field          | Type            | Required | Readonly | Auto Managed | Example |
+================+=================+==========+==========+==============+=========+
| ``actions``    | List(Action)    | False    | False    | False        |         |
+----------------+-----------------+----------+----------+--------------+---------+
| ``parameters`` | List(Parameter) | False    | False    | False        |         |
+----------------+-----------------+----------+----------+--------------+---------+
| ``resources``  | List(Resource)  | False    | False    | False        |         |
+----------------+-----------------+----------+----------+--------------+---------+


Action Schema
-------------

+---------------+----------+----------+----------+--------------+---------------------------+
| Field         | Type     | Required | Readonly | Auto Managed | Example                   |
+===============+==========+==========+==========+==============+===========================+
| ``id``        | String   | True     | True     | False        | period                    |
+---------------+----------+----------+----------+--------------+---------------------------+
| ``data``      | Raw      | False    | True     | True         | { action: forward, n: 0 } |
+---------------+----------+----------+----------+--------------+---------------------------+
| ``timestamp`` | DateTime | False    | True     | True         | 2020-11-07T23:04:21       |
+---------------+----------+----------+----------+--------------+---------------------------+


Parameter Schema
----------------

+---------------+----------+----------+----------+--------------+---------------------+
| Field         | Type     | Required | Readonly | Auto Managed | Example             |
+===============+==========+==========+==========+==============+=====================+
| ``id``        | String   | True     | True     | False        | period              |
+---------------+----------+----------+----------+--------------+---------------------+
| ``value``     | String   | True     | False    | False        | 10s                 |
+---------------+----------+----------+----------+--------------+---------------------+
| ``timestamp`` | DateTime | False    | True     | True         | 2020-11-07T23:04:21 |
+---------------+----------+----------+----------+--------------+---------------------+


Resource Schema
---------------

+---------------+----------+----------+----------+--------------+---------------------+
| Field         | Type     | Required | Readonly | Auto Managed | Example             |
+===============+==========+==========+==========+==============+=====================+
| ``id``        | String   | True     | True     | False        | period              |
+---------------+----------+----------+----------+--------------+---------------------+
| ``content``   | String   | True     | False    | False        | period: 10s         |
+---------------+----------+----------+----------+--------------+---------------------+
| ``timestamp`` | DateTime | False    | True     | True         | 2020-11-07T23:04:21 |
+---------------+----------+----------+----------+--------------+---------------------+


.. warning::

    - It is not possible to update *readonly* fields.
    - it is not possible to set the *Auto managed* fields.

.. note::

    - ``id`` is required but it is auto-generated if not provided.
      It is recommended to provide a friendly for simplify the retrieve of connected date in other indices.
      A common syntax is to use ``agent_catalog_id`` and ``exec_env_id`` concatenated with = '@'.
    - ``agent_catalog_id`` should be one of those stored in :ref:`agent-catalog` index.
    - ``exec_env_id`` should be one of those stored in :ref:`exec-env` index.


Create
------

To create a new agent instance use the following |REST| call:

.. http:post:: /instance/agent/(string:id)

    with the request body in |JSON| format:

    .. sourcecode:: http

        POST /instance/agent HTTP/1.1
        Host: cb-manager.example.com
        Content-Type: application/json

        {
            "id": "<agent-instance-id>",
            "agent_catalog_id": "<agent-id>",
            "exec_env_id": "<exec-env-id>",
            "operations": [
                "parameters": [
                    {
                        "id": "<parameter-id>",
                        "value": "<parameter-value>",
                    }
                ],
                "actions": [
                    {
                        "id": "<action-id>",
                        "mode": "<action-mode-value>"
                    }
                ]
            ]
        }

    :param id: optional agent instance id.

    :reqheader Authorization: HTTP Basic Authentication with username and password.
    :reqheader Content-Type: application/json

    :resheader Content-Type: application/json

    :status 201: Agent instances correctly created.
    :status 204: No content to create agent instances based on the request.
    :status 400: Request not valid.
    :status 401: Authentication failed.
    :status 406: Request validation failed.
    :status 415: Media type not supported.
    :status 422: Not possible to create ore or more agent instances based on the request.
    :status 500: Server not available to satisfy the request.

    Replace the data with the correct values, for example <agent-instance-id> with "firewall@mysql-server".

     .. note:

        It is possible to add additional data specific for this agent.

        The ``actions`` fields is used to perform the actions defined in the catalog referenced by the ``id``.

        Any other fields (like, in the above example, ``mode`` are used in the ``cmd`` field of
        the action defined in the :ref:`agent-catalog`.

        For example, if ``cmd`` is "firewall set {mode}" then it will be formatted using the values of the other fields.

        If the action has a field ``status`` in the catalog, this field is used to update the status of the agent instance
        if the execution finished correctly. Otherwise, if there are some error during the execution,
        the ``status`` will be set to "unknown".

    If the creation is correctly executed the response is:

    .. sourcecode:: http

        HTTP/1.1 201 Created
        Content-Type: application/json

        [
            {
                "status": "Created",
                "code": 201,
                "error": false,
                "message": "Agent instance with id=<agent-instance-id> correctly created"
            }
        ]

    Otherwise, if, for example, an agent instance with the given ``id`` is already found, this is the response:

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

    If some required data is missing (for example ``status``), the response could be:

    .. sourcecode:: http

        HTTP/1.1 406 Not Acceptable
        Content-Type: application/json

        [
            {
                "status": "Not Acceptable",
                "code": 406,
                "error": true,
                "message": {
                    "status": "required"
                }
            }
        ]


Read
----

To get the list of the agent instances:

.. http:get:: /instance/agent/(string: id)

    The response includes all the agent instances.

    It is possible to filter the results using the following request body:

    .. sourcecode:: http

        GET /instance/agent HTTP/1.1
        Host: cb-manager.example.com
        Content-Type: application/json

        {
            "select": [ "parameters" ],
            "where": {
                "equals": {
                    "target:" "id",
                    "expr": "<agent-instance-id>"
                }
            }
        }

    In this way, it will be returned only the ``parameters`` of the agent instance with ``id`` = "<agent-instance-id>".


Update
------

To update an agent instance, use:

.. http:put:: /instance/agent/(string:id)

    .. sourcecode:: http

        PUT /instance/agent HTTP/1.1
        Host: cb-manager.example.com
        Content-Type: application/json

        {
            "id": "<agent-instance-id}",
            "operations": [
                "parameters": [
                    {
                        "id": "<parameter-id>",
                        "value": "<new-parameter-value>"
                    }
                ],
                "actions": [
                    {
                        "id": "<action-id>",
                        "mode": "<new-action-mode-value>"
                    }
                ]
            ]
        }

    :param id: optional agent instance id.

    :reqheader Authorization: HTTP Basic Authentication with username and password.
    :reqheader Content-Type: application/json

    :resheader Content-Type: application/json

    :status 200: All agent instances correctly updated.
    :status 204: No content to update agent instances based on the request.
    :status 304: Update for one or more agent instances not necessary.
    :status 400: Request not valid.
    :status 401: Authentication failed.
    :status 406: Request validation failed.
    :status 415: Media type not supported.
    :status 422: Not possible to update one or more agent instances based on the request.
    :status 500: Server not available to satisfy the request.

    This example

    1. updates the ``value`` of the ``parameter`` with ``id`` = "<parameter-id>";
    2. execute a new action with  with ``id`` = "<action-id>"

    of the agent instance with ``id`` = "<agent-instance-id>".

    .. note:

        Also during the update it is possible to add additional data (not related to actions or parameters) for the specific agent instances.

    A possible response is:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json

        [
            {
                "status": "OK",
                "code": 200,
                "error": false,
                "message": "Agent instance with id=<agent-instance-id> correctly updated"
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
                "message": "Update for agent instance with id=<agent-instance-id> not necessary"
            }
        ]

Delete
------

To delete agent instances, use:

.. http:delete:: /instance/agent/(string:id)

    .. sourcecode:: http

        DELETE /instance/agent HTTP/1.1
        Host: cb-manager.example.com
        Content-Type: application/json

        {
            "where": {
                "equals": {
                    "target:" "id",
                    "expr": "<agent-instance-id>"
                }
            }
        }

    :param id: optional agent instance id.

    :reqheader Authorization: HTTP Basic Authentication with username and password.
    :reqheader Content-Type: application/json

    :resheader Content-Type: application/json

    :status 205: All agent instances correctly deleted.
    :status 400: Request not valid.
    :status 401: Authentication failed.
    :status 404: Agent instances based on the request query not found.
    :status 406: Request validation failed.
    :status 415: Media type not supported.
    :status 422: Not possible to delete one or more agent instances based on the request query.
    :status 500: Server not available to satisfy the request.

    This request removes the agent instance with ``id`` = "<agent-instance-id>".

    This is a possible response:

    .. sourcecode:: http

        HTTP/1.1 205 Reset Content
        Content-Type: application/json

        [
            {
                "status": "Reset Content",
                "code": 200,
                "error": false,
                "message": "Agent instance the id=<agent-instance-id> correctly deleted"
            }
        ]

    .. caution::

        Without request body, it removes **all** the agent instances.


.. |JSON| replace:: :abbr:`JSON (JavaScript Object Notation)`
.. |REST| replace:: :abbr:`REST (Representational State Transfer)`
