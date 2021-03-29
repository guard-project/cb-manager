.. _event:

Event
=====

This index stores all the incoming events.

Schema
------

+------------------------------+--------+----------+----------+--------------+----------------------------+
| Field                        | Type   | Required | Readonly | Auto Managed | Example                    |
+=================+============+========+==========+==========+==============+============================+
| ``id``                       | String | True     | True     | False        | dsalkasdioi232382yieyqwuiy |
+------------------------------+--------+----------+----------+--------------+----------------------------+

.. warning::

    - It is not possible to update *readonly* fields.
    - it is not possible to set the *Auto managed* fields.

.. note::

    - ``id`` is required but it is auto-generated if not provided.
      It is recommended to provide a friendly for simplify the retrieve of connected date in other indices.


Create
------

To create a new event use the following |REST| call:

.. http:post:: /event/(string:id)

    with the request body in |JSON| format:

    .. sourcecode:: http

        POST /event HTTP/1.1
        Host: cb-manager.example.com
        Content-Type: application/json

        {
            "id": "<event-id>"
        }

    :param id: optional event id.

    :reqheader Authorization: JWT Authentication.
    :reqheader Content-Type: application/json

    :resheader Content-Type: application/json

    :status 201: Event correctly created.
    :status 204: No content to create event based on the request.
    :status 400: Request not valid.
    :status 401: Authentication failed.
    :status 406: Request validation failed.
    :status 415: Media type not supported.
    :status 422: Not possible to create ore or more events based on the request.
    :status 500: Server not available to satisfy the request.

    Replace the data with the correct values, for example <event-id> with ``alert-attack``.

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
                "message": "Event with id=<event-id> correctly created"
            }
        ]

    Otherwise, if, for example, an event with the given ``id`` is already found, this is the response:

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

To get the list of events:

.. http:get:: /event/(string: id)

    The response includes all the events created.

    It is possible to filter the results using the following request body:

    .. sourcecode:: http

        GET /event HTTP/1.1
        Host: cb-manager.example.com
        Content-Type: application/json

        {
            "select": [ "id" ],
            "where": {
                "equals": {
                    "target:" "id",
                    "expr": "<event-id>"
                }
            }
        }

    :param id: optional event id.

    :reqheader Authorization: JWT Authentication.
    :reqheader Content-Type: application/json

    :resheader Content-Type: application/json

    :status 200: List of events filtered by the query in the request body.
    :status 400: Request not valid.
    :status 401: Authentication failed.
    :status 404: Event based on the request query not found.
    :status 406: Request validation failed.
    :status 415: Media type not supported.
    :status 422: Not possible to get events with the request query.
    :status 500: Server not available to satisfy the request.

    In this way, it will be returned only the ``id`` of the event with ``id`` = "<event-id>".


Update
------

To update an event, use:

.. http:put:: /event/(string:id)

    .. sourcecode:: http

        PUT /event HTTP/1.1
        Host: cb-manager.example.com
        Content-Type: application/json

        {
            "id": "<event-id>",
            "source": "<ip-address>"
        }

    :param id: optional event id.

    :reqheader Authorization: JWT Authentication.
    :reqheader Content-Type: application/json

    :resheader Content-Type: application/json

    :status 200: All events correctly updated.
    :status 204: No content to update events based on the request.
    :status 304: Update for one or more events not necessary.
    :status 400: Request not valid.
    :status 401: Authentication failed.
    :status 406: Request validation failed.
    :status 415: Media type not supported.
    :status 422: Not possible to update one or more events based on the request.
    :status 500: Server not available to satisfy the request.

    This example add a new field ``source`` for the event with ``id`` = "<event-id>".

    A possible response is:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json

        [
            {
                "status": "OK",
                "code": 200,
                "error": false,
                "message": "Event with id=<event-id> correctly updated"
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
                "message": "Update for event with id=<event-id> not necessary"
            }
        ]


Delete
------

To delete events, use:

.. http:delete:: /event/(string:id)

    .. sourcecode:: http

        DELETE /event HTTP/1.1
        Host: cb-manager.example.com
        Content-Type: application/json

        {
            "where": {
                "equals": {
                    "target:" "id",
                    "expr": "<event-id>"
                }
            }
        }

    :param id: optional event id.

    :reqheader Authorization: JWT Authentication.
    :reqheader Content-Type: application/json

    :resheader Content-Type: application/json

    :status 205: All events correctly deleted.
    :status 400: Request not valid.
    :status 401: Authentication failed.
    :status 404: Event based on the request query not found.
    :status 406: Request validation failed.
    :status 415: Media type not supported.
    :status 422: Not possible to delete one or more events based on the request query.
    :status 500: Server not available to satisfy the request.

    This request removes the event with ``id`` = "<event-id>".

    This is a possible response:

    .. sourcecode:: http

        HTTP/1.1 205 Reset Content
        Content-Type: application/json

        [
            {
                "status": "Reset Content",
                "code": 200,
                "error": false,
                "message": "Event with id=<event-id> correctly deleted"
            }
        ]

    .. caution::

        Without request body, it removes **all** the events.


.. |JSON| replace:: :abbr:`JSON (JavaScript Object Notation)`
.. |REST| replace:: :abbr:`REST (Representational State Transfer)`
