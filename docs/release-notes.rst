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


[1.0.4] - 2020-05-05
--------------------

* Upgrade to RMR version 4.0.2


[1.0.3] - 2020-04-22
--------------------

* Upgrade to RMR version 3.8.2


[1.0.2] - 4/8/2020
------------------

* Upgrade to xapp frame 1.0.0 which includes rmr python


[1.0.1] - 4/3/2020
------------------

* Docker now builds with an empty route file so rmr starts; it will not even start properly without this
* Change how fake_sdl is activated for docker convienence
* Create dev guide file
* Add instructions on how to test the rmr healthcheck in a running container
* Update to xapp frame 0.7.0 (which has rmr healthchecks)


[1.0.0] - 4/1/2020
------------------

* This release is seen as the first complete implementation of QPD, although likely fixes and enhancements are needed
* Implement the rmr messaging
* Add tests for various bad scenarios like UE IDs not existing and Cell data not existing
* Fix UE IDs to be strings as they are in the req slides


[0.2.0] - 3/27/2020
-------------------

* Implement SDL calls and testing
* Small cleanups


[0.1.0] - 3/26/2020
-------------------

* Implement the core business logic of the data merge


[0.0.2] - 3/25/2020
-------------------

* Move to SI95
* Move to Xapp frame 0.6.0
* Move to py38
* Remove unneeded stuff from setup.py since this is a docker component and not a pypi library
* Add some mock data for future development


[0.0.1] - 3/17/2020
-------------------

* inital skeleton creation
