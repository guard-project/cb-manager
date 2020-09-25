.. _ebpf-program-catalog:

eBPF Program Catalog
====================

Contains the available |eBPF| programs to be installed in the :ref:`exec-env`.

Schema
------

+-----------------+-----------------+----------+----------+--------------+----------------------------------------------------------------------+
| Field           | Type            | Required | Readonly | Auto Managed | Example                                                              |
+=================+=================+==========+==========+==============+======================================================================+
| ``id``          | String          | True     | True     | False        | packet-counter                                                       |
+-----------------+-----------------+----------+----------+--------------+----------------------------------------------------------------------+
| ``config``      | Config          | True     | False    | False        |                                                                      |
+-----------------+-----------------+----------+----------+--------------+----------------------------------------------------------------------+
| ``parameters``  | List(Parameter) | False    | False    | False        |                                                                      |
+-----------------+-----------------+----------+----------+--------------+----------------------------------------------------------------------+
| ``description`` | String          | False    | False    | False        | Transparent service to capture packets flowing through the interface |
|                 |                 |          |          |              | it is attached to, apply filters and obtain capture in .pcap format. |
+-----------------+-----------------+----------+----------+--------------+----------------------------------------------------------------------+


Config Schema
-------------

+---------------+--------------+----------+----------+--------------+---------+
| Field         | Type         | Required | Readonly | Auto Managed | Example |
+===============+==============+==========+==========+==============+=========+
| ``code``      | String       | True     | False    | False        |         |
+---------------+--------------+----------+----------+--------------+---------+
| ``metrics``   | List(Metric) | False    | False    | False        |         |
+---------------+--------------+----------+----------+--------------+---------+


Metric Schema
-------------

+---------------------------+---------------------------+----------+----------+---------------+---------------+
| Field                     | Type                      | Required | Readonly | Auto Managed  | Example       |
+===========================+===========================+==========+==========+===============+===============+
| ``name``                  | String                    | True     | False    | False         | packets_total |
+---------------------------+---------------------------+----------+----------+---------------+---------------+
| ``map_name``              | String                    | True     | False    | False         | PKT_COUNTER   |
+---------------------------+---------------------------+----------+----------+---------------+---------------+
| ``open_metrics_metadata`` | List(OpenMetricsMetadata) | False    | False    | False         |               |
+---------------------------+---------------------------+----------+----------+---------------+---------------+


Open Metrics Metadata Schema
----------------------------

+------------+--------------------------------+----------+----------+--------------+-------------------------------------------------------+
| Field      | Type                           | Required | Readonly | Auto Managed | Example                                               |
+============+==============+=================+==========+==========+==============+=======================================================+
| ``type``   | String                         | True     | False    | False        | counter                                               |
+------------+--------------------------------+----------+----------+--------------+-------------------------------------------------------+
| ``help``   | String                         | False    | False    | False        | This metric represents the number of packets that has |
|            |                                |          |          |              | traveled trough this probe.                           |
+------------+--------------------------------+----------+----------+--------------+-------------------------------------------------------+
| ``labels`` | List(OpenMetricsMetadataLabel) | False    | False    | False        |                                                       |
+------------+--------------------------------+----------+----------+--------------+-------------------------------------------------------+


Open Metrics Metadata Label Schema
----------------------------------

+---------------+--------------+----------+----------+--------------+----------+
| Field         | Type         | Required | Readonly | Auto Managed | Example  |
+===============+==============+==========+==========+==============+==========+
| ``name``      | String       | True     | False    | False        | IP_PROTO |
+---------------+--------------+----------+----------+--------------+----------+
| ``value``     | String       | True     | False    | Faòse        |   UPD    |
+---------------+--------------+----------+----------+--------------+----------+


Parameter Schema
----------------

+-----------------+-------------------+----------+----------+--------------+------------------------------+
| Field           | Type              | Required | Readonly | Auto Managed | Example                      |
+=================+=====================+==========+==========+============+==============================+
| ``id``          | String            | True     | True     | False        | start                        |
+-----------------+-------------------+----------+----------+--------------+------------------------------+
| ``type``        | Enum(String) [1]_ | True     | False    | False        | integer                      |
+-----------------+-------------------+----------+----------+--------------+------------------------------+
| ``list``        | Boolean           | False    | False    | False        | False                        |
+-----------------+-------------------+----------+----------+--------------+------------------------------+
| ``values``      | Enum(String)      | False    | False    | False        | yes, no                      |
+-----------------+-------------------+----------+----------+--------------+------------------------------+
| ``description`` | String            | False    | False    | False        | Network Interface to attach. |
+-----------------+-------------------+----------+----------+--------------+------------------------------+
| ``example``     | String            | False    | False    | False        | 10s                          |
+-----------------+-------------------+----------+----------+--------------+------------------------------+

.. [1] Possible values are "integer", "number", "time-duration", "string", "choice", "boolean", and "binary".

.. warning::

    - It is not possible to update *readonly* fields.
    - it is not possible to set the *Auto managed* fields.

.. note::

    - ``id`` is required but it is auto-generated if not provided.


Create
------

To create a new |eBPF| program in the catalog use the following |REST| call:

.. http:post:: /catalog/ebpf-program/(string:id)

    with the request body in |JSON| format:

    .. sourcecode:: http

        POST /catalog/ebpf-program HTTP/1.1
        Host: cb-manager.example.com
        Content-Type: application/json

        {
            "id": "<ebpf-program-id>",
            "config": {
                "code": "<source-code>",
                "metrics": [
                    {
                        "name": "<metric-name>",
                        "map-name": "<map-name>",
                        "open-metrics-metadata": {
                            "type": "<metric-type>",
                            "help": "<metric-help>",
                            "labels": [
                                {
                                    "name": "<label-name>",
                                    "value": "<label-value>"
                                }
                            ]
                        }
                    }
                ]
            },
            "parameters": [
                {
                    "id": "<parameter-id>",
                    "type": "<parameter-type>",
                    "example": "<parameter-example>",
                    "description": "<parameter-human-readable-description>"
                }
            ]
        }

    :param id: optional |eBPF| program id.

    :reqheader Authorization: HTTP Basic Authentication with username and password.
    :reqheader Content-Type: application/json

    :resheader Content-Type: application/json

    :status 201: |eBPF| Programs correctly created.
    :status 204: No content to create |eBPF| programs for the catalog based on the request.
    :status 400: Request not valid.
    :status 401: Authentication failed.
    :status 406: Request validation failed.
    :status 415: Media type not supported.
    :status 422: Not possible to create ore or more |eBPF| programs for the catalog based on the request.
    :status 500: Server not available to satisfy the request.

    Replace the data with the correct values, for example <ebpf-program-id> with ``nprobe``.

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
                "message": "eBPF program with id=<ebpf-program-id> correctly created"
            }
        ]

    Otherwise, if, for example, an |eBPF| program with the given ``id``
    is already found in the catalog, this is the response:

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

To get the list of the |eBPF| programs available in the catalog:

.. http:get:: /catalog/ebpf-program/(string: id)

    The response includes all the |eBPF| programs.

    It is possible to filter the results using the following request body:

    .. sourcecode:: http

        GET /catalog/ebpf-program HTTP/1.1
        Host: cb-manager.example.com
        Content-Type: application/json

        {
            "select": [ "parameters" ],
            "where": {
                "equals": {
                    "target:" "id",
                    "expr": "<ebpf-program-id>"
                }
            }
        }

    In this way, it will be returned only the ``parameters`` of the |eBPF| program in the catalog with ``id`` = "<ebpf-program-id>".


Update
------

To update an |eBPF| program in the catalog, use:

.. http:put:: /catalog/ebpf-program/(string:id)

    .. sourcecode:: http

        PUT /catalog/ebpf-program HTTP/1.1
        Host: cb-manager.example.com
        Content-Type: application/json

        {
            "id": "<ebpf-program-id>",
            "parameters": [
                {
                    "id": "<parameter-id>",
                    "type": "<new-parameter-type>"
                }
            ]
        }

    :param id: optional |eBPF| program id.

    :reqheader Authorization: HTTP Basic Authentication with username and password.
    :reqheader Content-Type: application/json

    :resheader Content-Type: application/json

    :status 200: All |eBPF| programs in the catalog correctly updated.
    :status 204: No content to update |eBPF| programs in the catalog based on the request.
    :status 304: Update for one or more |eBPF| programs in the catalog not necessary.
    :status 400: Request not valid.
    :status 401: Authentication failed.
    :status 406: Request validation failed.
    :status 415: Media type not supported.
    :status 422: Not possible to update one or more |eBPF| programs in the catalog based on the request.
    :status 500: Server not available to satisfy the request.

    This example updates the new ``type`` of the ``parameter`` with ``id`` = "<parameter-id>" of the
    |eBPF| program with ``id`` = "<ebpf-program-id>".

    .. note:

        Also during the update it is possible to add additional data (not related to parameters)
        for the specific |eBPF| program program.

    A possible response is:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json

        [
            {
                "status": "OK",
                "code": 200,
                "error": false,
                "message": "eBPF Program catalog with id=<ebpf-program-id> correctly updated"
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
                "message": "Update for eBPF program catalog with id=<ebpf-program-id> not necessary"
            }
        ]


Delete
------

To delete |eBPF| programs from the catalog, use:

.. http:delete:: /catalog/ebpf-program/(string:id)

    .. sourcecode:: http

        DELETE /catalog/ebpf-program HTTP/1.1
        Host: cb-manager.example.com
        Content-Type: application/json

        {
            "where": {
                "equals": {
                    "target:" "id",
                    "expr": "<ebpf-program-id>"
                }
            }
        }

    :param id: optional |eBPF| program id from the catalog.

    :reqheader Authorization: HTTP Basic Authentication with username and password.
    :reqheader Content-Type: application/json

    :resheader Content-Type: application/json

    :status 205: All |eBPF| programs correctly deleted from the catalog.
    :status 400: Request not valid.
    :status 401: Authentication failed.
    :status 404: |eBPF| programs based on the request query not found in the catalog.
    :status 406: Request validation failed.
    :status 415: Media type not supported.
    :status 422: Not possible to delete one or more |eBPF| programs from the catalog based on the request query.
    :status 500: Server not available to satisfy the request.

    This request removes from the catalog the |eBPF| program
    with ``id`` = "<ebpf-program-id>".

    This is a possible response:

    .. sourcecode:: http

        HTTP/1.1 205 Reset Content
        Content-Type: application/json

        [
            {
                "status": "Reset Content",
                "code": 200,
                "error": false,
                "message": "eBPF program catalog the id=<agent-id> correctly deleted"
            }
        ]

    .. caution::

        Without request body, it removes **all** the |eBPF| programs from the catalog.


.. |eBPF| replace:: :abbr:`eBPF (extended Berkeley Packet Filter)`
.. |JSON| replace:: :abbr:`JSON (JavaScript Object Notation)`
.. |REST| replace:: :abbr:`REST (Representational State Transfer)`
