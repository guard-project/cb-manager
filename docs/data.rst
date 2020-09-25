.. _data:

Data
====

This index stores all the incoming data from the :ref:`exec-env` collected by the :ref:`agent-instance` or
:ref:`ebpf-program-instance` installed on them.

Schema
------

+------------------------------+--------+----------+----------+--------------+----------------------------+
| Field                        | Type   | Required | Readonly | Auto Managed | Example                    |
+=================+============+========+==========+==========+==============+============================+
| ``id``                       | String | True     | True     | False        | dsalkasdioi232382yieyqwuiy |
+------------------------------+--------+----------+----------+--------------+----------------------------+
| ``agent_instance_id``        | String | False    | True     | False        | filebeat@mysql-server      |
+------------------------------+--------+----------+----------+--------------+----------------------------+
| ``ebpf_program_instance_id`` | String | False    | True     | False        | synflood@mysql-server      |
+------------------------------+--------+----------+----------+--------------+----------------------------+
| ``timestamp_event``          | Date   | False    | True     | False        | 2020/06/04 09:22:09        |
+------------------------------+--------+----------+----------+--------------+----------------------------+
| ``timestamp_agent``          | Date   | False    | True     | False        | 2020/06/04 09:22:19        |
+------------------------------+--------+----------+----------+--------------+----------------------------+

.. warning::

    - It is not possible to update *readonly* fields.
    - it is not possible to set the *Auto managed* fields.

.. note::

    - ``id`` is required but it is auto-generated if not provided.
      It is recommended to provide a friendly for simplify the retrieve of connected date in other indices.
    - ``agent_instance_id`` should be one of those stored in :ref:`agent-instance` index.
    - ``ebpf_program_instance_id`` should be one of those stored in :ref:`ebpf-program-instance` index.


Create
------

To create a new data use the following |REST| call:

.. http:post:: /data/(string:id)

    with the request body in |JSON| format:

    .. sourcecode:: http

        POST /data HTTP/1.1
        Host: cb-manager.example.com
        Content-Type: application/json

        {
            "id": "<data-id>",
            "agent_instance_id": "<agent-instance-id>",
            "timestamp_event": "<timestamp-event>",
            "timestamp_agent": "<timestamp-agent>",
        }

    :param id: optional data id.

    :reqheader Authorization: HTTP Basic Authentication with username and password.
    :reqheader Content-Type: application/json

    :resheader Content-Type: application/json

    :status 201: Data correctly created.
    :status 204: No content to create data based on the request.
    :status 400: Request not valid.
    :status 401: Authentication failed.
    :status 406: Request validation failed.
    :status 415: Media type not supported.
    :status 422: Not possible to create ore or more data based on the request.
    :status 500: Server not available to satisfy the request.

    Replace the data with the correct values, for example <agent-instance-id> with ``filebeat@mysql-server``.

    .. note::

        It is possible to add additional data.

    If the creation is correctly executed the response is:

    .. sourcecode:: http

        HTTP/1.1 201 Created
        Content-Type: application/json

        [
            {
                "status": "Created",
                "code": 201,
                "error": false,
                "message": "Data with id=<data-id> correctly created"
            }
        ]

    Otherwise, if, for example, a data with the given ``id`` is already found, this is the response:

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


Read
----

To get the list of data:

.. http:get:: /data/(string: id)

    The response includes all the data created.

    It is possible to filter the results using the following request body:

    .. sourcecode:: http

        GET /data HTTP/1.1
        Host: cb-manager.example.com
        Content-Type: application/json

        {
            "select": [ "type_id" ],
            "where": {
                "equals": {
                    "target:" "id",
                    "expr": "<data-id>"
                }
            }
        }

    :param id: optional data id.

    :reqheader Authorization: HTTP Basic Authentication with username and password.
    :reqheader Content-Type: application/json

    :resheader Content-Type: application/json

    :status 200: List of data filtered by the query in the request body.
    :status 400: Request not valid.
    :status 401: Authentication failed.
    :status 404: Data based on the request query not found.
    :status 406: Request validation failed.
    :status 415: Media type not supported.
    :status 422: Not possible to get data with the request query.
    :status 500: Server not available to satisfy the request.

    In this way, it will be returned only the ``type_id`` of the data with ``id`` = "<data-id>".


Update
------

To update a data, use:

.. http:put:: /data/(string:id)

    .. sourcecode:: http

        PUT /data HTTP/1.1
        Host: cb-manager.example.com
        Content-Type: application/json

        {
            "id": "<data-id>",
            "source": "<ip-address>",
        }

    :param id: optional data id.

    :reqheader Authorization: HTTP Basic Authentication with username and password.
    :reqheader Content-Type: application/json

    :resheader Content-Type: application/json

    :status 200: All data correctly updated.
    :status 204: No content to update data based on the request.
    :status 304: Update for one or more data not necessary.
    :status 400: Request not valid.
    :status 401: Authentication failed.
    :status 406: Request validation failed.
    :status 415: Media type not supported.
    :status 422: Not possible to update one or more data based on the request.
    :status 500: Server not available to satisfy the request.

    This example add a new field ``source`` for the data with ``id`` = "<data-id>".

    A possible response is:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json

        [
            {
                "status": "OK",
                "code": 200,
                "error": false,
                "message": "Data with id=<data-id> correctly updated"
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
                "message": "Update for data with id=<data-id> not necessary"
            }
        ]


Delete
------

To delete data, use:

.. http:delete:: /data/(string:id)

    .. sourcecode:: http

        DELETE /data HTTP/1.1
        Host: cb-manager.example.com
        Content-Type: application/json

        {
            "where": {
                "equals": {
                    "target:" "id",
                    "expr": "<data-id>"
                }
            }
        }

    :param id: optional data id.

    :reqheader Authorization: HTTP Basic Authentication with username and password.
    :reqheader Content-Type: application/json

    :resheader Content-Type: application/json

    :status 205: All data correctly deleted.
    :status 400: Request not valid.
    :status 401: Authentication failed.
    :status 404: Data based on the request query not found.
    :status 406: Request validation failed.
    :status 415: Media type not supported.
    :status 422: Not possible to delete one or more data based on the request query.
    :status 500: Server not available to satisfy the request.

    This request removes the data with ``id`` = "<data-id>".

    This is a possible response:

    .. sourcecode:: http

        HTTP/1.1 205 Reset Content
        Content-Type: application/json

        [
            {
                "status": "Reset Content",
                "code": 200,
                "error": false,
                "message": "Data with id=<data-id> correctly deleted"
            }
        ]

    .. caution::

        Without request body, it removes **all** the data.


.. |JSON| replace:: :abbr:`JSON (JavaScript Object Notation)`
.. |REST| replace:: :abbr:`REST (Representational State Transfer)`
