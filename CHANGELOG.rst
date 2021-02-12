Changelog
=========

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog`_,
and this project adheres to `Semantic Versioning`_.


Version 2.0.0 (2021-02-12)
--------------------------

WARNING: Introduces a breaking change by changing the number of LLDs
in all sets of the GeMAPS family and removing support for deltas
in those sets.

* Added: ``FeatureSet.eGeMAPSv02``
* Changed: add ``lld_de`` features to ``lld`` for the GeMAPS family
* Changed: raise error if ``lld_de`` is requested for a set of the GeMAPS family


Version 1.0.1 (2020-10-23)
--------------------------

* Fixed: add missing binaries to wheel
* Fixed: building docs in publish workflow
* Fixed: link to documentation in badge


Version 1.0.0 (2020-10-23)
--------------------------

* Added: initial release using openSMILE 3.0


.. _Keep a Changelog: https://keepachangelog.com/en/1.0.0/
.. _Semantic Versioning: https://semver.org/spec/v2.0.0.html
