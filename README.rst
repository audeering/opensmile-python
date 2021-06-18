================
openSMILE Python
================

|tests| |coverage| |docs| |python-versions| |license| 

Python interface for extracting openSMILE_ features.

.. code-block::

    $ pip install opensmile

.. note:: Only 64-bit Python is supported.

Feature sets
------------

Currently, three standard sets are supported.
`ComParE 2016`_ is the largest with more than 6k features.
The smaller sets GeMAPS_ and  eGeMAPS_
come in variants ``v01a``, ``v01b`` and ``v02`` (only eGeMAPS_).
We suggest to use the latest version
unless backward compatibility with
the original papers is desired.

Each feature set can be extracted on two levels:

* Low-level descriptors (LDD)
* Functionals

For `ComParE 2016`_ a third level is available:

* LLD deltas

.. note:: Pre v2.0.0 some LLDs of the GeMAPS family were incorrectly output
    as deltas. This was corrected with v2.0.0 and these features are now
    correctly returned as LLDs. Note that with v2.0.0 deltas are no
    longer available for the GeMAPS family.

The following table lists the number of features
for each set and level.

With v2.0.0
~~~~~~~~~~~

============  ==============
Name          #features
============  ==============
ComParE_2016  65 / 65 / 6373
GeMAPSv01a    18 / - / 62
GeMAPSv01b    18 / - / 62
eGeMAPSv01a   23 / - / 88
eGeMAPSv01b   23 / - / 88
eGeMAPSv02    25 / - / 88
============  ==============

.. note:: Additional feature sets have been added by the community.
    For a full list please see the documentation of ``opensmile.FeatureSet``.

Pre v2.0.0
~~~~~~~~~~

============  ==============
Name          #features
============  ==============
ComParE_2016  65 / 65 / 6373
GeMAPSv01a    5 / 13 / 62
GeMAPSv01b    5 / 13 / 62
eGeMAPSv01a   10 / 13 / 88
eGeMAPSv01b   10 / 13 / 88
============  ==============

Code example
------------

Code example,
that extracts `ComParE 2016`_  functionals from an audio file:

.. code-block:: python

    import opensmile

    smile = opensmile.Smile(
        feature_set=opensmile.FeatureSet.ComParE_2016,
        feature_level=opensmile.FeatureLevel.Functionals,
    )
    y = smile.process_file('audio.wav')

License
-------

openSMILE follows a dual-licensing model. Since the main goal of the project
is a widespread use of the software to facilitate research in the field of
machine learning from audio-visual signals, the source code and binaries are
freely available for private, research, and educational use under an open-source license
(see LICENSE).
It is not allowed to use the open-source version of openSMILE for any sort of commercial product.
Fundamental research in companies, for example, is permitted, but if a product is the result of
the research, we require you to buy a commercial development license.
Contact us at info@audeering.com (or visit us at https://www.audeering.com) for more information.

Original authors: Florian Eyben, Felix Weninger, Martin Wöllmer, Björn Schuller

Copyright © 2008-2013, Institute for Human-Machine Communication, Technische Universität München, Germany

Copyright © 2013-2015, audEERING UG (haftungsbeschränkt)

Copyright © 2016-2020, audEERING GmbH

Citing
------

Please cite openSMILE in your publications by citing the following paper:

    Florian Eyben, Martin Wöllmer, Björn Schuller: "openSMILE - The Munich Versatile and Fast Open-Source Audio Feature Extractor", Proc. ACM Multimedia (MM), ACM, Florence, Italy, ISBN 978-1-60558-933-6, pp. 1459-1462, 25.-29.10.2010.


.. _openSMILE: https://github.com/audeering/opensmile
.. _ComParE 2016: http://www.tangsoo.de/documents/Publications/Schuller16-TI2.pdf
.. _GeMAPS: https://sail.usc.edu/publications/files/eyben-preprinttaffc-2015.pdf
.. _eGeMAPS: https://sail.usc.edu/publications/files/eyben-preprinttaffc-2015.pdf
.. _audformat: https://github.com/audeering/audformat

.. badges images and links:
.. |tests| image:: https://github.com/audeering/opensmile-python/workflows/Test/badge.svg
    :target: https://github.com/audeering/opensmile-python/actions?query=workflow%3ATest
    :alt: Test status
.. |coverage| image:: https://codecov.io/gh/audeering/opensmile-python/branch/master/graph/badge.svg?token=PUA9P2UJW1
    :target: https://codecov.io/gh/audeering/opensmile-python
    :alt: code coverage
.. |docs| image:: https://img.shields.io/pypi/v/opensmile?label=docs
    :target: https://audeering.github.io/opensmile-python/
    :alt: opensmile's documentation
.. |license| image:: https://img.shields.io/badge/license-audEERING-red.svg
    :target: https://github.com/audeering/opensmile-python/blob/master/LICENSE
    :alt: opensmile's audEERING license
.. |python-versions| image:: https://img.shields.io/pypi/pyversions/opensmile.svg
    :target: https://pypi.org/project/opensmile/
    :alt: opensmile's supported Python versions
