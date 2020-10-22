================
openSMILE Python
================

|tests| |docs| |python-versions| |license| 

Python interface for extracting openSMILE_ features.

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
