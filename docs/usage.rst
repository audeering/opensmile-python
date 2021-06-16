Usage
=====

The aim of :mod:`opensmile` is to provide
a high-level interface to openSMILE_.
It ships pre-compiled binaries and default feature sets,
but it's also possible to run custom config files.

.. Load from internal audb repository
.. jupyter-execute::
    :hide-code:

    import audb

    audb.config.REPOSITORIES = [
        audb.Repository(
            name='data-public',
            host='https://audeering.jfrog.io/artifactory',
            backend='artifactory',
        ),
    ]

Getting ready
-------------

Let's do some imports and
load some files from the
emodb_ database.

.. jupyter-execute::
    :hide-output:
    :stderr:

    import os
    import time

    import numpy as np
    import pandas as pd

    import audb
    import audiofile
    import opensmile


    db = audb.load(
        'emodb',
        version='1.1.1',
        format='wav',
        mixdown=True,
        sampling_rate=16000,
        media='wav/03a01.*',  # load subset
        full_path=False,
        verbose=False,
    )

.. jupyter-execute::
    :hide-code:

    pd.set_option('display.max_columns', 4)

Process signal
--------------

Read first ten seconds of a file into memory.

.. jupyter-execute::

    file = os.path.join(db.root, db.files[0])
    signal, sampling_rate = audiofile.read(
        file,
        duration=10,
        always_2d=True,
    )

We set up a feature extractor for functionals
of a pre-defined feature set.

.. jupyter-execute::

    smile = opensmile.Smile(
        feature_set=opensmile.FeatureSet.eGeMAPSv02,
        feature_level=opensmile.FeatureLevel.Functionals,
    )
    smile.feature_names

And extract features for the signal.

.. jupyter-execute::

    smile.process_signal(
        signal,
        sampling_rate
    )

Now we create a feature extractor
for low-level descriptors (LLDs).

.. jupyter-execute::

    smile = opensmile.Smile(
        feature_set=opensmile.FeatureSet.eGeMAPSv02,
        feature_level=opensmile.FeatureLevel.LowLevelDescriptors,
    )
    smile.feature_names

And re-run feature extraction.

.. jupyter-execute::

    smile = opensmile.Smile(
        feature_set=opensmile.FeatureSet.eGeMAPSv02,
        feature_level=opensmile.FeatureLevel.LowLevelDescriptors,
    )
    smile.process_signal(
        signal,
        sampling_rate
    )

Logging
-------

To know what happens under the hood
we can create a log file.

.. jupyter-execute::

    smile = opensmile.Smile(
        feature_set=opensmile.FeatureSet.eGeMAPSv02,
        feature_level=opensmile.FeatureLevel.Functionals,
        loglevel=2,
        logfile='smile.log',
    )
    smile.process_signal(
        signal,
        sampling_rate
    )
    with open('./smile.log', 'r') as fp:
        log = fp.readlines()
    log

Custom config
-------------

We can create a custom config.

.. jupyter-execute::

    config_str = '''
    [componentInstances:cComponentManager]
    instance[dataMemory].type=cDataMemory

    ;;; default source
    [componentInstances:cComponentManager]
    instance[dataMemory].type=cDataMemory

    ;;; source

    \{\cm[source{?}:include external source]}

    ;;; main section

    [componentInstances:cComponentManager]
    instance[framer].type = cFramer
    instance[lld].type = cEnergy
    instance[func].type=cFunctionals

    [framer:cFramer]
    reader.dmLevel = wave
    writer.dmLevel = frames
    copyInputName = 1
    frameMode = fixed
    frameSize = 0.025000
    frameStep = 0.010000
    frameCenterSpecial = left
    noPostEOIprocessing = 1

    [lld:cEnergy]
    reader.dmLevel = frames
    writer.dmLevel = lld
    \{\cm[bufferModeRbConf{?}:path to included config to set the buffer mode for the standard ringbuffer levels]}
    nameAppend = energy
    copyInputName = 1
    rms = 1
    log = 1

    [func:cFunctionals]
    reader.dmLevel=lld
    writer.dmLevel=func
    copyInputName = 1
    \{\cm[bufferModeRbConf]}
    \{\cm[frameModeFunctionalsConf{?}:path to included config to set frame mode for all functionals]}
    functionalsEnabled=Moments
    Moments.variance = 0
    Moments.stddev = 1
    Moments.skewness = 0
    Moments.kurtosis = 0
    Moments.amean = 1
    Moments.doRatioLimit = 0

    ;;; sink

    \{\cm[sink{?}:include external sink]}

    '''

It's important to always set the
``source`` and ``sink`` as we did above.
But we are free in choosing the levels.
In the above we have added two
levels ``'func'`` and ``'lld'``.
Now, we simply pass the level
we are interested in.

.. jupyter-execute::

    with open('my.conf', 'w') as fp:
        fp.write(config_str)

    smile = opensmile.Smile(
        feature_set='my.conf',
        feature_level='func',
    )
    smile.process_signal(
        signal,
        sampling_rate
    )

And...

.. jupyter-execute::

    smile = opensmile.Smile(
        feature_set='my.conf',
        feature_level='lld',
    )
    smile.process_signal(
        signal,
        sampling_rate,
    )

Resample
--------

It's possible to resample the
input signals on the fly.

.. jupyter-execute::

    smile = opensmile.Smile(
        feature_set=opensmile.FeatureSet.eGeMAPSv02,
        feature_level=opensmile.FeatureLevel.Functionals,
        sampling_rate=8000,
        resample=True,
    )
    smile.process_signal(
        signal,
        sampling_rate,
    )

Multi-channel
-------------

We can process multi-channel audio.
Note that we need to set the channels
we want to process when we create
the feature extractor.

.. jupyter-execute::

    smile = opensmile.Smile(
        feature_set=opensmile.FeatureSet.eGeMAPSv02,
        feature_level=opensmile.FeatureLevel.Functionals,
        channels=[0, -1],  # process first and last channel
    )
    signal = np.concatenate([signal, signal, signal], axis=0)
    smile.process_signal(
        signal,
        sampling_rate,
    )

File input
----------

We can extract features from files.
Note that we only process
the first ten seconds of the files

.. jupyter-execute::

    files = db.files  # pick files
    smile = opensmile.Smile(
        feature_set=opensmile.FeatureSet.eGeMAPSv02,
        feature_level=opensmile.FeatureLevel.Functionals,
    )
    smile.process_files(
        files,
        ends=['2s'] * len(files),
        root=db.root,
    )

audformat
---------

We can extract features from an index
in the `audformat`_.
Note that we set five workers
to speed up the processing.

.. jupyter-execute::

    index = db['emotion'].index  # pick table index
    smile = opensmile.Smile(
        feature_set=opensmile.FeatureSet.eGeMAPSv02,
        feature_level=opensmile.FeatureLevel.Functionals,
        num_workers=5,
    )
    smile.process_index(
        index,
        root=db.root,
    )


.. _audformat: https://audeering.github.io/audformat/data-format.html
.. _emodb: https://github.com/audeering/emodb
.. _openSMILE: https://gitlab.audeering.com/tools/opensmile
