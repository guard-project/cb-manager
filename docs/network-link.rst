.. _network-link:

Network Link
============

Represents a network link that connect two or more :ref:`exec-env`.


Schema
------

+-----------------+--------+----------+----------+--------------+-------------------------------------+
| Field           | Type   | Required | Readonly | Auto Managed | Example                             |
+=================+========+==========+==========+==============+=====================================+
| ``id``          | String | True     | True     | False        | eth0                                |
+-----------------+--------+----------+----------+--------------+-------------------------------------+
| ``type_id``     | String | True     | False    | False        | pnt2pnt                             |
+-----------------+--------+----------+----------+--------------+-------------------------------------+
| ``description`` | String | False    | False    | False        | To connect |HTTP| and |DB| Servers. |
+-----------------+--------+----------+----------+--------------+-------------------------------------+

.. warning::

    - It is not possible to update *readonly* fields.
    - it is not possible to set the *auto managed* fields.

.. note::

    - ``id`` is required but it is auto-generated if not provided.
      It is recommended to provide a friendly for simplify the retrieve of connected date in other indices.
    - ``type_id`` should be one of those stored in :ref:`network-link-type`.


.. _network-link-create:

Create
------

To create a new network link use the following |REST| call:

.. http:post:: /network-link/(string:id)

    with the request body in |JSON| format:

    .. sourcecode:: http

        POST /network-link HTTP/1.1
        Host: cb-manager.example.com
        Content-Type: application/json

        {
            "id": "<network-link-id>",
            "type_id": "<network-link-type-id>",
            "description":"<human-readable-description>"
        }

    :param id: optional network link id.

    :reqheader Authorization: HTTP Basic Authentication with username and password.
    :reqheader Content-Type: application/json

    :resheader Content-Type: application/json

    :status 201: Network links correctly created.
    :status 204: No content to create network links based on the request.
    :status 400: Request not valid.
    :status 401: Authentication failed.
    :status 406: Request validation failed.
    :status 415: Media type not supported.
    :status 422: Not possible to create ore or more network links based on the request.
    :status 500: Server not available to satisfy the request.

    Replace the data with the correct values, for example ``network-link-id`` with ``eth0``.

    .. note:

        It is possible to add additional data specific for this network link.

    If the creation is correctly executed the response is:

    .. sourcecode:: http

        HTTP/1.1 201 Created
        Content-Type: application/json

        [
            {
                "status": "Created",
                "code": 201,
                "error": false,
                "message": "Network link with id=<network-link-id> correctly created"
            }
        ]

    Otherwise, if, for example, a network link with the given ``id`` is already found, this is the response:

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

    If some required data is missing (for example ``type_id``), the response could be:

    .. sourcecode:: http

        HTTP/1.1 406 Not Acceptable
        Content-Type: application/json

        [
            {
                "status": "Not Acceptable",
                "code": 406,
                "error": true,
                "message": {
                    "type_id": "required"
                }
            }
        ]


Read
----

To get the list of network links:

.. http:get:: /network-link/(string: id)

    The response includes all the network links created.

    It is possible to filter the results using the following request body:

    .. sourcecode:: http

        GET /network-link HTTP/1.1
        Host: cb-manager.example.com
        Content-Type: application/json

        {
            "select": [ "type_id" ],
            "where": {
                "equals": {
                    "target:" "id",
                    "expr": "<network-link-id>"
                }
            }
        }


    :param id: optional network link id.

    :reqheader Authorization: HTTP Basic Authentication with username and password.
    :reqheader Content-Type: application/json

    :resheader Content-Type: application/json

    :status 200: List of network links filtered by the query in the request body.
    :status 400: Request not valid.
    :status 401: Authentication failed.
    :status 404: Network links based on the request query not found.
    :status 406: Request validation failed.
    :status 415: Media type not supported.
    :status 422: Not possible to get network links with the request query.
    :status 500: Server not available to satisfy the request.

    In this way, it will be returned only the ``type_id`` of the network link with ``id`` = "<network-link-id>".


Update
------

To update a network link, use:

.. http:put:: /network-link/(string:id)

    .. sourcecode:: http

        PUT /network-link HTTP/1.1
        Host: cb-manager.example.com
        Content-Type: application/json

        {
            "id": "<network-link-id>",
            "type_id":"<new-network-link-type-id>",
        }

    :param id: optional network link id.

    :reqheader Authorization: HTTP Basic Authentication with username and password.
    :reqheader Content-Type: application/json

    :resheader Content-Type: application/json

    :status 200: All network links correctly updated.
    :status 204: No content to update network links based on the request.
    :status 304: Update for one or more network links not necessary.
    :status 400: Request not valid.
    :status 401: Authentication failed.
    :status 406: Request validation failed.
    :status 415: Media type not supported.
    :status 422: Not possible to update one or more network links based on the request.
    :status 500: Server not available to satisfy the request.

    This example set the new ``type_id`` for the network link with ``id`` = "<network-link-id>".

    .. note::

        Allso during the update it is possible to add additional data for the specific network link.

    A possible response is:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json

        [
            {
                "status": "OK",
                "code": 200,
                "error": false,
                "message": "Network link with id=<network-link-id> correctly updated"
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
                "message": "Update for network link with id=<network-link-id> not necessary"
            }
        ]


Delete
------

To delete network links, use:

.. http:delete:: /network-link/(string:id)

    .. sourcecode:: http

        DELETE /network-link HTTP/1.1
        Host: cb-manager.example.com
        Content-Type: application/json

        {
            "where": {
                "equals": {
                    "target:" "id",
                    "expr": "<network-link-id>"
                }
            }
        }

    :param id: optional network link id.

    :reqheader Authorization: HTTP Basic Authentication with username and password.
    :reqheader Content-Type: application/json

    :resheader Content-Type: application/json

    :status 205: All network links correctly deleted.
    :status 400: Request not valid.
    :status 401: Authentication failed.
    :status 404: Network links based on the request query not found.
    :status 406: Request validation failed.
    :status 415: Media type not supported.
    :status 422: Not possible to delete one or more network links based on the request query.
    :status 500: Server not available to satisfy the request.

    This request removes the network link with ``id`` = "<network-link-id>".

    This is a possible response:

    .. sourcecode:: http

        HTTP/1.1 205 Reset Content
        Content-Type: application/json

        [
            {
                "status": "Reset Content",
                "code": 200,
                "error": false,
                "message": "Network link with id=<network-link-id> correctly deleted"
            }
        ]

    .. caution::

        Without request body, it removes **all** the network links.


.. |DB| replace:: :abbr:`DB (DataBase)`
.. |HTTP| replace:: :abbr:`HTTP (HyperText Transfer Protocol)`
.. |JSON| replace:: :abbr:`JSON (JavaScript Object Notation)`
.. |REST| replace:: :abbr:`REST (Representational State Transfer)`
