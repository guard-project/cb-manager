.. _chain:

Chain
=====

The chain represent a group of :ref:`exec-env`, :ref:`network-link`, :ref:`connection`, and :ref:`agent-instance` that are logically connected.

Delete
------

To delete chain, use:

.. http:delete:: /chain/(string:id)

    .. sourcecode:: http

        DELETE /data HTTP/1.1
        Host: cb-manager.example.com
        Content-Type: application/json

    :param id: required id for the root execution environment of the chain.

    :reqheader Authorization: |JWT| Authentication.

    :resheader Content-Type: application/json

    :status 400: Request not valid.
    :status 401: Authentication failed.


.. |JSON| replace:: :abbr:`JSON (JavaScript Object Notation)`
.. |JWT| replace:: :abbr:`JWT (|JSON| Web Token)`
.. |REST| replace:: :abbr:`REST (Representational State Transfer)`
