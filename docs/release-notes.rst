.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. SPDX-License-Identifier: CC-BY-4.0
.. Copyright (C) 2020 AT&T Intellectual Property

Release Notes
===============

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog <http://keepachangelog.com/>`__
and this project adheres to `Semantic Versioning <http://semver.org/>`__.

.. contents::
   :depth: 3
   :local:

[1.0.0] - 4/1/2020
------------------
::

    * This release is seen as the first complete implementation of QPD, although likely fixes and enhancements are needed
    * Implement the rmr messaging
    * Add tests for various bad scenarios like UE IDs not existing and Cell data not existing
    * Fix UE IDs to be strings as they are in the req slides


[0.2.0] - 3/27/2020
-------------------
::

    * Implement SDL calls and testing
    * Small cleanups


[0.1.0] - 3/26/2020
-------------------
::

    * Implement the core business logic of the data merge

[0.0.2] - 3/25/2020
-------------------
::

    * Move to SI95
    * Move to Xapp frame 0.6.0
    * Move to py38
    * Remove unneeded stuff from setup.py since this is a docker component and not a pypi library
    * Add some mock data for future development

[0.0.1] - 3/17/2020
-------------------
::

    * inital skeleton creation
