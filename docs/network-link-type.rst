.. _network-link-type:

Network Link Type
=================

Describes the type of the network link including additional info.

Each :ref:`network-link` belongs to a specific type that is referred with the ``type_id`` field (see :ref:`network-link-create`).


Schema
------

+-----------------+--------+----------+----------+--------------+--------------------------------------------------------+
| Field           | Type   | Required | Readonly | Auto Managed | Example                                                |
+=================+========+==========+==========+==============+========================================================+
| ``id``          | String | True     | True     | False        | pnt2pnt                                                |
+-----------------+--------+----------+----------+--------------+--------------------------------------------------------+
| ``name``        | String | True     | False    | False        | Point to Point                                         |
+-----------------+--------+----------+----------+--------------+--------------------------------------------------------+
| ``description`` | String | False    | False    | False        | Communications connection between two                  |
|                 |        |          |          |              | communication endpoints or nodes.                      |
+-----------------+--------+----------+----------+--------------+--------------------------------------------------------+

.. warning::

    - It is not possible to update *readonly* fields.
    - it is not possible to set the *auto managed* fields.

.. note::

    - ``id`` is required but it is auto-generated if not provided.
      It is recommended to provide a friendly for simplify the retrieve of connected date in other indices.


Create
------

To create a new network link type use the following |REST| call:

.. http:post:: /type/network-link/(string:id)

    with the request body in |JSON| format:

    .. sourcecode:: http

        POST /type/network-link HTTP/1.1
        Host: cb-manager.example.com
        Content-Type: application/json

        {
            "id": "<type-id>",
            "description": "<human-readable-description>"
            "name": "<formal-name>"
        }

    :param id: optional network link type id.

    :reqheader Authorization: JWT Authentication.
    :reqheader Content-Type: application/json

    :resheader Content-Type: application/json

    :status 201: Network link types correctly created.
    :status 204: No content to create network link types based on the request.
    :status 400: Request not valid.
    :status 401: Authentication failed.
    :status 406: Request validation failed.
    :status 415: Media type not supported.
    :status 422: Not possible to create ore or more network link types based on the request.
    :status 500: Server not available to satisfy the request.

    Replace the data with the correct values, for example ``id`` with ``p2p``.

    .. note::

        It is possible to add additional data specific for this network link type.

    If the creation is correctly executed the response is:

    .. sourcecode:: http

        HTTP/1.1 201 Created
        Content-Type: application/json

        [
            {
                "status": "Created",
                "code": 201,
                "error": false,
                "message": "Network link type with id=<network-link-type-id> correctly created"
            }
        ]

    Otherwise, if, for example, a network link type with the given ``id`` is already found, this is the response:

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

    If some required data is missing (for example ``name``), the response could be:

    .. sourcecode:: http

        HTTP/1.1 406 Not Acceptable
        Content-Type: application/json

        [
            {
                "status": "Not Acceptable",
                "code": 406,
                "error": true,
                "message": {
                    "name": "required"
                }
            }
        ]

Read
----

To get the list of network Link types:

.. http:get:: /type/network-link/(string: id)

    The response includes all the network link types created.

    It is possible to filter the results using the following request body:

    .. sourcecode:: http

        GET /type/network-link HTTP/1.1
        Host: cb-manager.example.com
        Content-Type: application/json

        {
            "select": [ "type_id" ],
            "where": {
                "equals": {
                    "target:" "id",
                    "expr": "<network-link-type-id>"
                }
            }
        }


    :param id: optional network link type id.

    :reqheader Authorization: JWT Authentication.
    :reqheader Content-Type: application/json

    :resheader Content-Type: application/json

    :status 200: List of network link types filtered by the query in the request body.
    :status 400: Request not valid.
    :status 401: Authentication failed.
    :status 404: Network link types based on the request query not found.
    :status 406: Request validation failed.
    :status 415: Media type not supported.
    :status 422: Not possible to get network link types with the request query.
    :status 500: Server not available to satisfy the request.

    In this way, it will be returned only the ``name`` of all the network
    link types with ``id`` = "<network-link-type-id>".


Update
------

To update a network Link type, use:

.. http:put:: /type/network-link/(string:id)

    .. sourcecode:: http

        PUT /type/network-link HTTP/1.1
        Host: cb-manager.example.com
        Content-Type: application/json

        {
            "id": "<network-link-type-id>",
            "name":"<new-formal-name>",
        }

    :param id: optional network link type id.

    :reqheader Authorization: JWT Authentication.
    :reqheader Content-Type: application/json

    :resheader Content-Type: application/json

    :status 200: All network link types correctly updated.
    :status 204: No content to update network link types based on the request.
    :status 304: Update for one or more network link types not necessary.
    :status 400: Request not valid.
    :status 401: Authentication failed.
    :status 406: Request validation failed.
    :status 415: Media type not supported.
    :status 422: Not possible to update one or more network link types based on the request.
    :status 500: Server not available to satisfy the request.

    This example set the new ``name`` for the network link type with ``id`` = "<network-link-type-id>".

    .. note:

        Also during the update it is possible to add additional data for the specific network link type.

    A possible response is:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json

        [
            {
                "status": "OK",
                "code": 200,
                "error": false,
                "message": "Network link type with  id=<network-link-type-id> correctly updated"
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
                "message": "Update for network link type with id=<network-link-type-id> not necessary"
            }
        ]


Delete
------

To delete network link types, use:

.. http:delete:: /type/network-link/(string:id)

    .. sourcecode:: http

        DELETE /type/network-link HTTP/1.1
        Host: cb-manager.example.com
        Content-Type: application/json

        {
            "where": {
                "equals": {
                    "target:" "id",
                    "expr": "<network-link-type-id>"
                }
            }
        }

    :param id: optional network link type id.

    :reqheader Authorization: JWT Authentication.
    :reqheader Content-Type: application/json

    :resheader Content-Type: application/json

    :status 205: All network link types correctly deleted.
    :status 400: Request not valid.
    :status 401: Authentication failed.
    :status 404: Network link types based on the request query not found.
    :status 406: Request validation failed.
    :status 415: Media type not supported.
    :status 422: Not possible to delete one or more network link types based on the request query.
    :status 500: Server not available to satisfy the request.

    This request removes the network link type with ``id`` = "<network-link-type-id>".

    This is a possible response:

    .. sourcecode:: http

        HTTP/1.1 205 Reset Content
        Content-Type: application/json

        [
            {
                "status": "Reset Content",
                "code": 200,
                "error": false,
                "message": "Network link with id=<network-link-type-id> correctly deleted"
            }
        ]

    .. caution::

        Without request body, it removes **all** the network link types.


Loaded data
-----------

For the demo, this data is already available:

.. http:get:: /type/network-link

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json

        [
            {
                "id": "p2p",
                "name": "Point to Point",
                "description": "Communications connection between two communication endpoints or nodes."
            },
            {
                "id": "slide",
                "name": "Slice",
                "description": """Separation of multiple virtual networks that operate on the same physical hardware
                                  for different applications, services or purposes."""
            }
        ]


.. |JSON| replace:: :abbr:`JSON (JavaScript Object Notation)`
.. |REST| replace:: :abbr:`REST (Representational State Transfer)`
