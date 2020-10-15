.. CB-Manager documentation master file.

Welcome to CB-Manager documentation!
====================================

|CB|-Manager provides various |APIs| to interact with the Context Broker's database.
Through a |REST| Interface, it exposes data and events stored in the internal storage system in a structured way.
It provides uniform access to the capabilities of monitoring agents.

Compatibility
=============

|CB|-Manager requires Python 3.5+.


Documentation
=============

This part of the documentation will show you how to get started in using |CB|-Manager.

.. toctree::
   :maxdepth: 2
   :numbered:

   installation
   running
   exec-env
   exec-env-type
   network-link
   network-link-type
   connection
   data
   agent-catalog
   agent-instance
   ebpf-program-catalog
   ebpf-program-instance
   glossary


API Reference
-------------

If you are looking for information on a specific function, class or method, this part of the documentation is for you.

.. toctree::
   :maxdepth: 2

   api

Additional Notes
----------------

.. toctree::
   :maxdepth: 2

   contributing
   changelog


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. |APIs| replace:: :abbr:`APIs (Application Program Interfaces)`
.. |CB| replace:: :abbr:`CB (Context Broker)`
.. |REST| replace:: :abbr:`REST (Representational State Transfer)`
