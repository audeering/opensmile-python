================
openSMILE Python
================

|tests| |docs| |python-versions| |license| 

Python interface for extracting openSMILE_ features.

Currently, three standard sets are supported.
`ComParE 2016`_ is the largest with more than 6k features.
The smaller sets GeMAPS_ and  eGeMAPS_
come in two variants ``v01a`` and ``v01b``.
We suggest to use the newer version
unless backward compatibility with
the original papers is desired.

Each feature set can be extracted on three levels:

* Low-level descriptors (LDD)
* LLDs with deltas
* Functionals

The following table lists the number of features
for each set and level.

============  ==============
Name          #features
============  ==============
ComParE_2016  65 / 65 / 6373
GeMAPSv01a    5 / 13 / 62
GeMAPSv01b    62 / 13 / 62
eGeMAPSv01a   10 / 13 / 88
eGeMAPSv01b   10 / 13 / 88
============  ==============

Code example,
that extracts `ComParE 2016`_  functionals from an audio file:

.. code-block:: python

    import opensmile

    smile = opensmile.Smile(
        feature_set=opensmile.FeatureSet.ComParE_2016,
        feature_level=opensmile.FeatureLevel.Functionals,
    )
    y = smile.process_file('audio.wav')


.. _openSMILE: https://github.com/audeering/opensmile
.. _ComParE 2016: http://www.tangsoo.de/documents/Publications/Schuller16-TI2.pdf
.. _GeMAPS: https://sail.usc.edu/publications/files/eyben-preprinttaffc-2015.pdf
.. _eGeMAPS: https://sail.usc.edu/publications/files/eyben-preprinttaffc-2015.pdf

.. badges images and links:
.. |tests| image:: https://github.com/audeering/opensmile-python/workflows/Test/badge.svg
    :target: https://github.com/audeering/opensmile-python/actions?query=workflow%3ATest
    :alt: Test status
.. |docs| image:: https://img.shields.io/pypi/v/opensmile?label=docs
    :target: https://audeering.github.io/opensmile/
    :alt: opensmile's documentation
.. |license| image:: https://img.shields.io/badge/license-audEERING-red.svg
    :target: https://github.com/audeering/opensmile-python/blob/master/LICENSE
    :alt: opensmile's audEERING license
.. |python-versions| image:: https://img.shields.io/pypi/pyversions/opensmile.svg
    :target: https://pypi.org/project/opensmile/
    :alt: opensmile's supported Python versions
