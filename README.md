---
title: Context Broker Manager
---

- [Data Model](#data-model)
- [Methods](#methods)
  - [Exec\_Env](#exec_env)
    - [Exec\_Env Type](#exec_env-type)
  - [Network link](#network-link)
    - [Network link Type](#network-link-type)
  - [Connection](#connection)
  - [Agent](#agent)
    - [Catalog](#catalog)
    - [Instance](#instance)
  - [eBPF Program](#ebpf-program)
    - [Catalog](#catalog-1)
    - [Instance](#instance-1)
  - [Data](#data)
- [Guide](#guide)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [Display help](#display-help)
- [Glossary](#glossary)
- [References](#references)

[![MIT License](https://img.shields.io/github/license/guard-project/cb-manager)](https://github.com/guard-project/cb-manager/-/blob/master/LICENSE)

[![GitHub Code Size](https://img.shields.io/github/languages/code-size/guard-project/cb-manager?color=red&logo=github)](https://github.com/guard-project/cb-manager)

[![GitHub Repository Size](https://img.shields.io/github/repo-size/guard-project/cb-manager?color=red&logo=github)](https://github.com/guard-project/cb-manager)

[![GitJHub Release](https://img.shields.io/github/v/tag/guard-project/cb-manager?label=release&logo=github)](https://github.com/guard-project/cb-manager/releases)

[![CII Progress](https://img.shields.io/cii/summary/3991)](https://bestpractices.coreinfrastructure.org/en/projects/3991)

[![Readthedocs](https://readthedocs.org/projects/cb-manager/badge/?version=latest)](https://cb-manager.readthedocs.io)

[![PyUP](https://pyup.io/repos/github/guard-project/cb-manager/shield.svg)](https://pyup.io/repos/github/guard-project/cb-manager/)

[![Python 3991](https://pyup.io/repos/github/guard-project/cb-manager/python-3-shield.svg)](https://pyup.io/repos/github/guard-project/cb-manager/)

[![Travis CI](https://travis-ci.org/guard-project/cp-manager.svg?branch=master)](https://travis-ci.org/guard-project/cb-manager)

APIs to interact with the `Context Broker`\'s database. Through a
`REST (Representational State Transfer)`{.interpreted-text role="abbr"}
Interface, it exposes data and events stored in the internal storage
system in a structured way. It provides uniform access to the
capabilities of monitoring agents.

::: {.toctree maxdepth="2" numbered=""}
:::

Data Model
==========

![image](data_model.png)

Each table in the figure represents an **index** in the Elastic
nomenclature. Considering the **NoSQL** nature of the Elasticsearch
engine for each document of any indices it is possible to add additional
properties. The schema is not static and defined at priori, but it is
dynamic allowing the possibility to add custom properties for a specific
document. Elastic requires the name of the index in a lower-case format.
For this reason, all the index names follow the *dash-case*[^1] format.
Instead, each property[^2] follows the *snake-case*[^3] format. All the
properties marked with an asterisk (\*) are required by the
`APIs (Application Program Interfaces)`{.interpreted-text role="abbr"}
in order to make the POST request (i.e. to create a new resource, for
example an Exec\_Env). Instead the ones underlined are identifies the
specific resource (aka document in Elastic nomenclature or record in
traditional `DB (DataBase)`{.interpreted-text role="abbr"} one) and must
be unique. The `data` index contains the all the data collected from the
Exec\_Envs by means of the agent[^4].

The common attributes are:

1.  `id` (unique identifier)[^5];
2.  `id` of the source Exec\_Env (`exec_env_id`); and
3.  `id` of the agent instance that collect the data
    (`agent_instance_id`).

The `id` property type accepts only lower-case values without space that
start with an alphabetic character, e.g: apache is valid but not Apache.
Then, the other two properties are related to the time-stamp:

1.  `timestamp_event` when event is occurred; and
2.  `timestamp_agent` when the agent instance collect the data.

With the term agent instance, we refer to a specific agent installed in
the Exec\_Env.

The `exec-env` index contains the `hostname` of the remote host where is
it allocated and the `type_id` field that correspond a specified type of
Exec\_Env. The different type of Exec\_Env are defined with the index
`exec-env-type`. Currently, the available ones are: *i*) *Virtual
Machine* and *ii*) *Container*. Obviously, it is possible to add other
types depending on the specific requirements.

The `agent-catalog` index contains specific information related to the
agents, and in particular the Beats of the Elastic stack and eBPF-based
services deployed with the **Polycube** framework. For a detailed
description of these properties see[^6] and[^7].

Each agent in the catalog is characterized by one or more options. The
options are defined with the [agent-option]{.title-ref}
*nested-index*[^8]. This index described the option in terms of name and
relative type. At this moment, the supported types are:

-   *integer* (e.g. 1, 2, etc.);
-   *number* (e..g 1, 2.3, etc.);
-   *time-duration* (e.g. 1s, 2m, 3h, etc.);
-   *string*; *choice*, *obj*, and *boolean* (i.e. true or false).

There two additional (and optional) properties: *list* and *values*. The
first one indicate if the option is a list or not (default value:
false); while the latter one described the data in the case the type is
choice or obj. To accept different types, the values property can be of
any type.

All the data of the installed agent is stored in the `agent-instance`
index. This index contains the options got from the catalog with the
actual values. In addition, it includes the `id` of the Exec\_Env where
the agent is installed (`exec_env_id`) and the current *status* in terms
of *started* or *stopped*.

The network links are defined with the relative index where it is
indicate the type. All the possible network link types are defined in
the `network-link-type` index. At the moment, the possible types are:
*Point to Point* (Point 2 Point), *Multi-point*, and *Slice*. Similar to
the Exec\_Env case, also for the network link, it is possible to add
additional types depending on specific needs.

In addition, the data model allow to see the status of the connections
between the Exec\_Envs. The `connection` index couples the Exec\_Env and
the network link to which it belongs. This index should contains all the
information regarding the network link and the Exec\_Env as, for
example, the `IP (Internet Protocol)`{.interpreted-text role="abbr"}
address (version 4 and/or 6) or if the link is encrypted and how (which
method, etc.).

The `software` index contains the installed software with relative
properties. Each software record is referred to a specific Exec\_Env
that indicate where the software is installed. This part is out of scope
of the
`GUARD (GUArantee Reliability and trust for Digital service chains)`{.interpreted-text
role="abbr"} project context and, for this reason, it is this
highlighted with a dashed box. The
`APIs (Application Program Interface)`{.interpreted-text role="abbr"}
implementation does not consider this index. Nervelessness, it
represents a typical solution for various common cases. The proposed
data model allows the customization with the integration of additional
entities in very simple way.

Methods
=======

Exec\_Env
---------

+---------+---------------+-------------------------------------------+
| `HTTP ( | Path          | Action                                    |
| HyperTe |               |                                           |
| xt Tran |               |                                           |
| sfer Pr |               |                                           |
| otocol) |               |                                           |
| `{.inte |               |                                           |
| rpreted |               |                                           |
| -text   |               |                                           |
| role="a |               |                                           |
| bbr"}   |               |                                           |
| Method  |               |                                           |
+=========+===============+===========================================+
| GET     | > /exec-env   | > Returns the Exec\_Envs selected by the  |
|         |               | > query in the request body (or all it    |
| > -     | \-\-\-\-\-\-\ | > the request body is empty).             |
|         | -\-\-\-\-\-\- |                                           |
|         | \-\-\-\-\-\-\ | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\ |
|         | -\-\--+       | -\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|         |               | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\ |
|         | :   /exec-env | -\-\--+                                   |
|         | /(string:id)  |                                           |
|         |               | :   Returns the Exec\_Env selected by the |
|         |               |     given `id` and the query in the       |
|         |               |     request body.                         |
+---------+---------------+-------------------------------------------+
| POST    | > /exec-env   | > Create one or more new Exec\_Envs.      |
|         |               |                                           |
| :   -   | \-\-\-\-\-\-\ | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\ |
|         | -\-\-\-\-\-\- | -\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|         | \-\-\-\-\-\-\ | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\ |
|         | -\-\--+       | -\-\--+                                   |
|         |               |                                           |
|         | :   /exec-env | :   Create a new Exec\_Env with the given |
|         | /(string:id)  |     `id`.                                 |
+---------+---------------+-------------------------------------------+
| PUT     | > /exec-env   | > Update one or more existing Exec\_Envs. |
|         |               |                                           |
| :   -   | \-\-\-\-\-\-\ | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\ |
|         | -\-\-\-\-\-\- | -\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|         | \-\-\-\-\-\-\ | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\ |
|         | -\-\--+       | -\-\--+                                   |
|         |               |                                           |
|         | :   /exec-env | :   Update the Exec\_Env with given `id`. |
|         | /(string:id)  |                                           |
+---------+---------------+-------------------------------------------+
| DELETE  | > /exec-env   | > Delete the Exec\_Envs selected by the   |
|         |               | > query in the request body (or all it    |
| > -     | \-\-\-\-\-\-\ | > the request body is empty).             |
|         | -\-\-\-\-\-\- |                                           |
|         | \-\-\-\-\-\-\ | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\ |
|         | -\-\--+       | -\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|         |               | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\ |
|         | :   /exec-env | -\-\--+                                   |
|         | /(string:id)  |                                           |
|         |               | :   Delete the Exec\_Env selected by the  |
|         |               |     given `id` and the query in the       |
|         |               |     request body.                         |
+---------+---------------+-------------------------------------------+

### Exec\_Env Type

+--------+-----------------+-------------------------------------------+
| `HTTP  | Path            | Action                                    |
| (Hyper |                 |                                           |
| Text T |                 |                                           |
| ransfe |                 |                                           |
| r Prot |                 |                                           |
| ocol)` |                 |                                           |
| {.inte |                 |                                           |
| rprete |                 |                                           |
| d-text |                 |                                           |
| role=" |                 |                                           |
| abbr"} |                 |                                           |
| Method |                 |                                           |
+========+=================+===========================================+
| GET    | > /type/exec-en | > Returns the Exec\_Env types selected by |
|        | v               | > the query in the request body (or all   |
| > -    |                 | > it the request body is empty).          |
|        | \-\-\-\-\-\-\-\ |                                           |
|        | -\-\-\-\-\-\-\- | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\ |
|        | \-\-\-\-\-\-\-\ | -\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|        | -\-\-\-\--+     | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\ |
|        |                 | -\-\-\-\-\-\-\--+                         |
|        | :   /type/exec- |                                           |
|        | env/(string:id) | :   Returns the Exec\_Env type selected   |
|        |                 |     by the given `id` and the query in    |
|        |                 |     the request body.                     |
+--------+-----------------+-------------------------------------------+
| POST   | > /type/exec-en | > Create one or more new Exec\_Env types. |
|        | v               |                                           |
| :   -  |                 | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\ |
|        | \-\-\-\-\-\-\-\ | -\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|        | -\-\-\-\-\-\-\- | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\ |
|        | \-\-\-\-\-\-\-- | -\-\-\-\-\-\-\--+                         |
|        | +\-\-\-\--      |                                           |
|        | /type/exec-env/ | :   Create a new Exec\_Env with the given |
|        | (string:id)     |     `id`.                                 |
+--------+-----------------+-------------------------------------------+
| PUT    | > /type/exec-en | > Update one or more existing Exec\_Env   |
|        | v               | > types.                                  |
| :   -  |                 |                                           |
|        | \-\-\-\-\-\-\-\ | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\ |
|        | -\-\-\-\-\-\-\- | -\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|        | \-\-\-\-\-\-\-- | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\ |
|        | +\-\-\-\--      | -\-\-\-\-\-\-\--+                         |
|        | /type/exec-env/ |                                           |
|        | (string:id)     | :   Update the Exec\_Env type with given  |
|        |                 |     `id`.                                 |
+--------+-----------------+-------------------------------------------+
| DELETE | > /type/exec-en | > Delete the Exec\_Env types selected by  |
|        | v               | > the query in the request body (or all   |
| > -    |                 | > it the request body is empty).          |
|        | \-\-\-\-\-\-\-\ |                                           |
|        | -\-\-\-\-\-\-\- | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\ |
|        | \-\-\-\-\-\-\-- | -\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|        | +\-\-\-\--      | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\ |
|        | /type/exec-env/ | -\-\-\-\-\-\-\--+                         |
|        | (string:id)     |                                           |
|        |                 | :   Delete the Exec\_Env type selected by |
|        |                 |     the given `id` and the query in the   |
|        |                 |     request body.                         |
+--------+-----------------+-------------------------------------------+

Network link
------------

+---------+----------------+-------------------------------------------+
| `HTTP ( | Path           | Action                                    |
| HyperTe |                |                                           |
| xt Tran |                |                                           |
| sfer Pr |                |                                           |
| otocol) |                |                                           |
| `{.inte |                |                                           |
| rpreted |                |                                           |
| -text   |                |                                           |
| role="a |                |                                           |
| bbr"}   |                |                                           |
| Method  |                |                                           |
+=========+================+===========================================+
| GET     | > /network-lin | > Returns the network links selected by   |
|         | k              | > the query in the request body (or all   |
| > -     |                | > it the request body is empty).          |
|         | \-\-\-\-\-\-\- |                                           |
|         | \-\-\-\-\-\-\- | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\ |
|         | \-\-\-\-\-\-\- | -\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|         | \-\-\-\-\--+   | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\ |
|         |                | -\-\-\-\-\-\--+                           |
|         | :   /network-l |                                           |
|         | ink/(string:id | :   Returns the network link selected by  |
|         | )              |     the given `id` and the query in the   |
|         |                |     request body.                         |
+---------+----------------+-------------------------------------------+
| POST    | > /network-lin | > Create one or more new network links.   |
|         | k              |                                           |
| :   -   |                | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\ |
|         | \-\-\-\-\-\-\- | -\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|         | \-\-\-\-\-\-\- | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\ |
|         | \-\-\-\-\-\-\- | -\-\-\-\-\-\--+                           |
|         | \-\-\-\-\--+   |                                           |
|         |                | :   Create a new network link with the    |
|         | :   /network-l |     given `id`.                           |
|         | ink/(string:id |                                           |
|         | )              |                                           |
+---------+----------------+-------------------------------------------+
| PUT     | > /network-lin | > Update one or more existing network     |
|         | k              | > links.                                  |
| :   -   |                |                                           |
|         | \-\-\-\-\-\-\- | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\ |
|         | \-\-\-\-\-\-\- | -\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|         | \-\-\-\-\-\-\- | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\ |
|         | \-\-\-\-\--+   | -\-\-\-\-\-\--+                           |
|         |                |                                           |
|         | :   /network-l | :   Update the network link with given    |
|         | ink/(string:id |     `id`.                                 |
|         | )              |                                           |
+---------+----------------+-------------------------------------------+
| DELETE  | > /network-lin | > Delete the network links selected by    |
|         | k              | > the query in the request body (or all   |
| > -     |                | > it the request body is empty).          |
|         | \-\-\-\-\-\-\- |                                           |
|         | \-\-\-\-\-\-\- | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\ |
|         | \-\-\-\-\-\-\- | -\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|         | \-\-\-\-\--+   | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\ |
|         |                | -\-\-\-\-\-\--+                           |
|         | :   /network-l |                                           |
|         | ink/(string:id | :   Delete the network link selected by   |
|         | )              |     the given `id` and the query in the   |
|         |                |     request body.                         |
+---------+----------------+-------------------------------------------+

### Network link Type

+--------+------------------+------------------------------------------+
| `HTTP  | Path             | Action                                   |
| (Hyper |                  |                                          |
| Text T |                  |                                          |
| ransfe |                  |                                          |
| r Prot |                  |                                          |
| ocol)` |                  |                                          |
| {.inte |                  |                                          |
| rprete |                  |                                          |
| d-text |                  |                                          |
| role=" |                  |                                          |
| abbr"} |                  |                                          |
| Method |                  |                                          |
+========+==================+==========================================+
| GET    | > /type/network- | > Returns the network link types         |
|        | link             | > selected by the query in the request   |
| > -    |                  | > body (or all it the request body is    |
|        | \-\-\-\-\-\-\-\- | > empty).                                |
|        | \-\-\-\-\-\-\-\- |                                          |
|        | \-\-\-\-\-\-\-\- | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|        | \-\-\-\-\-\-\--+ | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|        |                  | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|        | :   /type/networ | \-\-\-\-\-\-\-\-\-\-\-\-\--+             |
|        | k-link/(string:i |                                          |
|        | d)               | :   Returns the network link type        |
|        |                  |     selected by the given `id` and the   |
|        |                  |     query in the request body.           |
+--------+------------------+------------------------------------------+
| POST   | > /type/network- | > Create one or more new network link    |
|        | link             | > types.                                 |
| :   -  |                  |                                          |
|        | \-\-\-\-\-\-\-\- | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|        | \-\-\-\-\-\-\-\- | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|        | \-\-\-\-\-\-\-\- | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|        | \-\-\-\-\-\-\--+ | \-\-\-\-\-\-\-\-\-\-\-\-\--+             |
|        |                  |                                          |
|        | :   /type/networ | :   Create a new network link type with  |
|        | k-link/(string:i |     the given `id`.                      |
|        | d)               |                                          |
+--------+------------------+------------------------------------------+
| PUT    | > /type/network- | > Update one or more existing network    |
|        | link             | > link types.                            |
| :   -  |                  |                                          |
|        | \-\-\-\-\-\-\-\- | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|        | \-\-\-\-\-\-\-\- | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|        | \-\-\-\-\-\-\-\- | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|        | \-\-\-\-\-\-\--+ | \-\-\-\-\-\-\-\-\-\-\-\-\--+             |
|        |                  |                                          |
|        | :   /type/networ | :   Update the network link type with    |
|        | k-link/(string:i |     given `id`.                          |
|        | d)               |                                          |
+--------+------------------+------------------------------------------+
| DELETE | > /type/network- | > Delete the network link types selected |
|        | link             | > by the query in the request body (or   |
| > -    |                  | > all it the request body is empty).     |
|        | \-\-\-\-\-\-\-\- |                                          |
|        | \-\-\-\-\-\-\-\- | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|        | \-\-\-\-\-\-\-\- | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|        | \-\-\-\-\-\-\--+ | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|        |                  | \-\-\-\-\-\-\-\-\-\-\-\-\--+             |
|        | :   /type/networ |                                          |
|        | k-link/(string:i | :   Delete the network link type         |
|        | d)               |     selected by the given `id` and the   |
|        |                  |     query in the request body.           |
+--------+------------------+------------------------------------------+

Connection
----------

+---------+----------------+-------------------------------------------+
| `HTTP ( | Path           | Action                                    |
| HyperTe |                |                                           |
| xt Tran |                |                                           |
| sfer Pr |                |                                           |
| otocol) |                |                                           |
| `{.inte |                |                                           |
| rpreted |                |                                           |
| -text   |                |                                           |
| role="a |                |                                           |
| bbr"}   |                |                                           |
| Method  |                |                                           |
+=========+================+===========================================+
| GET     | > /connection  | > Returns the connections selected by the |
|         |                | > query in the request body (or all it    |
| > -     | \-\-\-\-\-\-\- | > the request body is empty).             |
|         | \-\-\-\-\-\-\- |                                           |
|         | \-\-\-\-\-\-\- | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\ |
|         | \-\-\--+       | -\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|         |                | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\ |
|         | :   /connectio | -\-\-\-\--+                               |
|         | n/(string:id)  |                                           |
|         |                | :   Returns the connection selected by    |
|         |                |     the given `id` and the query in the   |
|         |                |     request body.                         |
+---------+----------------+-------------------------------------------+
| POST    | > /connection  | > Create one or more new connections.     |
|         |                |                                           |
| :   -   | \-\-\-\-\-\-\- | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\ |
|         | \-\-\-\-\-\-\- | -\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|         | \-\-\-\-\-\-\- | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\ |
|         | \-\-\--+       | -\-\-\-\--+                               |
|         |                |                                           |
|         | :   /connectio | :   Create a new connection with the      |
|         | n/(string:id)  |     given `id`.                           |
+---------+----------------+-------------------------------------------+
| PUT     | > /connection  | > Update one or more existing             |
|         |                | > connections.                            |
| :   -   | \-\-\-\-\-\-\- |                                           |
|         | \-\-\-\-\-\-\- | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\ |
|         | \-\-\-\-\-\-\- | -\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|         | \-\-\--+       | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\ |
|         |                | -\-\-\-\--+                               |
|         | :   /connectio |                                           |
|         | n/(string:id)  | :   Update the connection with given      |
|         |                |     `id`.                                 |
+---------+----------------+-------------------------------------------+
| DELETE  | > /connection  | > Delete the connections selected by the  |
|         |                | > query in the request body (or all it    |
| > -     | \-\-\-\-\-\-\- | > the request body is empty).             |
|         | \-\-\-\-\-\-\- |                                           |
|         | \-\-\-\-\-\-\- | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\ |
|         | \-\-\--+       | -\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|         |                | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\ |
|         | :   /connectio | -\-\-\-\--+                               |
|         | n/(string:id)  |                                           |
|         |                | :   Delete the connection selected by the |
|         |                |     given `id` and the query in the       |
|         |                |     request body.                         |
+---------+----------------+-------------------------------------------+

Agent
-----

### Catalog

+---------+-----------------+------------------------------------------+
| `HTTP ( | Path            | Action                                   |
| HyperTe |                 |                                          |
| xt Tran |                 |                                          |
| sfer Pr |                 |                                          |
| otocol) |                 |                                          |
| `{.inte |                 |                                          |
| rpreted |                 |                                          |
| -text   |                 |                                          |
| role="a |                 |                                          |
| bbr"}   |                 |                                          |
| Method  |                 |                                          |
+=========+=================+==========================================+
| GET     | > /catalog/agen | > Returns the agents from the catalog    |
|         | t               | > selected by the query in the request   |
| > -     |                 | > body (or all it the request body is    |
|         | \-\-\-\-\-\-\-\ | > empty).                                |
|         | -\-\-\-\-\-\-\- |                                          |
|         | \-\-\-\-\-\-\-\ | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|         | -\-\-\-\--+     | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|         |                 | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|         | :   /catalog/ag | \-\-\-\-\--+                             |
|         | ent/(string:id) |                                          |
|         |                 | :   Returns the agent from the catalog   |
|         |                 |     selected by the given `id` and the   |
|         |                 |     query in the request body.           |
+---------+-----------------+------------------------------------------+
| POST    | > /catalog/agen | > Insert one or more new agents in the   |
|         | t               | > catalog.                               |
| :   -   |                 |                                          |
|         | \-\-\-\-\-\-\-\ | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|         | -\-\-\-\-\-\-\- | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|         | \-\-\-\-\-\-\-\ | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|         | -\-\-\-\--+     | \-\-\-\-\--+                             |
|         |                 |                                          |
|         | :   /catalog/ag | :   Insert a new agents in the catalog   |
|         | ent/(string:id) |     with the given `id`.                 |
+---------+-----------------+------------------------------------------+
| PUT     | > /catalog/agen | > Update one or more existing agents in  |
|         | t               | > the catalog.                           |
| :   -   |                 |                                          |
|         | \-\-\-\-\-\-\-\ | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|         | -\-\-\-\-\-\-\- | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|         | \-\-\-\-\-\-\-\ | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|         | -\--+\-\--      | \-\-\-\-\--+                             |
|         | /catalog/agent/ |                                          |
|         | (string:id)     | :   Update the agent in the catalog with |
|         |                 |     given `id`.                          |
+---------+-----------------+------------------------------------------+
| DELETE  | > /catalog/agen | > Delete the agents from the catalog     |
|         | t               | > selected by the query in the request   |
| > -     |                 | > body (or all it the request body is    |
|         | \-\-\-\-\-\-\-\ | > empty).                                |
|         | -\-\-\-\-\-\-\- |                                          |
|         | \-\-\-\-\-\-\-\ | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|         | -\-\-\-\--+     | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|         |                 | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|         | :   /catalog/ag | \-\-\-\-\--+                             |
|         | ent/(string:id) |                                          |
|         |                 | :   Delete the agent from the catalog    |
|         |                 |     selected by the given `id` and the   |
|         |                 |     query in the request body.           |
+---------+-----------------+------------------------------------------+

### Instance

+---------+-------------------+---------------------------------------+
| `HTTP ( | Path              | Action                                |
| HyperTe |                   |                                       |
| xt Tran |                   |                                       |
| sfer Pr |                   |                                       |
| otocol) |                   |                                       |
| `{.inte |                   |                                       |
| rpreted |                   |                                       |
| -text   |                   |                                       |
| role="a |                   |                                       |
| bbr"}   |                   |                                       |
| Method  |                   |                                       |
+=========+===================+=======================================+
| GET     | > /instance/agent | > Returns the agent instances         |
|         |                   | > selected by the query in the        |
| > -     | \-\-\-\-\-\-\-\-\ | > request body (or all it the request |
|         | -\-\-\-\-\-\-\-\- | > body is empty).                     |
|         | \-\-\-\-\-\-\-\-\ |                                       |
|         | -\-\--+           | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\ |
|         |                   | -\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|         | :   /instance/age | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\ |
|         | nt/(string:id)    | -\--+                                 |
|         |                   |                                       |
|         |                   | :   Returns the agent instances       |
|         |                   |     selected by the given `id` and    |
|         |                   |     the query in the request body.    |
+---------+-------------------+---------------------------------------+
| POST    | > /instance/agent | > Create one or more new agent        |
|         |                   | > instances.                          |
| :   -   | \-\-\-\-\-\-\-\-\ |                                       |
|         | -\-\-\-\-\-\-\-\- | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\ |
|         | \-\-\-\-\-\-\-\-\ | -\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|         | -\-\--+           | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\ |
|         |                   | -\--+                                 |
|         | :   /instance/age |                                       |
|         | nt/(string:id)    | :   Create a new agent instances with |
|         |                   |     the given `id`.                   |
+---------+-------------------+---------------------------------------+
| PUT     | > /instance/agent | > Update one or more existing agent   |
|         |                   | > instances.                          |
| :   -   | \-\-\-\-\-\-\-\-\ |                                       |
|         | -\-\-\-\-\-\-\-\- | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\ |
|         | \-\-\-\-\-\-\-\-\ | -\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|         | -\-\--+           | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\ |
|         |                   | -\--+                                 |
|         | :   /instance/age |                                       |
|         | nt/(string:id)    | :   Update the agent instance with    |
|         |                   |     given `id`.                       |
+---------+-------------------+---------------------------------------+
| DELETE  | > /instance/agent | > Delete the agent instances selected |
|         |                   | > by the query in the request body    |
| > -     | \-\-\-\-\-\-\-\-\ | > (or all it the request body is      |
|         | -\-\-\-\-\-\-\-\- | > empty).                             |
|         | \-\-\-\-\-\-\-\-\ |                                       |
|         | -\-\--+           | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\ |
|         |                   | -\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|         | :   /instance/age | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\ |
|         | nt/(string:id)    | -\--+                                 |
|         |                   |                                       |
|         |                   | :   Delete the agent instance         |
|         |                   |     selected by the given `id` and    |
|         |                   |     the query in the request body.    |
+---------+-------------------+---------------------------------------+

eBPF Program
------------

### Catalog

+--------+-------------------+-----------------------------------------+
| `HTTP  | Path              | Action                                  |
| (Hyper |                   |                                         |
| Text T |                   |                                         |
| ransfe |                   |                                         |
| r Prot |                   |                                         |
| ocol)` |                   |                                         |
| {.inte |                   |                                         |
| rprete |                   |                                         |
| d-text |                   |                                         |
| role=" |                   |                                         |
| abbr"} |                   |                                         |
| Method |                   |                                         |
+========+===================+=========================================+
| GET    | > /catalog/ebpf-p | > Returns the `eBPF (extended Berkeley  |
|        | rogram            | Packet Filter)`{.interpreted-text       |
| > -    |                   | > role="abbr"} programs from the        |
|        | \-\-\-\-\-\-\-\-\ | > catalog selected by the query in the  |
|        | -\-\-\-\-\-\-\-\- | > request body (or all it the request   |
|        | \-\-\-\-\-\-\-\-\ | > body is empty).                       |
|        | -\-\-\-\-\-\-\-\- |                                         |
|        | -+                | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\ |
|        |                   | -\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|        | :   /catalog/ebpf | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\ |
|        | -program/(string: | -\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--+       |
|        | id)               |                                         |
|        |                   | :   Returns the `eBPF (extended Berkele |
|        |                   | y Packet Filter)`{.interpreted-text     |
|        |                   |     role="abbr"} program from the       |
|        |                   |     catalog selected by the given `id`  |
|        |                   |     and the query in the request body.  |
+--------+-------------------+-----------------------------------------+
| POST   | > /catalog/ebpf-p | > Insert one or more new                |
|        | rogram            | > `eBPF (extended Berkeley Packet Filte |
| :   -  |                   | r)`{.interpreted-text                   |
|        | \-\-\-\-\-\-\-\-\ | > role="abbr"} programs in the catalog. |
|        | -\-\-\-\-\-\-\-\- |                                         |
|        | \-\-\-\-\-\-\-\-\ | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\ |
|        | -\-\-\-\-\-\-\-\- | -\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|        | -+                | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\ |
|        |                   | -\-\-\-\-\-\-\-\-\-\-\-\-\-\-- +        |
|        | :   /catalog/ebpf |                                         |
|        | -program/(string: | :   Insert a new                        |
|        | id)               |     `eBPF (extended Berkeley Packet Fil |
|        |                   | ter)`{.interpreted-text                 |
|        |                   |     role="abbr"} programs in the        |
|        |                   |     catalog with the given `id`.        |
+--------+-------------------+-----------------------------------------+
| PUT    | > /catalog/ebpf-p | > Update one or more existing           |
|        | rogram            | > `eBPF (extended Berkeley Packet Filte |
| :   -  |                   | r)`{.interpreted-text                   |
|        | \-\-\-\-\-\-\-\-\ | > role="abbr"} programs in the catalog. |
|        | -\-\-\-\-\-\-\-\- |                                         |
|        | \-\-\-\-\-\-\-\-\ | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\ |
|        | -\-\-\-\-\-\-\-\- | -\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|        | -+                | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\ |
|        |                   | -\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--+       |
|        | :   /catalog/ebpf |                                         |
|        | -program/(string: | :   Update the `eBPF (extended Berkeley |
|        | id)               |  Packet Filter)`{.interpreted-text      |
|        |                   |     role="abbr"} program in the catalog |
|        |                   |     with given `id`.                    |
+--------+-------------------+-----------------------------------------+
| DELETE | > /catalog/ebpf-p | > Delete the `eBPF (extended Berkeley P |
|        | rogram            | acket Filter)`{.interpreted-text        |
| > -    |                   | > role="abbr"} programs from the        |
|        | \-\-\-\-\-\-\-\-\ | > catalog selected by the query in the  |
|        | -\-\-\-\-\-\-\-\- | > request body (or all it the request   |
|        | \-\-\-\-\-\-\-\-\ | > body is empty).                       |
|        | -\-\-\-\-\-\-\-\- |                                         |
|        | -+                | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\ |
|        |                   | -\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|        | :   /catalog/ebpf | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\ |
|        | -program/(string: | -\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--+       |
|        | id)               |                                         |
|        |                   | :   Delete the `eBPF (extended Berkeley |
|        |                   |  Packet Filter)`{.interpreted-text      |
|        |                   |     role="abbr"} program from the       |
|        |                   |     catalog selected by the given `id`  |
|        |                   |     and the query in the request body.  |
+--------+-------------------+-----------------------------------------+

### Instance

+--------+---------------------+---------------------------------------+
| `HTTP  | Path                | Action                                |
| (Hyper |                     |                                       |
| Text T |                     |                                       |
| ransfe |                     |                                       |
| r Prot |                     |                                       |
| ocol)` |                     |                                       |
| {.inte |                     |                                       |
| rprete |                     |                                       |
| d-text |                     |                                       |
| role=" |                     |                                       |
| abbr"} |                     |                                       |
| Method |                     |                                       |
+========+=====================+=======================================+
| GET    | > /instance/ebpf-pr | > Returns the `eBPF (extended Berkele |
|        | ogram               | y Packet Filter)`{.interpreted-text   |
| > -    |                     | > role="abbr"} program instances      |
|        | \-\-\-\-\-\-\-\-\-\ | > selected by the query in the        |
|        | -\-\-\-\-\-\-\-\-\- | > request body (or all it the request |
|        | \-\-\-\-\-\-\-\-\-\ | > body is empty).                     |
|        | -\-\-\-\-\-\--+     |                                       |
|        |                     | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\ |
|        | :   /instance/ebpf- | -\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|        | program/(string:id) | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\ |
|        |                     | -\-\-\-\-\-\-\-\-\-\--+               |
|        |                     |                                       |
|        |                     | :   Returns the `eBPF (extended Berke |
|        |                     | ley Packet Filter)`{.interpreted-text |
|        |                     |     role="abbr"} program instances    |
|        |                     |     selected by the given `id` and    |
|        |                     |     the query in the request body.    |
+--------+---------------------+---------------------------------------+
| POST   | > /instance/ebpf-pr | > Create one or more new              |
|        | ogram               | > `eBPF (extended Berkeley Packet Fil |
| :   -  |                     | ter)`{.interpreted-text               |
|        | \-\-\-\-\-\-\-\-\-\ | > role="abbr"} program instances.     |
|        | -\-\-\-\-\-\-\-\-\- |                                       |
|        | \-\-\-\-\-\-\-\-\-\ | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\ |
|        | -\-\-\-\-\-\--+     | -\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|        |                     | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\ |
|        | :   /instance/ebpf- | -\-\-\-\-\-\-\-\-\-\--+               |
|        | program/(string:id) |                                       |
|        |                     | :   Create a new                      |
|        |                     |     `eBPF (extended Berkeley Packet F |
|        |                     | ilter)`{.interpreted-text             |
|        |                     |     role="abbr"} program instances    |
|        |                     |     with the given `id`.              |
+--------+---------------------+---------------------------------------+
| PUT    | > /instance/ebpf-pr | > Update one or more existing         |
|        | ogram               | > `eBPF (extended Berkeley Packet Fil |
| :   -  |                     | ter)`{.interpreted-text               |
|        | \-\-\-\-\-\-\-\-\-\ | > role="abbr"} program instances.     |
|        | -\-\-\-\-\-\-\-\-\- |                                       |
|        | \-\-\-\-\-\-\-\-\-\ | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\ |
|        | -\-\-\-\-\-\--+     | -\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|        |                     | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\ |
|        | :   /instance/ebpf- | -\-\-\-\-\-\-\-\-\-\--+               |
|        | program/(string:id) |                                       |
|        |                     | :   Update the `eBPF (extended Berkel |
|        |                     | ey Packet Filter)`{.interpreted-text  |
|        |                     |     role="abbr"} program instance     |
|        |                     |     with given `id`.                  |
+--------+---------------------+---------------------------------------+
| DELETE | > /instance/ebpf-pr | > Delete the `eBPF (extended Berkeley |
|        | ogram               |  Packet Filter)`{.interpreted-text    |
| > -    |                     | > role="abbr"} program instances      |
|        | \-\-\-\-\-\-\-\-\-\ | > selected by the query in the        |
|        | -\-\-\-\-\-\-\-\-\- | > request body (or all it the request |
|        | \-\-\-\-\-\-\-\-\-\ | > body is empty).                     |
|        | -\-\-\-\-\-\--+     |                                       |
|        |                     | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\ |
|        | :   /instance/ebpf- | -\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|        | program/(string:id) | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\ |
|        |                     | -\-\-\-\-\-\-\-\-\-\--+               |
|        |                     |                                       |
|        |                     | :   Delete the `eBPF (extended Berkel |
|        |                     | ey Packet Filter)`{.interpreted-text  |
|        |                     |     role="abbr"} program instance     |
|        |                     |     selected by the given `id` and    |
|        |                     |     the query in the request body.    |
+--------+---------------------+---------------------------------------+

Data
----

+---------+------------+----------------------------------------------+
| `HTTP ( | Path       | Action                                       |
| HyperTe |            |                                              |
| xt Tran |            |                                              |
| sfer Pr |            |                                              |
| otocol) |            |                                              |
| `{.inte |            |                                              |
| rpreted |            |                                              |
| -text   |            |                                              |
| role="a |            |                                              |
| bbr"}   |            |                                              |
| Method  |            |                                              |
+=========+============+==============================================+
| GET     | > /data    | > Returns the collected data selected by the |
|         |            | > query in the request body (or all it the   |
| > -     | \-\-\-\-\- | > request body is empty).                    |
|         | \-\-\-\-\- |                                              |
|         | \-\-\-\-\- | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|         | \-\-\--+   | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|         |            | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|         | :   /data/ | \-\-\--+                                     |
|         | (string:id |                                              |
|         | )          | :   Returns the collected data selected by   |
|         |            |     the given `id` and the query in the      |
|         |            |     request body.                            |
+---------+------------+----------------------------------------------+
| POST    | > /data    | > Create one or more new collected data.     |
|         |            |                                              |
| :   -   | \-\-\-\-\- | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|         | \-\-\-\-\- | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|         | \-\-\-\-\- | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|         | \-\-\--+   | \-\-\--+                                     |
|         |            |                                              |
|         | :   /data/ | :   Create a new collected data with the     |
|         | (string:id |     given `id`.                              |
|         | )          |                                              |
+---------+------------+----------------------------------------------+
| PUT     | > /data    | > Update one or more existing collected      |
|         |            | > data.                                      |
| :   -   | \-\-\-\-\- |                                              |
|         | \-\-\-\-\- | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|         | \-\-\-\-\- | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|         | \-\-\--+   | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|         |            | \-\-\--+                                     |
|         | :   /data/ |                                              |
|         | (string:id | :   Update the collected data with given     |
|         | )          |     `id`.                                    |
+---------+------------+----------------------------------------------+
| DELETE  | > /data    | > Delete the collected data selected by the  |
|         |            | > query in the request body (or all it the   |
| > -     | \-\-\-\-\- | > request body is empty).                    |
|         | \-\-\-\-\- |                                              |
|         | \-\-\-\-\- | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|         | \-\-\--+   | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|         |            | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|         | :   /data/ | \-\-\--+                                     |
|         | (string:id |                                              |
|         | )          | :   Delete the collected data selected by    |
|         |            |     the given `id` and the query in the      |
|         |            |     request body.                            |
+---------+------------+----------------------------------------------+

Guide
=====

See the Swagger Schema ([\|YAML\|](api/swagger.yaml),
[\|JSON\|](api/swagger.json)) and the relative **documentation**
(`REST (Representational State Transfer)`{.interpreted-text role="abbr"}
endpoint `/api/doc </api/doc>`) more details about the
`REST (Representational State Transfer)`{.interpreted-text role="abbr"}
endpoints and relative formats and requirements of request and response.

Installation
============

1.  Prerequisite
    -   python (version \>= 3.5)
    -   pip (for python 3)
2.  Clone the repository.

``` {.sourceCode .console}
git clone https://gitlab.com/guard-repositories/cb-manager.git
cd cb-manager
```

3.  Install the dependencies.

``` {.sourceCode .console}
pip3 install -r requirements.txt
```

Configuration
=============

The configurations are stored in the [config.ini](config.ini) file.

+---------+----------+------------+-----------------------------------+
| Section | Setting  | Default    | Note                              |
|         |          | value      |                                   |
+=========+==========+============+===================================+
| context | > host   | > 0.0.0.0  | > `IP (Internet Protocol)`{.inter |
| =broker |          |            | preted-text                       |
|         | \-\-\-\- | \-\-\-\-\- | > role="abbr"} address to accept  |
| :   -   | \-\-\-\- | \-\-\-\-\- | > requests.                       |
|         | \-\-\-\- | \-\-\-\-\- |                                   |
|         | \-\-\-\- | \-\-\-\--+ | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\ |
|         | -+       |            | -\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|         |          | :   5000   | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\ |
|         | :   port |            | -\-\-\-\-\-\--+                   |
|         |          |            |                                   |
|         |          |            | :   `TCP (Transmission Control Pr |
|         |          |            | otocol)`{.interpreted-text        |
|         |          |            |     role="abbr"} Port of the      |
|         |          |            |     `REST (Representational State |
|         |          |            |  Transfer)`{.interpreted-text     |
|         |          |            |     role="abbr"} Server.          |
+---------+----------+------------+-----------------------------------+
| heartbe | > timeou | > 5s       | > Timeout for heartbeat with      |
| at      | t        |            | > `LCP (Local Control Plane)`{.in |
|         |          | \-\-\-\-\- | terpreted-text                    |
| :   -   | \-\-\-\- | \-\-\-\-\- | > role="abbr"}.                   |
|  -      | \-\-\-\- | \-\-\-\-\- |                                   |
|         | \-\-\-\- | \-\-\-\--+ | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\ |
|         | \-\-\-\- |            | -\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|         | -+       | :   10s    | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\ |
|         |          |            | -\-\-\-\-\-\--+                   |
|         | :   peri | \-\-\-\-\- |                                   |
|         | od       | \-\-\-\-\- | :   Period for the heartbeat with |
|         |          | \-\-\-\-\- |     the                           |
|         | \-\-\-\- | \-\-\-\--+ |     `LCP (Local Control Plane)`{. |
|         | \-\-\-\- |            | interpreted-text                  |
|         | \-\-\-\- | :   5min   |     role="abbr"}.                 |
|         | \-\-\-\- |            |                                   |
|         | -+       |            | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\ |
|         |          |            | -\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|         | :   auth |            | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\ |
|         | -expirat |            | -\-\-\-\-\-\--+                   |
|         | ion      |            |                                   |
|         |          |            | :   Period for auth expiration    |
|         |          |            |     used in the heartbeat with    |
|         |          |            |     the                           |
|         |          |            |     `LCP (Local Control Plane)`{. |
|         |          |            | interpreted-text                  |
|         |          |            |     role="abbr"}.                 |
+---------+----------+------------+-----------------------------------+
| elastic | > endpoi | > elastics | > Elasticsearch server            |
| search  | nt       | earch:9200 | > hostname/`IP (Internet Protocol |
|         |          |            | )`{.interpreted-text              |
| :   -   | \-\-\-\- | \-\-\-\-\- | > role="abbr"}:port.              |
|  -      | \-\-\-\- | \-\-\-\-\- |                                   |
|         | \-\-\-\- | \-\-\-\-\- | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\ |
|         | \-\-\-\- | \-\-\-\--+ | -\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|         | -+       |            | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\ |
|         |          | :   20s    | -\-\-\-\-\-\--+                   |
|         | :   time |            |                                   |
|         | out      | \-\-\-\-\- | :   Timeout for the connection to |
|         |          | \-\-\-\-\- |     Elasticsearch.                |
|         | \-\-\-\- | \-\-\-\-\- |                                   |
|         | \-\-\-\- | \-\-\-\--+ | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\ |
|         | \-\-\-\- |            | -\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|         | \-\-\-\- | :   1min   | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\ |
|         | -+       |            | -\-\-\-\-\-\--+                   |
|         |          |            |                                   |
|         | :   retr |            | :   Period to retry the           |
|         | y-period |            |     connection to Elasticsearch.  |
+---------+----------+------------+-----------------------------------+
| dev     | > userna | > cb-manag | > Username for                    |
|         | me       | er         | > `HTTP (HyperText Transfer Proto |
| :   -   |          |            | col)`{.interpreted-text           |
|         | \-\-\-\- | \-\-\-\-\- | > role="abbr"} authentication     |
|         | \-\-\-\- | \-\-\-\-\- | > (for developer use).            |
|         | \-\-\-\- | \-\-\-\-\- |                                   |
|         | \-\-\-\- | \-\-\-\--+ | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\ |
|         | -+       |            | -\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- |
|         |          | :   guard | \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\ |
|         | :   pass | [^9]       | -\-\-\-\-\-\--+                   |
|         | word     |            |                                   |
|         |          |            | :   Password for                  |
|         |          |            |     `HTTP (HyperText Transfer Pro |
|         |          |            | tocol)`{.interpreted-text         |
|         |          |            |     role="abbr"} authentication   |
|         |          |            |     (for developer use).          |
+---------+----------+------------+-----------------------------------+

Usage
=====

Display help
------------

`` `bash python3 main.py -h ``\`

::: {.glossary}
:::

Glossary
========

> ACL
>
> :   Access Control Lis
>
> API
>
> :   Application Program Interface
>
> BA
>
> :   Basic Authentication
>
> BPF
>
> :   Berkeley Packet Filter
>
> CB
>
> :   Context Broker
>
> CII
>
> :   Core Infrastructure Initiative
>
> CRUD
>
> :   Create - Read - Update - Delete
>
> DB
>
> :   Database
>
> eBPF
>
> :   extended BPF
>
> ELK
>
> :   Elastic - LogStash - Kibana
>
> Exec\_Env
>
> :   Execution Environment
>
> gRPC
>
> :   Google RPC
>
> HOBA
>
> :   HTTP Origin-Bound Authentication
>
> HTTP
>
> :   Hyper Text Transfer Protocol
>
> ID
>
> :   Identification
>
> IP
>
> :   Internet Protocol
>
> JSON
>
> :   Java Object Notation
>
> LCP
>
> :   Local Control Plane
>
> LDAP
>
> :   Lightweight Directory Access Protocol
>
> MIT
>
> :   Massachusetts Institute of Technology
>
> RBAC
>
> :   Role-Based Access Control
>
> regex
>
> :   regular expression
>
> REST
>
> :   Representational State Transfer
>
> RFC
>
> :   Request For Comments
>
> RPC
>
> :   Remote Procedure Call
>
> SCM
>
> :   Security Context Model
>
> SLA
>
> :   Service Level Agreements
>
> SQL
>
> :   Structured Query Language
>
> TCP
>
> :   Transmission Control Protocol
>
> TTL
>
> :   Time To Live
>
> VNF
>
> :   Virtual Network Function
>
> YANG
>
> :   Yet Another Next Generation
>
> YAML
>
> :   YAML Ain\'t Markup languages
>
References
==========

[^1]: In the dash-case (also referred as **hyphen-case** or
    **kebab-case**) format all the letters are lower-case, the
    punctuation is not allowed and the words are separated by single
    dash (or hyphen: -). Example: `exec-env`.

[^2]: We use the terms properties, fields and attributes
    interchangeably.

[^3]: In the snake-case format all the letters are lower-case, the
    punctuation is not allowed and the words are separated by single
    underscore (\_). Example: `exec_env_id`.

[^4]: In our architecture the agents are Beats from Elastic Stack.
    Notwithstanding, the data model refers to a generic agent allowing
    to possibility to use different types.

[^5]: In Elasticsearch, each document is identified by a unique id. For
    obvious reasons, in the description of the following indices, we
    omit the description of all the id fields.

[^6]: \"Getting started with Beats,\" \[Online\]. Available:
    [libbeat](https://www.elastic.co/guide/en/beats/libbeat/current/getting-started.html).

[^7]: \"Polycube. eBPF/XDP-based software framework for fast network
    services running in the Linux kernel,\" \[Online\]. Available:
    [Polycube in GitHub](https://github.com/polycube-network/polycube).

[^8]: With nested index, we refer to index that are embedded inside your
    parent one, [managing relations inside
    elasticsearch](https://www.elastic.co/blog/managing-relations-inside-elasticsearch)

[^9]: Stored in hashed sha256 version.


<!-- saved from url=(0035)https://pandoc.org/demo/footer.html -->
<html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"></head><body><div id="footer">
  © 2006-2007 <a href="http://johnmacfarlane.net/">John MacFarlane</a>
</div>

</body></html>
