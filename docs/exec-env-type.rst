.. _exec-env-type:

Execution Environment Type
==========================

Describes the type of the :ref:`exec-env` including additional info.

Each execution environment belongs to a specific type that is referred with the ``type_id`` field (see :ref:`exec-env-create`).


Schema
------

+-----------------+--------+----------+----------+--------------+---------------------------------------------+
| Field           | Type   | Required | Readonly | Auto Managed | Example                                     |
+=================+========+==========+==========+==============+=============================================+
| ``id``          | String | True     | True     | False        | vm                                          |
+-----------------+--------+----------+----------+--------------+---------------------------------------------+
| ``name``        | String | True     | False    | False        | Virtual Machine                             |
+-----------------+--------+----------+----------+--------------+---------------------------------------------+
| ``description`` | String | False    | False    | False        | The service is deployed in virtual machine. |
+-----------------+--------+----------+----------+--------------+---------------------------------------------+

.. warning::

    - It is not possible to update *readonly* fields.
    - it is not possible to set the *auto managed* fields.

.. note::

    - ``id`` is required but it is auto-generated if not provided.
      It is recommended to provide a friendly for simplify the retrieve of connected date in other indices.


Create
------

To create a new execution environment type use the following |REST| call:

.. http:post:: /type/exec-env/(string:id)

    with the request body in |JSON| format:

    .. sourcecode:: http

        POST /type/exec-env HTTP/1.1
        Host: cb-manager.example.com
        Content-Type: application/json

        {
            "id": "<type-id>",
            "name": "<formal-name>"
        }

    :param id: optional execution environment type id.

    :reqheader Authorization: HTTP Basic Authentication with username and password.
    :reqheader Content-Type: application/json

    :resheader Content-Type: application/json

    :status 201: Execution environment types correctly created.
    :status 204: No content to create execution environment types based on the request.
    :status 400: Request not valid.
    :status 401: Authentication failed.
    :status 406: Request validation failed.
    :status 415: Media type not supported.
    :status 422: Not possible to create ore or more execution environment types based on the request.
    :status 500: Server not available to satisfy the request.

    Replace the data with the correct values, for example <type-id>, and <formal-name> with "vm"
    and "Virtual Machine", respectively.

    .. note::

        It is possible to add additional data specific for this execution environment type.

    If the creation is correctly executed the response is:

    .. sourcecode:: http

        HTTP/1.1 201 Created
        Content-Type: application/json

        [
            {
                "status": "Created",
                "code": 201,
                "error": false,
                "message": "Executed environment type with id=<exec-env-type-id> correctly created"
            }
        ]

    Otherwise, if, for example, an execution environment type with the given ``id`` is already found, this is the response:

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

To get the list of execution environment types:

.. http:get:: /type/exec-env/(string: id)

    The response includes all the execution environment types created.

    It is possible to filter the results using the following request body:

    .. sourcecode:: http

        GET /type/exec-env HTTP/1.1
        Host: cb-manager.example.com
        Content-Type: application/json

        {
            "select": [ "name" ],
            "where": {
                "equals": {
                    "target:" "id",
                    "expr": "<exec-env-type-id>"
                }
            }
        }

    :param id: optional execution environment type id.

    :reqheader Authorization: HTTP Basic Authentication with username and password.
    :reqheader Content-Type: application/json

    :resheader Content-Type: application/json

    :status 200: List of execution environment types filtered by the query in the request body.
    :status 400: Request not valid.
    :status 401: Authentication failed.
    :status 404: Execution environment types based on the request query not found.
    :status 406: Request validation failed.
    :status 415: Media type not supported.
    :status 422: Not possible to get execution environment types with the request query.
    :status 500: Server not available to satisfy the request.

    In this way, it will be returned only the ``name`` of the execution environment type with ``id`` = "<type-id>".


Update
------

To update an execution environment type, use:

.. http:put:: /type/exec-env/(string:id)

    .. sourcecode:: http

        PUT /type/exec-env HTTP/1.1
        Host: cb-manager.example.com
        Content-Type: application/json

        {
            "id": "<exec-env-type-id>",
            "name":"<new-formal-name>",
        }

    :param id: optional execution environment type id.

    :reqheader Authorization: HTTP Basic Authentication with username and password.
    :reqheader Content-Type: application/json

    :resheader Content-Type: application/json

    :status 200: All execution environment types correctly updated.
    :status 204: No content to update execution environment types based on the request.
    :status 304: Update for one or more execution environment types not necessary.
    :status 400: Request not valid.
    :status 401: Authentication failed.
    :status 406: Request validation failed.
    :status 415: Media type not supported.
    :status 422: Not possible to update one or more execution environment types based on the request.
    :status 500: Server not available to satisfy the request.

    This example set the new ``name`` for the execution environment type with ``id`` = "<type-id>".

    .. note:

        Also during the update it is possible to add additional data for the specific execution environment type.

    A possible response is:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json

        [
            {
                "status": "OK",
                "code": 200,
                "error": false,
                "message": "Execution environment type with id=<exec-env-id> correctly updated"
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
                "message": "Update for execution environment type with id=<exec-env-id> not necessary"
            }
        ]

Delete
------

To delete an execution environment type, use:

.. http:delete:: /type/exec-env/(string:id)

    .. sourcecode:: http

        DELETE /type/exec-env HTTP/1.1
        Host: cb-manager.example.com
        Content-Type: application/json

        {
            "where": {
                "equals": {
                    "target:" "id",
                    "expr": "<exec-env-type-id>"
                }
            }
        }

    :param id: optional execution environment type id.

    :reqheader Authorization: HTTP Basic Authentication with username and password.
    :reqheader Content-Type: application/json

    :resheader Content-Type: application/json

    :status 205: All execution environments correctly deleted.
    :status 400: Request not valid.
    :status 401: Authentication failed.
    :status 404: Execution environment types based on the request query not found.
    :status 406: Request validation failed.
    :status 415: Media type not supported.
    :status 422: Not possible to delete one or more execution environment types based on the request query.
    :status 500: Server not available to satisfy the request.

    This request removes the execution environment type with ``id`` = "<exec-env-id>".

    This is a possible response:

    .. sourcecode:: http

        HTTP/1.1 205 Reset Content
        Content-Type: application/json

        [
            {
                "status": "Reset Content",
                "code": 200,
                "error": false,
                "message": "Execution environment type with id=<exec-env-type-id> correctly deleted"
            }
        ]

    .. caution::

        Without request body, it removes **all** the execution environment types.


Loaded data
-----------

This data is already available:

.. http:get:: /type/exec-env

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json

        [
            {
                "id": "vm",
                "name": "Virtual Machine",
                "description": "The service is deployed in a virtual machine."
            },
            {
                "id": "container",
                "name": "Container",
                "description": "The service is deployed in a container."
            },
            {
                "id": "host",
                "name": "Host",
                "description": "The service is deployed in a physical machine."
            }
        ]


.. |JSON| replace:: :abbr:`JSON (JavaScript Object Notation)`
.. |REST| replace:: :abbr:`REST (Representational State Transfer)`
