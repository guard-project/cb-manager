.. _api:


API
===

.. currentmodule:: api

.. autofunction:: api


Error Handler
-------------

.. currentmodule:: api.error_handler

.. autoclass:: Base_Handler
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Bad_Request_Handler
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Internal_Server_Error_Handler
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Unsupported_Media_Type_Handler
    :members:
    :private-members:
    :inherited-members:


Media Handler
-------------

.. currentmodule:: api.media_handler

.. autoclass:: XML_Handler
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: YAML_Handler
    :members:
    :private-members:
    :inherited-members:


Middleware
----------

.. currentmodule:: api.middleware

.. autoclass:: Basic_Auth_Backend_Middleware
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Negotiation_Middleware
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

.. autoclass:: Base_Document
    :members:
    :private-members:
    :inherited-members:


Agent
^^^^^

.. currentmodule:: document.agent.catalog

.. autoclass:: Agent_Catalog_Document
    :members:
    :private-members:
    :inherited-members:

.. currentmodule:: document.agent.instance

.. autoclass:: Agent_Instance_Document
    :members:
    :private-members:
    :inherited-members:


eBPF Program
^^^^^^^^^^^^

.. currentmodule:: document.ebpf_program.catalog

.. autoclass:: eBPF_Program_Catalog_Document
    :members:
    :private-members:
    :inherited-members:

.. currentmodule:: document.ebpf_program.instance

.. autoclass:: eBPF_Program_Instance_Document
    :members:
    :private-members:
    :inherited-members:


Connection
^^^^^^^^^^

.. currentmodule:: document.connection

.. autoclass:: Connection_Document
    :members:
    :private-members:
    :inherited-members:


Data
^^^^

.. currentmodule:: document.data

.. autoclass:: Data_Document
    :members:
    :private-members:
    :inherited-members:


Execution Environment
^^^^^^^^^^^^^^^^^^^^^

.. currentmodule:: document.exec_env

.. autoclass:: Exec_Env_Document
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Exec_Env_Type_Document
    :members:
    :private-members:
    :inherited-members:


Network Link
^^^^^^^^^^^^

.. currentmodule:: document.network_link

.. autoclass:: Network_Link_Document
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Network_Link_Type_Document
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

.. autoclass:: HTTP_Method
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: HTTP_Status
    :members:
    :private-members:
    :inherited-members:


Response
--------

.. currentmodule:: lib.response

.. autoclass:: Base_Response
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Bad_Request_Response
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Conflict_Response
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Content_Response
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Created_Response
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Internal_Server_Error_Response
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: No_Content_Response
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Not_Acceptable_Response
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Not_Found_Response
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Not_Modified_Response
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Ok_Response
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Reset_Content_Response
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Unauthorized_Response
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Unprocessable_Entity_Response
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Unsupported_Media_Type_Response
    :members:
    :private-members:
    :inherited-members:


Reader
------

.. currentmodule:: reader.arg

.. autoclass:: Arg_Reader
    :members:
    :private-members:
    :inherited-members:

.. currentmodule:: reader.config

.. autoclass:: Config_Reader
    :members:
    :private-members:
    :inherited-members:

.. currentmodule:: reader.query

.. autoclass:: Query_Reader
    :members:
    :private-members:
    :inherited-members:


Resource
--------

.. currentmodule:: resource

.. autofunction:: routes

.. currentmodule:: resource.base

.. autoclass:: Base_Resource
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

.. autoclass:: Agent_Catalog_Resource
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Agent_Catalog_Selected_Resource
    :members:
    :private-members:
    :inherited-members:

.. currentmodule:: resource.agent.instance

.. autoclass:: Agent_Instance_Resource
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Agent_Instance_Selected_Resource
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

.. autoclass:: eBPF_Program_Catalog_Resource
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: eBPF_Program_Catalog_Selected_Resource
    :members:
    :private-members:
    :inherited-members:

.. currentmodule:: resource.ebpf_program.instance

.. autoclass:: eBPF_Program_Instance_Resource
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: eBPF_Program_Instance_Selected_Resource
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

.. autoclass:: Exec_Env_Resource
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Exec_Env_Selected_Resource
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Exec_Env_Type_Resource
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Exec_Env_Type_Selected_Resource
    :members:
    :private-members:
    :inherited-members:


Network Link
^^^^^^^^^^^^

.. currentmodule:: resource.network_link

.. autoclass:: Network_Link_Resource
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Network_Link_Selected_Resource
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Network_Link_Type_Resource
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Network_Link_Type_Selected_Resource
    :members:
    :private-members:
    :inherited-members:


Connection
^^^^^^^^^^

.. currentmodule:: resource.connection

.. autoclass:: Connection_Resource
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Connection_Selected_Resource
    :members:
    :private-members:
    :inherited-members:


Data
^^^^

.. currentmodule:: resource.data

.. autoclass:: Data_Resource
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Data_Selected_Resource
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

.. autoclass:: Unique_List
    :members:
    :private-members:
    :inherited-members:

.. currentmodule:: schema.base

.. autoclass:: Base_Schema
    :members:
    :private-members:
    :inherited-members:


Agent
^^^^^

Catalog
"""""""

.. currentmodule:: schema.agent.catalog

.. autoclass:: Agent_Catalog_Schema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Agent_Catalog_Action_Schema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Agent_Catalog_Action_Config_Schema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Agent_Catalog_Parameter_Schema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Agent_Catalog_Parameter_Config_Schema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Agent_Catalog_Resource_Schema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Agent_Catalog_Resource_Config_Schema
    :members:
    :private-members:
    :inherited-members:


Instance
""""""""

.. currentmodule:: schema.agent.instance

.. autoclass:: Agent_Instance_Schema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Agent_Instance_Operation_Schema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Agent_Instance_Action_Schema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Agent_Instance_Parameter_Schema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Agent_Instance_Resource_Schema
    :members:
    :private-members:
    :inherited-members:


eBPF Program
^^^^^^^^^^^^

Catalog
"""""""

.. currentmodule:: schema.ebpf_program.catalog

.. autoclass:: eBPF_Program_Catalog_Schema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: eBPF_Program_Catalog_Parameter_Schema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: eBPF_Program_Catalog_Config_Schema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: eBPF_Program_Catalog_Config_Metric_Schema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: eBPF_Program_Catalog_Config_Metric_Open_Metrics_Metadata_Schema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: eBPF_Program_Catalog_Config_Metric_Open_Metrics_Metadata_Label_Schema
    :members:
    :private-members:
    :inherited-members:


Instance
""""""""

.. currentmodule:: schema.ebpf_program.instance

.. autoclass:: eBPF_Program_Instance_Schema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: eBPF_Program_Instance_Parameter_Schema
    :members:
    :private-members:
    :inherited-members:


Execution Environment
^^^^^^^^^^^^^^^^^^^^^

.. currentmodule:: schema.exec_env

.. autoclass:: LCP_Schema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Exec_Env_Schema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Exec_Env_Type_Schema
    :members:
    :private-members:
    :inherited-members:


Network Link
^^^^^^^^^^^^

.. currentmodule:: schema.network_link

.. autoclass:: Network_Link_Schema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Network_Link_Type_Schema
    :members:
    :private-members:
    :inherited-members:


Connection
^^^^^^^^^^

.. currentmodule:: schema.connection

.. autoclass:: Connection_Schema
    :members:
    :private-members:
    :inherited-members:

.. currentmodule:: schema.data


Data
^^^^

.. autoclass:: Data_Schema
    :members:
    :private-members:
    :inherited-members:


Query Request
^^^^^^^^^^^^^

.. currentmodule:: schema.query_request

.. autoclass:: Query_Request_Schema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Query_Request_Order_Schema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Query_Request_Limit_Schema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Query_Request_Filter_Schema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Query_Request_Clause_Schema
    :members:
    :private-members:
    :inherited-members:


Response
^^^^^^^^

.. currentmodule:: schema.response

.. autoclass:: Exception_Response_Schema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Base_Response_Schema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Bad_Request_Response_Schema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Conflict_Response_Schema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Content_Response_Schema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Created_Response_Schema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: No_Content_Response_Schema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Not_Acceptable_Response_Schema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Not_Found_Response_Schema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Not_Modified_Response_Schema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Ok_Response_Schema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Reset_Content_Response_Schema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Unauthorized_Response_Schema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Unprocessable_Entity_Response_Schema
    :members:
    :private-members:
    :inherited-members:

.. autoclass:: Unsupported_Media_Type_Response_Schema
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

.. autofunction:: reload_import

.. autofunction:: to_str


Hash
^^^^

.. currentmodule:: utils.hash

.. autofunction:: hash

.. autofunction:: generate_username

.. autofunction:: generate_password


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
