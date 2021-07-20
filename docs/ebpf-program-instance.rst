.. _ebpf-program-instance:

eBPF Program Instance
=====================

Contains the :ref:`ebpf-program-catalog` instances installed in the :ref:`exec-env`.

Schema
------

+-----------------------------+--------+----------+----------+--------------+-------------------------------------------------------+
| Field                       | Type   | Required | Readonly | Auto Managed | Example                                               |
+=============================+========+==========+==========+==============+=======================================================+
| ``id``                      | String | True     | True     | False        | packet-counter@mysql-server                           |
+-----------------------------+--------+----------+----------+--------------+-------------------------------------------------------+
| ``ebpf_program_catalog_id`` | String | True     | False    | False        | packet-counter                                        |
+-----------------------------+--------+----------+----------+--------------+-------------------------------------------------------+
| ``exec_env_id``             | String | True     | True     | False        | mysql-server                                          |
+-----------------------------+--------+----------+----------+--------------+-------------------------------------------------------+
| ``description``             | String | False    | False    | False        | Collect system metrics from Apache |HTTP| Web Server. |
+-----------------------------+--------+----------+----------+--------------+-------------------------------------------------------+

.. warning::

    - It is not possible to update *readonly* fields.
    - it is not possible to set the *Auto managed* fields.

.. note::

    - ``id`` is required but it is auto-generated if not provided.
       It is recommended to provide a friendly for simplify the retrieve of connected date in other indices.
       A common syntax is to use ``ebpf_program_catalog_id`` and ``exec_env_id`` concatenated with = '@'.
    - ``ebpf_program_catalog_id`` should be one of those stored in :ref:`ebpf-program-catalog` index.
    - ``exec_env_id`` should be one of those stored in :ref:`exec-env` index.


Create
------

To create a new |eBPF| program instance use the following |REST| call:

.. http:post:: /instance/ebpfprogrem/(string:id)

    with the request body in |JSON| format:

    .. sourcecode:: http

        POST /instance/ebpf-program HTTP/1.1
        Host: cb-manager.example.com
        Content-Type: application/json

        {
            "id": "<ebpf-program-instance-id>",
            "ebpf_program_catalog_id": "<ebpf-program-id>",
            "exec_env_id": "<exec-env-id>"
        }

    :param id: optional |eBPF| program instance id.

    :reqheader Authorization: JWT Authentication.
    :reqheader Content-Type: application/json

    :resheader Content-Type: application/json

    :status 201: |eBPF| program instances correctly created.
    :status 204: No content to create |eBPF| program instances based on the request.
    :status 400: Request not valid.
    :status 401: Authentication failed.
    :status 406: Request validation failed.
    :status 415: Media type not supported.
    :status 422: Not possible to create ore or more |eBPF| program instances based on the request.
    :status 500: Server not available to satisfy the request.

    Replace the data with the correct values, for example <ebpf-program-instance-id> with "packet-counter@mysql-server".

    .. note:

        It is possible to add additional data specific for this |eBPF| program.

    If the creation is correctly executed the response is:

    .. sourcecode:: http

        HTTP/1.1 201 Created
        Content-Type: application/json

        [
            {
                "status": "Created",
                "code": 201,
                "error": false,
                "message": "eBPF program instance with id=<ebpf-program-instance-id> correctly created"
            }
        ]

    Otherwise, if, for example, an |eBPF| program instance with the given ``id`` is already found, this is the response:

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

To get the list of the |eBPF| program instances:

.. http:get:: /instance/ebpf-program/(string: id)

    The response includes all the |eBPF| program instances.

    It is possible to filter the results using the following request body:

    .. sourcecode:: http

        GET /instance/ebpf-program HTTP/1.1
        Host: cb-manager.example.com
        Content-Type: application/json

        {
            "select": [ "exec_env_id" ],
            "where": {
                "equals": {
                    "target:" "id",
                    "expr": "<ebpf-program-instance-id>"
                }
            }
        }

    In this way, it will be returned only the ``exec_env_id`` of the |eBPF|
    program instance with ``id`` = "<ebpf-program-instance-id>".


Update
------

To update an |eBPF| program instance, use:

.. http:put:: /instance/ebpf-program/(string:id)

    .. sourcecode:: http

        PUT /instance/ebpf-program HTTP/1.1
        Host: cb-manager.example.com
        Content-Type: application/json

        {
            "id": "<epbf-program-instance-id>",
            "description": "<human-readable-description>"
        }

    :param id: optional |eBPF| program instance id.

    :reqheader Authorization: JWT Authentication.
    :reqheader Content-Type: application/json

    :resheader Content-Type: application/json

    :status 200: All |eBPF| program instances correctly updated.
    :status 204: No content to update |eBPF| program instances based on the request.
    :status 304: Update for one or more |eBPF| program instances not necessary.
    :status 400: Request not valid.
    :status 401: Authentication failed.
    :status 406: Request validation failed.
    :status 415: Media type not supported.
    :status 422: Not possible to update one or more |eBPF| program instances based on the request.
    :status 500: Server not available to satisfy the request.

    This example set the ``description`` to "<human-readable-description>" of the |eBPF|
    program instance with ``id`` = "<ebpf-program-instance-id>".

    .. note:

        Also during the update it is possible to add additional data (not related to actions or parameters)
        for the specific |eBPF| program instances.

    A possible response is:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json

        [
            {
                "status": "OK",
                "code": 200,
                "error": false,
                "message": "eBPF program instance with id=<ebpf-program-instance-id> correctly updated"
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
                "message": "Update for eBPF program instance with id=<ebpf-program-instance-id> not necessary"
            }
        ]


Delete
------

To delete |eBPF| program instances, use:

.. http:delete:: /instance/ebpf-program/(string:id)

    .. sourcecode:: http

        DELETE /instance/ebpf-program HTTP/1.1
        Host: cb-manager.example.com
        Content-Type: application/json

        {
            "where": {
                "equals": {
                    "target:" "id",
                    "expr": "<ebpf-program-instance-id>"
                }
            }
        }

    :param id: optional |eBPF| program instance id.

    :reqheader Authorization: JWT Authentication.
    :reqheader Content-Type: application/json

    :resheader Content-Type: application/json

    :status 205: All |eBPF| program instances correctly deleted.
    :status 400: Request not valid.
    :status 401: Authentication failed.
    :status 404: |eBPF| program instances based on the request query not found.
    :status 406: Request validation failed.
    :status 415: Media type not supported.
    :status 422: Not possible to delete one or more |eBPF| program instances based on the request query.
    :status 500: Server not available to satisfy the request.

    This request removes the |eBPF| program instance with ``id`` = "<ebpf-program-instance-id>".

    This is a possible response:

    .. sourcecode:: http

        HTTP/1.1 205 Reset Content
        Content-Type: application/json

        [
            {
                "status": "Reset Content",
                "code": 200,
                "error": false,
                "message": "eBPF program instance the id=<ebpf-program-instance-id> correctly deleted"
            }
        ]

    .. caution::

        Without request body, it removes **all** the |eBPF| program instances.


.. |eBPF| replace:: :abbr:`eBPF (extended Berkeley Packet Filter)`
.. |HTTP| replace:: :abbr:`HTTP (HyperText Transfer Procotocol)`
.. |JSON| replace:: :abbr:`JSON (JavaScript Object Notation)`
.. |REST| replace:: :abbr:`REST (Representational State Transfer)`
