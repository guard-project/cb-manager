.. _algorithm-catalog:

Algorithm Catalog
=================

Contains the available algorithms.


Schema
------

+-----------------+-----------------+----------+----------+--------------+-----------------+
| Field           | Type            | Required | Readonly | Auto Managed | Example         |
+=================+=================+==========+==========+==============+=================+
| ``id``          | String          | True     | True     | False        | ddos-predictor  |
+-----------------+-----------------+----------+----------+--------------+-----------------+
| ``parameters``  | List(Parameter) | False    | False    | False        |                 |
+-----------------+-----------------+----------+----------+--------------+-----------------+
| ``description`` | String          | False    | False    | False        | DDoS predictor. |
+-----------------+-----------------+----------+----------+--------------+-----------------+


Parameter Schema
----------------

+-----------------+-------------------+----------+----------+--------------+--------------------------------+
| Field           | Type              | Required | Readonly | Auto Managed | Example                        |
+=================+===================+==========+==========+==============+================================+
| ``id``          | String            | True     | True     | False        | frequency                      |
+-----------------+-------------------+----------+----------+--------------+--------------------------------+
| ``type``        | Enum(String) [1]_ | True     | False    | False        | integer                        |
+-----------------+-------------------+----------+----------+--------------+--------------------------------+
| ``list``        | Boolean           | False    | False    | False        | False                          |
+-----------------+-------------------+----------+----------+--------------+--------------------------------+
| ``values``      | Enum(String)      | False    | False    | False        | mysql                          |
+-----------------+-------------------+----------+----------+--------------+--------------------------------+
| ``description`` | String            | False    | False    | False        | Frequency to scan the network. |
+-----------------+-------------------+----------+----------+--------------+--------------------------------+
| ``example``     | String            | False    | False    | False        | 10s                            |
+-----------------+-------------------+----------+----------+--------------+--------------------------------+

.. [1] Possible values are "integer", "number", "time-duration", "string", "choice", "boolean", and "binary".


.. warning::

    - It is not possible to update *readonly* fields.
    - it is not possible to set the *Auto managed* fields.

.. note::

    - ``id`` is required but it is auto-generated if not provided.
      It is recommended to provide a friendly for simplify the retrieve of connected date in other indices.


Create
------

To create a new algorithm in the catalog use the following |REST| call:

.. http:post:: /catalog/algorithm/(string:id)

    with the request body in |JSON| format:

    .. sourcecode:: http

        POST /catalog/algorithm HTTP/1.1
        Host: cb-manager.example.com
        Content-Type: application/json

        {
            "id": "<algorithm-id>",
            "parameters": [
                {
                    "id": "<parameter-id>",
                    "type": "<parameter-type>",
                    "description": "<parameter-human-readable-description>",
                    "example": "<parameter-example>",
                }
            ]
        }

    :param id: optional algorithm id.

    :reqheader Authorization: JWT Authentication.
    :reqheader Content-Type: application/json

    :resheader Content-Type: application/json

    :status 201: Algorithms correctly created.
    :status 204: No content to create algorithms for the catalog based on the request.
    :status 400: Request not valid.
    :status 401: Authentication failed.
    :status 406: Request validation failed.
    :status 415: Media type not supported.
    :status 422: Not possible to create ore or more algorithms for the catalog based on the request.
    :status 500: Server not available to satisfy the request.

    Replace the data with the correct values, for example <algorithm-id> with ``ddos-predictor``.

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
                "message": "Algorithm catalog with id=<algorithm-id> correctly created"
            }
        ]

    Otherwise, if, for example, an algorithm with the given ``id`` is already found in the catalog, this is the response:

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

To get the list of the algorithms available in the catalog:

.. http:get:: /catalog/algorithm/(string: id)

    The response includes all the algorithms.

    It is possible to filter the results using the following request body:

    .. sourcecode:: http

        GET /catalog/algorithm HTTP/1.1
        Host: cb-manager.example.com
        Content-Type: application/json

        {
            "select": [ "parameters" ],
            "where": {
                "equals": {
                    "target:" "id",
                    "expr": "<algorithm-id>"
                }
            }
        }

    :param id: optional algorithm id from the catalog.

    :reqheader Authorization: JWT Authentication.
    :reqheader Content-Type: application/json

    :resheader Content-Type: application/json

    :status 200: List of algorithms from the catalog filtered by the query in the request body.
    :status 400: Request not valid.
    :status 401: Authentication failed.
    :status 404: Data based on the request query not found.
    :status 406: Request validation failed.
    :status 415: Media type not supported.
    :status 422: Not possible to get algorithms from the catalog with the request query.
    :status 500: Server not available to satisfy the request.

    In this way, it will be returned only the ``parameters`` of the algorithm in the catalog with ``id`` = "<algorithm-id>".


Update
------

To update an algorithm in the catalog, use:

.. http:put:: /catalog/algorithm/(string:id)

    .. sourcecode:: http

        PUT /catalog/algorithm HTTP/1.1
        Host: cb-manager.example.com
        Content-Type: application/json

        {
            "id": "<algorithm-id>",
            "parameters": [
                {
                    "id": "<parameter-id>",
                    "type": "<new-parameter-type>"
                }
            ]
        }

    :param id: optional algorithm id.

    :reqheader Authorization: JWT Authentication.
    :reqheader Content-Type: application/json

    :resheader Content-Type: application/json

    :status 200: All algorithms in the catalog correctly updated.
    :status 204: No content to update algorithms in the catalog based on the request.
    :status 304: Update for one or more algorithms in the catalog not necessary.
    :status 400: Request not valid.
    :status 401: Authentication failed.
    :status 406: Request validation failed.
    :status 415: Media type not supported.
    :status 422: Not possible to update one or more algorithms in the catalog based on the request.
    :status 500: Server not available to satisfy the request.

    This example

    1. updates the new ``type`` of the ``parameter`` with ``id`` = "<parameter-id>";
    2. adds a new action

    of the algorithm with ``id`` = "<algorithm-id>".

    .. note:

        Also during the update it is possible to add additional data (not related to actions or parameters) for the specific algorithm.

    A possible response is:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json

        [
            {
                "status": "OK",
                "code": 200,
                "error": false,
                "message": "Algorithm catalog with id=<algorithm-id> correctly updated"
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
                "message": "Update for algorithm catalog with id=<algorithm-id> not necessary"
            }
        ]


Delete
------

To delete algorithms from the catalog, use:

.. http:delete:: /catalog/algorithm/(string:id)

    .. sourcecode:: http

        DELETE /catalog/algorithm HTTP/1.1
        Host: cb-manager.example.com
        Content-Type: application/json

        {
            "where": {
                "equals": {
                    "target:" "id",
                    "expr": "<algorithm-id>"
                }
            }
        }

    :param id: optional algorithm id from the catalog.

    :reqheader Authorization: JWT Authentication.
    :reqheader Content-Type: application/json

    :resheader Content-Type: application/json

    :status 205: All algorithms correctly deleted from the catalog.
    :status 400: Request not valid.
    :status 401: Authentication failed.
    :status 404: Algorithms based on the request query not found in the catalog.
    :status 406: Request validation failed.
    :status 415: Media type not supported.
    :status 422: Not possible to delete one or more algorithms from the catalog based on the request query.
    :status 500: Server not available to satisfy the request.

    This request removes from the catalog the algorithm with ``id`` = "<algorithm-id>".

    This is a possible response:

    .. sourcecode:: http

        HTTP/1.1 205 Reset Content
        Content-Type: application/json

        [
            {
                "status": "Reset Content",
                "code": 200,
                "error": false,
                "message": "Algorithm catalog the id=<algorithm-id> correctly deleted"
            }
        ]

    .. caution::

        Without request body, it removes **all** the algorithms from the catalog.


.. |JSON| replace:: :abbr:`JSON (JavaScript Object Notation)`
.. |REST| replace:: :abbr:`REST (Representational State Transfer)`
