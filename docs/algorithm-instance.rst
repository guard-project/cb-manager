.. _algorithm-instance:

Algorithm Instance
==================

Contains the :ref:`algorithm-catalog` instances.


Schema
------

+--------------------------+-----------------+----------+----------+--------------+------------------+
| Field                    | Type            | Required | Readonly | Auto Managed | Example          |
+==========================+=================+==========+==========+==============+==================+
| ``id``                   | String          | True     | True     | False        | ddos-predictor-1 |
+--------------------------+-----------------+----------+----------+--------------+------------------+
| ``algorithm_catalog_id`` | String          | True     | True     | False        | ddos-predictor   |
+--------------------------+-----------------+----------+----------+--------------+------------------+
| ``operations``           | List(Operation) | False    | True     | False        |                  |
+--------------------------+-----------------+----------+----------+--------------+------------------+
| ``description``          | String          | False    | False    | False        | DDoS predictor.  |
+--------------------------+-----------------+----------+----------+--------------+------------------+


Operation Schema
----------------

+----------------+-----------------+----------+----------+--------------+---------+
| Field          | Type            | Required | Readonly | Auto Managed | Example |
+================+=================+==========+==========+==============+=========+
| ``parameters`` | List(Parameter) | False    | False    | False        |         |
+----------------+-----------------+----------+----------+--------------+---------+


Parameter Schema
----------------

+---------------+----------+----------+----------+--------------+---------+
| Field         | Type     | Required | Readonly | Auto Managed | Example |
+===============+==========+==========+==========+==============+=========+
| ``id``        | String   | True     | True     | False        | period  |
+---------------+----------+----------+----------+--------------+---------+
| ``value``     | Any      | True     | False    | False        | 10s     |
+---------------+----------+----------+----------+--------------+---------+


.. warning::

    - It is not possible to update *readonly* fields.
    - it is not possible to set the *Auto managed* fields.

.. note::

    - ``id`` is required but it is auto-generated if not provided.
      It is recommended to provide a friendly for simplify the retrieve of connected date in other indices.
      A common syntax is to use and ``id`` that includes the ``algorithm_catalog_id``.
    - ``algorithm_catalog_id`` should be one of those stored in :ref:`algorithm-catalog` index.


Create
------

To create a new algorithm instance use the following |REST| call:

.. http:post:: /instance/algorithm/(string:id)

    with the request body in |JSON| format:

    .. sourcecode:: http

        POST /instance/algorithm HTTP/1.1
        Host: cb-manager.example.com
        Content-Type: application/json

        {
            "id": "<algorithm-instance-id>",
            "algorithm_catalog_id": "<algorithm-id>",
            "operations": [
                "parameters": [
                    {
                        "id": "<parameter-id>",
                        "value": "<parameter-value>",
                    }
                ]
            ]
        }

    :param id: optional algorithm instance id.

    :reqheader Authorization: JWT Authentication.
    :reqheader Content-Type: application/json

    :resheader Content-Type: application/json

    :status 201: Algorithm instances correctly created.
    :status 204: No content to create algorithm instances based on the request.
    :status 400: Request not valid.
    :status 401: Authentication failed.
    :status 406: Request validation failed.
    :status 415: Media type not supported.
    :status 422: Not possible to create ore or more algorithm instances based on the request.
    :status 500: Server not available to satisfy the request.

    Replace the data with the correct values, for example <algorithm-instance-id> with "firewall@mysql-server".

     .. note:

        It is possible to add additional data specific for this algorithm.

    If the creation is correctly executed the response is:

    .. sourcecode:: http

        HTTP/1.1 201 Created
        Content-Type: application/json

        [
            {
                "status": "Created",
                "code": 201,
                "error": false,
                "message": "Algorithm instance with id=<algorithm-instance-id> correctly created"
            }
        ]

    Otherwise, if, for example, an algorithm instance with the given ``id`` is already found, this is the response:

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

To get the list of the algorithm instances:

.. http:get:: /instance/algorithm/(string: id)

    The response includes all the algorithm instances.

    It is possible to filter the results using the following request body:

    .. sourcecode:: http

        GET /instance/algorithm HTTP/1.1
        Host: cb-manager.example.com
        Content-Type: application/json

        {
            "select": [ "parameters" ],
            "where": {
                "equals": {
                    "target:" "id",
                    "expr": "<algorithm-instance-id>"
                }
            }
        }

    In this way, it will be returned only the ``parameters`` of the algorithm instance with ``id`` = "<algorithm-instance-id>".


Update
------

To update an algorithm instance, use:

.. http:put:: /instance/algorithm/(string:id)

    .. sourcecode:: http

        PUT /instance/algorithm HTTP/1.1
        Host: cb-manager.example.com
        Content-Type: application/json

        {
            "id": "<algorithm-instance-id}",
            "operations": [
                "parameters": [
                    {
                        "id": "<parameter-id>",
                        "value": "<new-parameter-value>"
                    }
                ]
            ]
        }

    :param id: optional algorithm instance id.

    :reqheader Authorization: JWT Authentication.
    :reqheader Content-Type: application/json

    :resheader Content-Type: application/json

    :status 200: All algorithm instances correctly updated.
    :status 204: No content to update algorithm instances based on the request.
    :status 304: Update for one or more algorithm instances not necessary.
    :status 400: Request not valid.
    :status 401: Authentication failed.
    :status 406: Request validation failed.
    :status 415: Media type not supported.
    :status 422: Not possible to update one or more algorithm instances based on the request.
    :status 500: Server not available to satisfy the request.

    This example updates the ``value`` of the ``parameter`` with ``id`` = "<parameter-id>" of the algorithm instance with ``id`` = "<algorithm-instance-id>".

    .. note:

        Also during the update it is possible to add additional data (not related to actions or parameters) for the specific algorithm instances.

    A possible response is:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json

        [
            {
                "status": "OK",
                "code": 200,
                "error": false,
                "message": "Algorithm instance with id=<algorithm-instance-id> correctly updated"
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
                "message": "Update for algorithm instance with id=<algorithm-instance-id> not necessary"
            }
        ]

Delete
------

To delete algorithm instances, use:

.. http:delete:: /instance/algorithm/(string:id)

    .. sourcecode:: http

        DELETE /instance/algorithm HTTP/1.1
        Host: cb-manager.example.com
        Content-Type: application/json

        {
            "where": {
                "equals": {
                    "target:" "id",
                    "expr": "<algorithm-instance-id>"
                }
            }
        }

    :param id: optional algorithm instance id.

    :reqheader Authorization: JWT Authentication.
    :reqheader Content-Type: application/json

    :resheader Content-Type: application/json

    :status 205: All algorithm instances correctly deleted.
    :status 400: Request not valid.
    :status 401: Authentication failed.
    :status 404: Algorithm instances based on the request query not found.
    :status 406: Request validation failed.
    :status 415: Media type not supported.
    :status 422: Not possible to delete one or more algorithm instances based on the request query.
    :status 500: Server not available to satisfy the request.

    This request removes the algorithm instance with ``id`` = "<algorithm-instance-id>".

    This is a possible response:

    .. sourcecode:: http

        HTTP/1.1 205 Reset Content
        Content-Type: application/json

        [
            {
                "status": "Reset Content",
                "code": 200,
                "error": false,
                "message": "Algorithm instance the id=<algorithm-instance-id> correctly deleted"
            }
        ]

    .. caution::

        Without request body, it removes **all** the algorithm instances.


.. |JSON| replace:: :abbr:`JSON (JavaScript Object Notation)`
.. |REST| replace:: :abbr:`REST (Representational State Transfer)`
