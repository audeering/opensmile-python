import errno
import os
import typing
import warnings

import numpy as np
import pandas as pd

import audeer

import opensmile.core.audinterface as audinterface

from opensmile.core.SMILEapi import (
    OpenSMILE,
    FrameMetaData,
)
from opensmile.core.config import config
from opensmile.core.define import (
    FeatureLevel,
    FeatureSet,
)


class Smile(audinterface.Feature):
    r"""OpenSMILE feature extractor.

    1. You can choose a pre-defined feature set by passing one of
       :class:`opensmile.FeatureSet`

    2. You can also provide a custom config file using the following
       template:

       .. code-block::

           [componentInstances:cComponentManager]
           instance[dataMemory].type=cDataMemory

           ;;; default source
           \{\cm[source{?}:source include config]}

           ;;; add components reading from reader.dmLevel=wave

           ;;; combine features
           [componentInstances:cComponentManager]
           instance[funcconcat].type=cVectorConcat
           [funcconcat:cVectorConcat]
           reader.dmLevel = <feat-1>;<feat-2>;...
           writer.dmLevel = features
           includeSingleElementFields = 1

           ;;; default sink
           \{\cm[sink{?}:include external sink]}

    Args:
        feature_set: default feature set or path to a custom config file
        feature_level: default feature level or level name if a custom
            config file is used
        options: dictionary with optional script parameters
        loglevel: log level (0-5), the higher the number the more log
            messages are given
        logfile: if not ``None`` log messages will be stored to this file
        num_channels: the expected number of channels
        keep_nat: if the end of segment is set to ``NaT`` do not replace
            with file duration in the result
        num_workers: number of parallel jobs or 1 for sequential
            processing
        verbose: show debug messages

    Example:

    >>> sampling_rate = 16000
    >>> signal = np.zeros(sampling_rate)
    >>> smile = Smile(
    ...     feature_set=FeatureSet.ComParE_2016,
    ...     feature_level=FeatureLevel.Functionals,
    ... )
    >>> smile.process_signal(signal, sampling_rate).audspec_lengthL1norm_sma_range
    start   end
    0 days  0 days 00:00:01    0.0
    Name: audspec_lengthL1norm_sma_range, dtype: float32

    """  # noqa: E501
    def __init__(
            self,
            feature_set: typing.Union[
                str, FeatureSet
            ] = FeatureSet.ComParE_2016,
            feature_level: typing.Union[
                str, FeatureLevel
            ] = FeatureLevel.Functionals,
            *,
            options: dict = None,
            loglevel: int = 2,
            logfile: str = None,
            num_channels: int = 1,
            keep_nat: bool = False,
            num_workers: typing.Optional[int] = 1,
            verbose: bool = False,
    ):

        self.feature_level = feature_level
        r"""Standard feature level or sink level in custom config file."""
        self.feature_set = feature_set
        r"""Standard feature set or path to custom config file"""
        self.options = options or {}
        r"""Dictionary with options"""
        self.logfile = audeer.safe_path(logfile) if logfile else None
        r"""Log file"""
        self.loglevel = loglevel
        r"""Log level"""
        self.verbose = verbose

        self._check_deltas_available()

        super().__init__(
            self._feature_names(),
            process_func=self._extract,
            num_workers=num_workers,
            num_channels=num_channels,
            keep_nat=keep_nat,
            multiprocessing=True,
            verbose=verbose,
        )

        self._y = None
        self._starts = None
        self._ends = None

        self._check_deprecated()

    @property
    def default_config_root(self) -> str:
        r"""Return root directory with standard config files."""
        return os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            config.CONFIG_ROOT,
        )

    @property
    def config_name(self) -> str:
        r"""Return name of config file (without file extension)."""
        name, _ = os.path.splitext(os.path.basename(self.config_path))
        return name

    @property
    def config_path(self) -> str:
        r"""Return file path of config file."""

        if type(self.feature_set) is FeatureSet:
            config_path = os.path.join(
                self.default_config_root,
                self.feature_set.value + config.CONFIG_EXT,
            )
        else:
            config_path = audeer.safe_path(self.feature_set)

        if not os.path.exists(config_path):
            raise FileNotFoundError(
                errno.ENOENT,
                os.strerror(errno.ENOENT),
                config_path,
            )

        return config_path

    def _check_deltas_available(self):
        r"""Raise error if deltas are requested for GeMAPS family."""
        if self.feature_set in [
            FeatureSet.GeMAPS,
            FeatureSet.GeMAPSv01a,
            FeatureSet.GeMAPSv01b,
            FeatureSet.eGeMAPS,
            FeatureSet.eGeMAPSv01a,
            FeatureSet.eGeMAPSv01b,
            FeatureSet.eGeMAPSv02,
        ]:
            if self.feature_level == FeatureLevel.LowLevelDescriptors_Deltas:
                raise ValueError(
                    f"Feature level '{self.feature_level.name}' is not "
                    f"available for feature set '{self.feature_set.name}'."
                )

    def _check_deprecated(self):
        r"""Check if feature set is deprecated"""
        deprecated_feature_sets = {  # deprecated: recommended
            FeatureSet.GeMAPS: FeatureSet.GeMAPSv01b,
            FeatureSet.GeMAPSv01a: FeatureSet.GeMAPSv01b,
            FeatureSet.eGeMAPS: FeatureSet.eGeMAPSv02,
            FeatureSet.eGeMAPSv01a: FeatureSet.eGeMAPSv02,
            FeatureSet.eGeMAPSv01b: FeatureSet.eGeMAPSv02,
        }
        if type(self.feature_set) is FeatureSet and \
                self.feature_set in deprecated_feature_sets:
            warnings.warn(
                f"Feature set '{self.feature_set}' is "
                f"deprecated, consider switching to "
                f"'{deprecated_feature_sets[self.feature_set]}'.",
                UserWarning,
            )

    def _extract(
            self,
            signal: np.ndarray,
            sampling_rate: int,
    ) -> (pd.TimedeltaIndex, pd.TimedeltaIndex, np.ndarray):
        r"""Run feature extraction."""

        if signal.shape[0] != self.num_channels:
            raise RuntimeError(
                f"Input signal has {signal.shape[0]} channels, "
                f"but 'num_channels' to set to {self.num_channels}."
            )

        signal = signal.copy()
        signal *= 32768
        signal = signal.astype(np.int16)

        ys = []
        starts = []
        ends = []

        for x in signal:

            self._y = []
            self._starts = []
            self._ends = []

            options = self._options()
            options['source'] = os.path.join(
                self.default_config_root,
                config.EXTERNAL_INPUT_CONFIG
            )
            options['sampleRate'] = sampling_rate
            options['nBits'] = 16

            smile = self._smile(options=options)
            smile.external_audio_source_write_data(
                config.EXTERNAL_SOURCE_COMPONENT, bytes(x)
            )
            smile.external_audio_source_set_eoi(
                config.EXTERNAL_SOURCE_COMPONENT
            )
            smile.run()
            smile.free()

            if not self._y:
                warnings.warn(
                    UserWarning("Segment too short, filling with NaN.")
                )
                self._y.append(np.ones(self.num_features) * np.nan)
                self._starts.append(0)
                self._ends.append(signal.size / sampling_rate)

            starts = np.vstack(self._starts).squeeze()
            ends = np.vstack(self._ends).squeeze()
            if starts.shape:
                starts = pd.to_timedelta(starts, 's')
                ends = pd.to_timedelta(ends, 's')
            else:
                starts = pd.TimedeltaIndex([pd.to_timedelta(starts, 's')])
                ends = pd.TimedeltaIndex([pd.to_timedelta(ends, 's')])

            y = np.vstack(self._y)
            ys.append(y)

        return starts, ends, np.concatenate(ys, axis=1)

    def _feature_names(self) -> typing.List[str]:
        r"""Read feature names from config file."""
        options = self._options()
        options['source'] = os.path.join(
            self.default_config_root,
            config.EXTERNAL_INPUT_CONFIG
        )
        smile = self._smile(options=options)
        num_elements = smile.external_sink_get_num_elements(
            config.EXTERNAL_OUTPUT_COMPONENT
        )
        names = [
            smile.external_sink_get_element_name(
                config.EXTERNAL_OUTPUT_COMPONENT,
                idx) for idx in range(num_elements)
        ]
        smile.free()
        return names

    def _options(self) -> dict:
        r"""Fill options dictionary."""
        options = self.options.copy()
        options['sink'] = os.path.join(
            self.default_config_root,
            config.EXTERNAL_OUTPUT_SINGLE_CONFIG
        )
        if type(self.feature_level) is FeatureLevel:
            options['sinkLevel'] = self.feature_level.value
        else:
            options['sinkLevel'] = self.feature_level
        options['bufferModeRbConf'] = os.path.join(
            self.default_config_root,
            'shared/BufferModeRb.conf.inc'
        )
        if 'frameModeFunctionalsConf' not in options:
            options['frameModeFunctionalsConf'] = os.path.join(
                self.default_config_root,
                'shared/FrameModeFunctionals.conf.inc'
            )
        return options

    def _series_to_frame(
            self,
            series: pd.Series,
    ) -> pd.DataFrame:
        r"""Usually, we need to figure out start and end times from
        ``win_dur`` and ``hop_dur``. But since openSMILE provides segment
        times, we can skip this step and use them directly."""

        frames = [None] * len(series)
        if len(series.index.levels) == 3:
            for idx, ((file, start, end), values) in enumerate(series.items()):
                num = len(values[0])
                files = [file] * num
                starts = values[0] + start
                ends = values[1] + start
                # override first and last timestamp
                starts._values[0] = start
                ends._values[-1] = end
                values = values[2]
                index = pd.MultiIndex.from_arrays(
                    [
                        files,
                        starts,
                        ends,
                    ],
                    names=['file', 'start', 'end'],
                )
                frames[idx] = pd.DataFrame(
                    index=index,
                    data=values,
                    columns=self.column_names,
                )
        else:
            for idx, ((start, end), values) in enumerate(series.items()):
                starts = values[0] + start
                ends = values[1] + start
                # override first and last timestamp
                starts._values[0] = start
                ends._values[-1] = end
                values = values[2]
                index = pd.MultiIndex.from_arrays(
                    [
                        starts,
                        ends,
                    ],
                    names=['start', 'end'],
                )
                frames[idx] = pd.DataFrame(
                    index=index,
                    data=values,
                    columns=self.column_names,
                )
        return pd.concat(frames, axis='index')

    def _smile(self, options: dict) -> OpenSMILE:
        r"""Set up smile instance."""
        smile = OpenSMILE()
        smile.initialize(
            config_file=self.config_path,
            options=options,
            loglevel=self.loglevel,
            log_file=self.logfile,
            debug=self.verbose)
        smile.external_sink_set_callback_ex(
            config.EXTERNAL_OUTPUT_COMPONENT,
            self._sink_callback
        )
        return smile

    def _sink_callback(self, y: np.ndarray, meta: FrameMetaData):
        r"""Callback where features are collected."""
        self._y.append(y.copy())
        self._starts.append(meta.time)
        self._ends.append(meta.time + meta.lengthSec)
