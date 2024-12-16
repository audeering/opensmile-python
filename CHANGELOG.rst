Changelog
=========

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog`_,
and this project adheres to `Semantic Versioning`_.


Version 2.5.1 (2024-12-16)
--------------------------

* Added: support for Python 3.12
* Added: support for Python 3.13
* Removed: support for Python 3.8


Version 2.5.0 (2023-10-19)
--------------------------

* Added: support for ``manylinux_2_17_armv7l`` aka Raspberry PI
* Added: support for ``manylinux_2_17_aarch64``
* Added: support for ``macosx_11_0_arm64`` aka M1
* Added: support for Python 3.11
* Added: support for Python 3.10
* Changed: use binaries from ``opensmile`` v3.0.2
* Changed: build platform dependent wheels
  to reduce installation size
* Removed: support for Python 3.7


Version 2.4.2 (2023-01-03)
--------------------------

* Added: support for Python 3.9
* Changed: split API documentation into sub-pages
  for each function
* Removed: support for Python 3.6


Version 2.4.1 (2022-01-10)
--------------------------

* Changed: switch to ``Python 3.8`` during publishing


Version 2.4.0 (2022-01-10)
--------------------------

* Added: ``multiprocessing`` argument to ``Smile``
* Changed: update binaries to ``3.0.1`` to support multi-threading


Version 2.3.0 (2021-12-16)
--------------------------

* Changed: update to ``audobject >0.6.1``


Version 2.2.0 (2021-07-23)
--------------------------

* Fixed: ``Smile.__call__()`` always returns (channels, features, frames)


Version 2.1.3 (2021-07-06)
--------------------------

* Fixed: include ``emobase`` config files into package


Version 2.1.2 (2021-06-21)
--------------------------

* Fixed: short underline in CHANGELOG


Version 2.1.1 (2021-06-18)
--------------------------

* Changed: enable Windows tests again


Version 2.1.0 (2021-06-16)
--------------------------

* Added: ``channels``, ``mixdown``, ``resample`` argument
* Added: support for ``audformat``
* Changed: disable Windows tests
* Changed: dependency to ``audinterface`` and ``audobject``
* Changed: use ``emodb`` in usage section
* Removed: static files from docs


Version 2.0.2 (2021-05-14)
--------------------------

* Fixed: building docs in publish workflow


Version 2.0.1 (2021-05-14)
--------------------------

* Added: ``FeatureSet.emobase``


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
