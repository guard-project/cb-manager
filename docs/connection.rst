.. _connection:

Connection
==========

Defines the connection between :ref:`exec-env` and :ref:`network-link`.


Schema
------

+---------------------+--------+----------+----------+--------------+---------------------------------------------+
| Field               | Type   | Required | Readonly | Auto Managed | Example                                     |
+=====================+========+==========+==========+==============+=============================================+
| ``id``              | String | True     | True     | False        | http-db-connection                          |
+---------------------+--------+----------+----------+--------------+---------------------------------------------+
| ``exec_env_id``     | String | True     | True     | False        | mysql-server                                |
+---------------------+--------+----------+----------+--------------+---------------------------------------------+
| ``network_link_id`` | String | True     | True     | False        |eth0                                         |
+---------------------+--------+----------+----------+--------------+---------------------------------------------+
| ``description``     | String | False    | False    | False        | Connection for the |HTTP| and |DB| Servers. |
+---------------------+--------+----------+----------+--------------+---------------------------------------------+

.. warning::

   - It is not possible to update *readonly* fields.
   - it is not possible to set the *auto managed* fields.

.. note::

   - ``id`` is required but it is auto-generated if not provided.
     It is recommended to provide a friendly for simplify the retrieve of connected date in other indices.
   - ``exec_env_id`` should be one of those stored in :ref:`exec-env` index.
   - ``network_link_id`` should be one of those stored in :ref:`network-link` index.


Create
------

To create a new connection use the following |REST| call:

.. http:post:: /connection/(string:id)

    with the request body in |JSON| format:

    .. sourcecode:: http

        POST /connection HTTP/1.1
        Host: cb-manager.example.com
        Content-Type: application/json

        {
            "id": "<connection-id>",
            "exec_env_id": "<exec-env-id>",
            "network_link_id": "<network-link-id>",
            "description": "<human-readable-description>"
        }

    :param id: optional connection id.

    :reqheader Authorization: HTTP Basic Authentication with username and password.
    :reqheader Content-Type: application/json

    :resheader Content-Type: application/json

    :status 201: Connections correctly created.
    :status 204: No content to create connections based on the request.
    :status 400: Request not valid.
    :status 401: Authentication failed.
    :status 406: Request validation failed.
    :status 415: Media type not supported.
    :status 422: Not possible to create ore or more connections based on the request.
    :status 500: Server not available to satisfy the request.

    Replace the data with the correct values, for example <connection-id> with ``http-db-connection``.

    .. note::

        It is possible to add additional data specific for this connection.

    If the creation is correctly executed the response is:

    .. sourcecode:: http

        HTTP/1.1 201 Created
        Content-Type: application/json

        [
            {
                "status": "Created",
                "code": 201,
                "error": false,
                "message": "Connection with id=<connection-id> correctly created"
            }
        ]

    Otherwise, if, for example, a connection with the given ``id`` is already found, this is the response:

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

    If some required data is missing (for example ``exec_env_id``), the response could be:

    .. sourcecode:: http

        HTTP/1.1 406 Not Acceptable
        Content-Type: application/json

        [
            {
                "status": "Not Acceptable",
                "code": 406,
                "error": true,
                "message": {
                    "exec_env_id": "required"
                }
            }
        ]


Read
----

To get the list of connections:

.. http:get:: /connection/(string: id)

    The response includes all the connections created.

    It is possible to filter the results using the following request body:

    .. sourcecode:: http

        GET /connection HTTP/1.1
        Host: cb-manager.example.com
        Content-Type: application/json

        {
            "select": [ "network_link_id" ],
            "where": {
                "equals": {
                    "target:" "id",
                    "expr": "<connection-id>"
                }
            }
        }

    :param id: optional connection id.

    :reqheader Authorization: HTTP Basic Authentication with username and password.
    :reqheader Content-Type: application/json

    :resheader Content-Type: application/json

    :status 200: List of connections filtered by the query in the request body.
    :status 400: Request not valid.
    :status 401: Authentication failed.
    :status 404: Connections based on the request query not found.
    :status 406: Request validation failed.
    :status 415: Media type not supported.
    :status 422: Not possible to get connections with the request query.
    :status 500: Server not available to satisfy the request.

    In this way, it will be returned only the ``network_link_id`` of the connection with ``id`` = "<connection-id>"


Update
------

To update a connection, use:

.. http:put:: /connection/(string:id)

    .. sourcecode:: http

        PUT /connection HTTP/1.1
        Host: cb-manager.example.com
        Content-Type: application/json

        {
            "id": "<connection-id>",
            "description":"<new-description>"
        }

    :param id: optional connection id.

    :reqheader Authorization: HTTP Basic Authentication with username and password.
    :reqheader Content-Type: application/json

    :resheader Content-Type: application/json

    :status 200: All connections correctly updated.
    :status 204: No content to update connections based on the request.
    :status 304: Update for one or more connections not necessary.
    :status 400: Request not valid.
    :status 401: Authentication failed.
    :status 406: Request validation failed.
    :status 415: Media type not supported.
    :status 422: Not possible to update one or more connections based on the request.
    :status 500: Server not available to satisfy the request.

    This example set the new ``description`` for the connection with ``id`` = "<connection-id>".

    .. note::

        Also during the update it is possible to add additional data for the specific connection.

    A possible response is:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json

        [
            {
                "status": "OK",
                "code": 200,
                "error": false,
                "message": "Connection with id=<connection-id> correctly updated"
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
                "message": "Update for connection with id=<connection-id> not necessary"
            }
        ]


Delete
------

To delete connections, use:

.. http:delete:: /connection/(string:id)

    .. sourcecode:: http

        DELETE /connection HTTP/1.1
        Host: cb-manager.example.com
        Content-Type: application/json

        {
            "where": {
                "equals": {
                    "target:" "id",
                    "expr": "<connection-id>"
                }
            }
        }

    :param id: optional connection id.

    :reqheader Authorization: HTTP Basic Authentication with username and password.
    :reqheader Content-Type: application/json

    :resheader Content-Type: application/json

    :status 205: All connections correctly deleted.
    :status 400: Request not valid.
    :status 401: Authentication failed.
    :status 404: Connections based on the request query not found.
    :status 406: Request validation failed.
    :status 415: Media type not supported.
    :status 422: Not possible to delete one or more connections based on the request query.
    :status 500: Server not available to satisfy the request.

    This request removes the connection with ``id`` = <connection-id>".

    This is a possible response:

    .. sourcecode:: http

        HTTP/1.1 205 Reset Content
        Content-Type: application/json

        [
            {
                "status": "Reset Content",
                "code": 200,
                "error": false,
                "message": "Connection with id=<connection-id> correctly deleted"
            }
        ]

    .. caution::

        Without request body, it removes *all* the connections.


.. |DB| replace:: :abbr:`DB (DataBase)`
.. |HTTP| replace:: :abbr:`HTTP (HyperText Transfer Protocol)`
.. |REST| replace:: :abbr:`REST (Representational State Transfer)`
.. |JSON| replace:: :abbr:`JSON (JavaScript Object Notation)`
