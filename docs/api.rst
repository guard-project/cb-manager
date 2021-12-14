.. _api:


API
===

.. currentmodule:: api

.. autofunction:: api


Error Handler
-------------

.. currentmodule:: api.error_handler

.. autoclass:: BaseHandler
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: BadRequestHandler
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: InternalServerErrorHandler
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: UnsupportedMediaTypeHandler
    :members:_
    :private-members:
    :inherited-members:


Media Handler
-------------

.. currentmodule:: api.media_handler

.. autoclass:: XMLHandler
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: YAMLHandler
    :members:
    :private-members:
    :inherited-members:


Middleware
----------

.. currentmodule:: api.middleware

.. autoclass:: NegotiationMiddleware
    :members:
    :private-members:
    :inherited-members:


Spec
----

.. currentmodule:: api.spec

.. autoclass:: Spec
    :members:
    :private-members:
    :inherited-members:


Docstring
---------

.. currentmodule:: docstring

.. autodecorator:: docstring


Document
--------

.. currentmodule:: document.base

.. autoclass:: BaseDocument
    :members:
    :private-members:
    :inherited-members:


Agent
^^^^^

.. currentmodule:: document.agent.catalog

.. autoclass:: AgentCatalogDocument
    :members:
    :private-members:
    :inherited-members:

.. currentmodule:: document.agent.instance

.. autoclass:: AgentInstanceDocument
    :members:
    :private-members:
    :inherited-members:


eBPF Program
^^^^^^^^^^^^

.. currentmodule:: document.ebpf_program.catalog

.. autoclass:: eBPFProgramCatalogDocument
    :members:
    :private-members:
    :inherited-members:

.. currentmodule:: document.ebpf_program.instance

.. autoclass:: eBPFProgramInstanceDocument
    :members:
    :private-members:
    :inherited-members:


Connection
^^^^^^^^^^

.. currentmodule:: document.connection

.. autoclass:: ConnectionDocument
    :members:
    :private-members:
    :inherited-members:


Data
^^^^

.. currentmodule:: document.data

.. autoclass:: DataDocument
    :members:
    :private-members:
    :inherited-members:


Execution Environment
^^^^^^^^^^^^^^^^^^^^^

.. currentmodule:: document.exec_env

.. autoclass:: ExecEnvDocument
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: ExecEnvTypeDocument
    :members:
    :private-members:
    :inherited-members:


Network Link
^^^^^^^^^^^^

.. currentmodule:: document.NetworkLink

.. autoclass:: NetworkLinkDocument
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: NetworkLinkTypeDocument
    :members:
    :private-members:
    :inherited-members:

Lib
---

.. currentmodule:: lib.elasticsearch

.. autofunction:: connection

.. currentmodule:: lib.heartbeat

.. autofunction:: heartbeat

.. currentmodule:: lib.http

.. autoclass:: HTTPMethod
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: HTTPStatus
    :members:
    :private-members:
    :inherited-members:

.. currentmodule:: lib.token

.. autofunction:: create_token

Response
--------

.. currentmodule:: lib.response

.. autoclass:: BaseResponse
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: BadRequestResponse
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: ConflictResponse
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: ContentResponse
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: CreatedResponse
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: InternalServerErrorResponse
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: NoContentResponse
    :members:
    :private-members:TypeDocument
    :inherited-members:

.. autoclass:: NotAcceptableResponse
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: NotFoundResponse
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: NotModifiedResponse
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: OkResponse
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: ResetContentResponse
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: UnauthorizedResponse
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: UnprocessableEntityResponse
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: UnsupportedMediaTypeResponse
    :members:
    :private-members:
    :inherited-members:


Reader
------

.. currentmodule:: reader.arg

.. autoclass:: ArgReader
    :members:
    :private-members:
    :inherited-members:TypeDocument
.. currentmodule:: reader.config

.. autoclass:: ConfigReader
    :members:
    :private-members:
    :inherited-members:

.. currentmodule:: reader.query

.. autoclass:: QueryReader
    :members:
    :private-members:
    :inherited-members:


Resource
--------

.. currentmodule:: resource

.. autofunction:: routes

.. currentmodule:: resource.base

.. autoclass:: BaseResource
    :members:
    :private-members:
    :inherited-members:

.. currentmodule:: resource.base.handler.lcp

.. autoclass:: LCP
    :members:
    :private-members:
    :inherited-members:


Agent
^^^^^

.. currentmodule:: resource.agent.catalog

.. autoclass:: AgentCatalogResource
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: AgentCatalogSelectedResource
    :members:
    :private-members:
    :inherited-members:

.. currentmodule:: resource.agent.instance

.. autoclass:: AgentInstanceResource
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: AgentInstanceSelectedResource
    :members:
    :private-members:
    :inherited-members:

.. currentmodule:: resource.agent.handler.lcp

.. autoclass:: LCP
    :members:
    :private-members:
    :inherited-members:


eBPF Program
^^^^^^^^^^^^

.. currentmodule:: resource.ebpf_program.catalog

.. autoclass:: eBPFProgramCatalogResource
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: eBPFProgramCatalogSelectedResource
    :members:
    :private-members:
    :inherited-members:

.. currentmodule:: resource.ebpf_program.instance

.. autoclass:: eBPFProgramInstanceResource
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: eBPFProgramInstanceSelectedResource
    :members:
    :private-members:
    :inherited-members:

.. currentmodule:: resource.ebpf_program.handler.lcp

.. autoclass:: LCP
    :members:
    :private-members:
    :inherited-members:


Execution Environment
^^^^^^^^^^^^^^^^^^^^^

.. currentmodule:: resource.exec_env

.. autoclass:: ExecEnvResource
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: ExecEnvSelectedResource
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: ExecEnvTypeResource
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: ExecEnvTypeSelectedResource
    :members:
    :private-members:
    :inherited-members:


Network Link
^^^^^^^^^^^^

.. currentmodule:: resource.NetworkLink

.. autoclass:: NetworkLinkResource
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: NetworkLinkSelectedResource
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: NetworkLinkTypeResource
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: NetworkLinkTypeSelectedResource
    :members:
    :private-members:
    :inherited-members:


Connection
^^^^^^^^^^

.. currentmodule:: resource.connection

.. autoclass:: ConnectionResource
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: ConnectionSelectedResource
    :members:
    :private-members:
    :inherited-members:


Data
^^^^

.. currentmodule:: resource.data

.. autoclass:: DataResource
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: DataSelectedResource
    :members:
    :private-members:
    :inherited-members:


Schema
------

.. currentmodule:: schema.validate

.. autoclass:: In
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: UniqueList
    :members:
    :private-members:
    :inherited-members:

.. currentmodule:: schema.base

.. autoclass:: BaseSchema
    :members:
    :private-members:
    :inherited-members:


Agent
^^^^^

Catalog
"""""""

.. currentmodule:: schema.agent.catalog

.. autoclass:: AgentCatalogSchema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: AgentCatalogActionSchema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: AgentCatalogActionConfigSchema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: AgentCatalogParameterSchema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: AgentCatalogParameterConfigSchema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: AgentCatalogResourceSchema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: AgentCatalogResourceConfigSchema
    :members:
    :private-members:
    :inherited-members:


Instance
""""""""

.. currentmodule:: schema.agent.instance

.. autoclass:: AgentInstanceSchema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: AgentInstanceOperationSchema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: AgentInstanceActionSchema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: AgentInstanceParameterSchema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: AgentInstanceResourceSchema
    :members:
    :private-members:
    :inherited-members:


eBPF Program
^^^^^^^^^^^^

Catalog
"""""""

.. currentmodule:: schema.ebpf_program.catalog

.. autoclass:: eBPFProgramCatalogSchema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: eBPFProgramCatalogParameterSchema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: eBPFProgramCatalogConfigSchema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: eBPFProgramCatalogConfigMetricSchema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: eBPFProgramCatalogConfigMetricOpenMetricsMetadataSchema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: eBPFProgramCatalogConfigMetricOpenMetricsMetadataLabelSchema
    :members:
    :private-members:
    :inherited-members:


Instance
""""""""

.. currentmodule:: schema.ebpf_program.instance

.. autoclass:: eBPFProgramInstanceSchema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: eBPFProgramInstanceParameterSchema
    :members:
    :private-members:
    :inherited-members:


Execution Environment
^^^^^^^^^^^^^^^^^^^^^

.. currentmodule:: schema.exec_env

.. autoclass:: LCPSchema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: ExecEnvSchema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: ExecEnvTypeSchema
    :members:
    :private-members:
    :inherited-members:


Network Link
^^^^^^^^^^^^

.. currentmodule:: schema.NetworkLink

.. autoclass:: NetworkLinkSchema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: NetworkLinkTypeSchema
    :members:
    :private-members:
    :inherited-members:


Connection
^^^^^^^^^^

.. currentmodule:: schema.connection

.. autoclass:: ConnectionSchema
    :members:
    :private-members:
    :inherited-members:

.. currentmodule:: schema.data


Data
^^^^

.. autoclass:: DataSchema
    :members:
    :private-members:
    :inherited-members:


Query Request
^^^^^^^^^^^^^

.. currentmodule:: schema.queryRequest

.. autoclass:: QueryRequestSchema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: QueryRequestOrderSchema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: QueryRequestLimitSchema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: QueryRequestFilterSchema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: QueryRequestClauseSchema
    :members:
    :private-members:
    :inherited-members:


Response
^^^^^^^^

.. currentmodule:: schema.response

.. autoclass:: ExceptionResponseSchema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: BaseResponseSchema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: BadRequestResponseSchema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: ConflictResponseSchema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: ContentResponseSchema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: CreatedResponseSchema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: NoContentResponseSchema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: NotAcceptableResponseSchema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: NotFoundResponseSchema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: NotModifiedResponseSchema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: OkResponseSchema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: ResetContentResponseSchema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: UnauthorizedResponseSchema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: UnprocessableEntityResponseSchema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: UnsupportedMediaTypeResponseSchema
    :members:
    :inherited-members:
    :private-members:


Utils
-----

Datetime
^^^^^^^^

.. currentmodule:: utils.datetime

.. autodata:: FORMAT

.. autofunction:: datetime_from_str

.. autofunction:: datetime_to_str


Exception
^^^^^^^^^

.. currentmodule:: utils.exception

.. autofunction:: extract_info

.. autofunction:: to_str


JSON
^^^^

.. currentmodule:: utils.json

.. autofunction:: dumps

.. autofunction:: loads


Log
^^^

.. currentmodule:: utils.log

.. autoclass:: Log
    :members:
    :private-members:
    :inherited-members:


Sequence
^^^^^^^^

.. currentmodule:: utils.sequence

.. autofunction:: expand

.. autofunction:: format

.. autofunction:: is_dict

.. autofunction:: is_list

.. autofunction:: iterate

.. autofunction:: subset

.. autofunction:: table_to_dict

.. autofunction:: wrap


Signal
^^^^^^

.. currentmodule:: utils.signal

.. autofunction:: send_tree


String
^^^^^^

.. currentmodule:: utils.string

.. autoclass:: Formatter
    :members:
    :private-members:
    :inherited-members:

.. autofunction:: is_str

.. autodata:: format


Time
^^^^

.. currentmodule:: utils.time

.. autofunction:: get_seconds
