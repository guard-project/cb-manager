.. _pipeline:

Pipeline
========

This index stores all the incoming pipelines.

Schema
------

+------------------------------+--------+----------+----------+--------------+-----------------------------+
| Field                        | Type   | Required | Readonly | Auto Managed | Example                     |
+=================+============+========+==========+==========+==============+=============================+
| ``id``                       | String | True     | True     | False        | dsalkasdioi232382yieyqwuiy  |
+------------------------------+--------+----------+----------+--------------+-----------------------------+
| ``updated_at``               | Date   | False    | False    | False        | 1617278285                  |
+------------------------------+--------+----------+----------+--------------+-----------------------------+
| ``created_at``               | Date   | True     | True     | False        | 1617278285                  |
+------------------------------+--------+----------+----------+--------------+-----------------------------+
| ``name``                     | String | False    | False    | False        | test pipeline guard-vdpi ud |
+------------------------------+--------+----------+----------+--------------+-----------------------------+
| ``status                     | String | True     | False    | False        | started                     |
+------------------------------+--------+----------+----------+--------------+-----------------------------+
| ``user``                     | String | False    | False    | False        | Minds & Sparks              |
+------------------------------+--------+----------+----------+--------------+-----------------------------+

.. warning::

    - It is not possible to update *readonly* fields.
    - it is not possible to set the *Auto managed* fields.

.. note::

    - ``id`` is required but it is auto-generated if not provided.
      It is recommended to provide a friendly for simplify the retrieve of connected date in other indices.


Create
------

To create a new pipeline use the following |REST| call:

.. http:post:: /pipeline/(string:id)

    with the request body in |JSON| format:

    .. sourcecode:: http

        POST /pipeline HTTP/1.1
        Host: cb-manager.example.com
        Content-Type: application/json

        {
            "id": "<pipeline-id>",
            "created_at": 1617278285,
            "updated_at": 1617278340,
            "name": "test pipeline guard-vdpi udt",
            "user": "Minds & Sparks",
            "status": "started"
        }

    :param id: optional pipeline id.

    :reqheader Authorization: JWT Authentication.
    :reqheader Content-Type: application/json

    :resheader Content-Type: application/json

    :status 201: Pipeline correctly created.
    :status 204: No content to create pipeline based on the request.
    :status 400: Request not valid.
    :status 401: Authentication failed.
    :status 406: Request validation failed.
    :status 415: Media type not supported.
    :status 422: Not possible to create ore or more pipelines based on the request.
    :status 500: Server not available to satisfy the request.

    Replace the data with the correct values, for example <pipeline-id> with ``alert-attack``.

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
                "message": "Pipeline with id=<pipeline-id> correctly created"
            }
        ]

    Otherwise, if, for example, an pipeline with the given ``id`` is already found, this is the response:

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

To get the list of pipelines:

.. http:get:: /pipeline/(string: id)

    The response includes all the pipelines created.

    It is possible to filter the results using the following request body:

    .. sourcecode:: http

        GET /pipeline HTTP/1.1
        Host: cb-manager.example.com
        Content-Type: application/json

        {
            "select": [ "id" ],
            "where": {
                "equals": {
                    "target:" "id",
                    "expr": "<pipeline-id>"
                }
            }
        }

    :param id: optional pipeline id.

    :reqheader Authorization: JWT Authentication.
    :reqheader Content-Type: application/json

    :resheader Content-Type: application/json

    :status 200: List of pipelines filtered by the query in the request body.
    :status 400: Request not valid.
    :status 401: Authentication failed.
    :status 404: Pipeline based on the request query not found.
    :status 406: Request validation failed.
    :status 415: Media type not supported.
    :status 422: Not possible to get pipelines with the request query.
    :status 500: Server not available to satisfy the request.

    In this way, it will be returned only the ``id`` of the pipeline with ``id`` = "<pipeline-id>".


Update
------

To update an pipeline, use:

.. http:put:: /pipeline/(string:id)

    .. sourcecode:: http

        PUT /pipeline HTTP/1.1
        Host: cb-manager.example.com
        Content-Type: application/json

        {
            "id": "<pipeline-id>",
            "source": "<ip-address>"
        }

    :param id: optional pipeline id.

    :reqheader Authorization: JWT Authentication.
    :reqheader Content-Type: application/json

    :resheader Content-Type: application/json

    :status 200: All pipelines correctly updated.
    :status 204: No content to update pipelines based on the request.
    :status 304: Update for one or more pipelines not necessary.
    :status 400: Request not valid.
    :status 401: Authentication failed.
    :status 406: Request validation failed.
    :status 415: Media type not supported.
    :status 422: Not possible to update one or more pipelines based on the request.
    :status 500: Server not available to satisfy the request.

    This example add a new field ``source`` for the pipeline with ``id`` = "<pipeline-id>".

    A possible response is:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json

        [
            {
                "status": "OK",
                "code": 200,
                "error": false,
                "message": "Pipeline with id=<pipeline-id> correctly updated"
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
                "message": "Update for pipeline with id=<pipeline-id> not necessary"
            }
        ]


Delete
------

To delete pipelines, use:

.. http:delete:: /pipeline/(string:id)

    .. sourcecode:: http

        DELETE /pipeline HTTP/1.1
        Host: cb-manager.example.com
        Content-Type: application/json

        {
            "where": {
                "equals": {
                    "target:" "id",
                    "expr": "<pipeline-id>"
                }
            }
        }

    :param id: optional pipeline id.

    :reqheader Authorization: JWT Authentication.
    :reqheader Content-Type: application/json

    :resheader Content-Type: application/json

    :status 205: All pipelines correctly deleted.
    :status 400: Request not valid.
    :status 401: Authentication failed.
    :status 404: Pipeline based on the request query not found.
    :status 406: Request validation failed.
    :status 415: Media type not supported.
    :status 422: Not possible to delete one or more pipelines based on the request query.
    :status 500: Server not available to satisfy the request.

    This request removes the pipeline with ``id`` = "<pipeline-id>".

    This is a possible response:

    .. sourcecode:: http

        HTTP/1.1 205 Reset Content
        Content-Type: application/json

        [
            {
                "status": "Reset Content",
                "code": 200,
                "error": false,
                "message": "Pipeline with id=<pipeline-id> correctly deleted"
            }
        ]

    .. caution::

        Without request body, it removes **all** the pipelines.


.. |JSON| replace:: :abbr:`JSON (JavaScript Object Notation)`
.. |REST| replace:: :abbr:`REST (Representational State Transfer)`
