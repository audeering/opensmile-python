================
openSMILE Python
================

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
