.. _exec-env:

Execution Environment
=====================

The execution environment represents the remove service.

When the service is deployed by the the orchestrator, it is necessary to insert related info to the Context Broker.


Schema
------

+-----------------+--------+----------+----------+--------------+---------------------+
| Field           | Type   | Required | Readonly | Auto Managed | Example             |
+=================+========+==========+==========+==============+=====================+
| ``id``          | String | True     | True     | False        | mysql-server        |
+-----------------+--------+----------+----------+--------------+---------------------+
| ``hostname``    | String | True     | False    | False        | 10.0.0.1            |
+-----------------+--------+----------+----------+--------------+---------------------+
| ``type_id``     | String | True     | False    | False        | vm                  |
+-----------------+--------+----------+----------+--------------+---------------------+
| ``lcp``         | |LCP|  | True     | False    | False        |                     |
+-----------------+--------+----------+----------+--------------+---------------------+
| ``description`` | String | False    | False    | False        | Open-source |RDBMS| |
+-----------------+--------+----------+----------+--------------+---------------------+


LCP Schema
----------

+--------------------+---------+----------+----------+--------------+---------+
| Field              | Type    | Required | Readonly | Auto managed | Example |
+=========+==========+=========+==========+==========+==============+=========+
| ``port``           | Integer | True     | False    | False        | 4000    |
+--------------------+---------+----------+----------+--------------+---------+
| ``started``        | Date    | False    | True     | True         |         |
+--------------------+---------+----------+----------+--------------+---------+
| ``last_heartbeat`` | Date    | False    | True     | True         |         |
+--------------------+---------+----------+----------+--------------+---------+
| ``username``       | String  | False    | True     | True         |         |
+--------------------+---------+----------+----------+--------------+---------+
| ``password``       | String  | False    | True     | True         |         |
+--------------------+---------+----------+----------+--------------+---------+

.. warning::

    - It is not possible to update *readonly* fields.
    - it is not possible to set the *auto managed* fields.

.. note::

    - ``id`` is required but it is auto-generated if not provided.
      It is recommended to provide a friendly for simplify the retrieve of connected date in other indices.
    - ``type_id`` should be one of those stored in :ref:`exec-env-type` index.


.. _exec-env-create:

Create
------

To create a new Execution Environment use the following |REST| call:

.. http:post:: /exec-env/(string:id)

    with the request body in |JSON| format:

    .. sourcecode:: http

        POST /exec-env HTTP/1.1
        Host: cb-manager.example.com
        Content-Type: application/json

        {
            "id": "<exec-env-id>",
            "description": "<description>",
            "type_id": "<exec-env-type-id>",
            "hostname":"<ip-address>",
            "lcp": {
                "port": "<lcp-port>"
            }
        }

    :param id: optional execution environments id.

    :reqheader Authorization: HTTP Basic Authentication with username and password.
    :reqheader Content-Type: application/json

    :resheader Content-Type: application/json

    :status 201: Execution environments correctly created.
    :status 204: No content to create execution environments based on the request.
    :status 400: Request not valid.
    :status 401: Authentication failed.
    :status 406: Request validation failed.
    :status 415: Media type not supported.
    :status 422: Not possible to create ore or more execution environments based on the request.
    :status 500: Server not available to satisfy the request.

    Replace the data with the correct values, for example <exec-env-id> with ``apache-server``.

    .. note::

        It is possible to add additional data specific for this execution environment.

    If the creation is correctly executed the response is:

    .. sourcecode:: http

        HTTP/1.1 201 Created
        Content-Type: application/json

        [
            {
                "status": "Created",
                "code": 201,
                "error": false,
                "message": "Executed environment with id=<exec-env-id> correctly created"
            }
        ]

    Otherwise, if, for example, an execution environment with the given ``id`` is already found, this is the response:

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

    If some required data is missing (for example ``hostname``), the response could be:

    .. sourcecode:: http

        HTTP/1.1 406 Not Acceptable
        Content-Type: application/json

        [
            {
                "status": "Not Acceptable",
                "code": 406,
                "error": true,
                "message": {
                    "hostname": "required"
                }
            }
        ]


Read
----

To get the list of execution environment:

.. http:get:: /exec-env/(string: id)

    The response includes all the execution environments created.

    It is possible to filter the results using the following request body:

    .. sourcecode:: http

        GET /exec-env HTTP/1.1
        Host: cb-manager.example.com
        Content-Type: application/json

        {
            "select": [ "hostname" ],
            "where": {
                "equals": {
                    "target:" "id",
                    "expr": "<exec-env-id>"
                }
            }
        }

    :param id: optional execution environment id.

    :reqheader Authorization: HTTP Basic Authentication with username and password.
    :reqheader Content-Type: application/json

    :resheader Content-Type: application/json

    :status 200: List of execution environments filtered by the query in the request body.
    :status 400: Request not valid.
    :status 401: Authentication failed.
    :status 404: Execution environments based on the request query not found.
    :status 406: Request validation failed.
    :status 415: Media type not supported.
    :status 422: Not possible to get execution environments with the request query.
    :status 500: Server not available to satisfy the request.

    In this way, it will be returned only the ``hostname`` of all the execution environments with ``id`` = "<exec-env-id>"


Update
------

To update an execution environment, use:

.. http:put:: /exec-env/(string:id)

    .. sourcecode:: http

        PUT /exec-env HTTP/1.1
        Host: cb-manager.example.com
        Content-Type: application/json

        {
            "id": "<exec-env-id>",
            "hostname":"<new-ip-address>",
        }

    :param id: optional execution environment id.

    :reqheader Authorization: HTTP Basic Authentication with username and password.
    :reqheader Content-Type: application/json

    :resheader Content-Type: application/json

    :status 200: All execution environments correctly updated.
    :status 204: No content to update execution environments based on the request.
    :status 304: Update for one or more execution environments not necessary.
    :status 400: Request not valid.
    :status 401: Authentication failed.
    :status 406: Request validation failed.
    :status 415: Media type not supported.
    :status 422: Not possible to update one or more execution environments based on the request.
    :status 500: Server not available to satisfy the request.

    This example set the new ``hostname`` for execution environment with ``id`` = "<exec-env-id>".

    .. note::

        Also during the update it is possible to add additional data for the specific execution environment.

    A possible response is:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json

        [
            {
                "status": "OK",
                "code": 200,
                "error": false,
                "message": "Execution environment with id=<exec-env-id> correctly updated"
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
                "message": "Update for execution environment with id=<exec-env-id> not necessary"
            }
        ]


Delete
------

To delete an execution environment, use:

.. http:delete:: /exec-env/(string:id)

    .. sourcecode:: http

        DELETE /exec-env HTTP/1.1
        Host: cb-manager.example.com
        Content-Type: application/json

        {
            "where": {
                "equals": {
                    "target:" "id",
                    "expr": "<exec-env-id>"
                }
            }
        }

    :param id: optional execution environment id.

    :reqheader Authorization: HTTP Basic Authentication with username and password.
    :reqheader Content-Type: application/json

    :resheader Content-Type: application/json

    :status 205: All execution environments correctly deleted.
    :status 400: Request not valid.
    :status 401: Authentication failed.
    :status 404: Execution environments based on the request query not found.
    :status 406: Request validation failed.
    :status 415: Media type not supported.
    :status 422: Not possible to delete one or more execution environments based on the request query.
    :status 500: Server not available to satisfy the request.

    This request removes the execution environment with ``id`` = <exec-env-id>".

    This is a possible response:

    .. sourcecode:: http

        HTTP/1.1 205 Reset Content
        Content-Type: application/json

        [
            {
                "status": "Reset Content",
                "code": 200,
                "error": false,
                "message": "Execution environment with id=<exec-env-id> correctly deleted"
            }
        ]

    .. caution::

        Without request body, it removes *all* the execution environments.


.. |JSON| replace:: :abbr:`JSON (JavaScript Object Notation)`
.. |LCP| replace:: :abbr:`LCP (Local Control Plane)`
.. |REST| replace:: :abbr:`REST (Representational State Transfer)`
.. |RDBMS| replace:: :abbr:`RDBMS (Relational Database Management System)`
