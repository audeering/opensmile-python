from __future__ import annotations

from collections.abc import Callable
from collections.abc import Sequence
import errno
import os
import warnings

import numpy as np
import pandas as pd

import audeer
import audinterface
import audobject

from opensmile.core.config import config
from opensmile.core.define import FeatureLevel
from opensmile.core.define import FeatureLevelResolver
from opensmile.core.define import FeatureSet
from opensmile.core.define import FeatureSetResolver
from opensmile.core.lib import FrameMetaData
from opensmile.core.lib import OpenSMILE


class Smile(audinterface.Feature, audobject.Object):
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

    .. note:: The following arguments are not serialized:

        * ``keep_nat``
        * ``loglevel``
        * ``logfile``
        * ``num_workers``
        * ``multiprocessing``
        * ``segment``
        * ``verbose``

        For more information see section on `hidden arguments`_.

    Args:
        feature_set: default feature set or path to a custom config file
        feature_level: default feature level or level name if a custom
            config file is used
        options: dictionary with optional script parameters
        loglevel: log level (0-5), the higher the number the more log
            messages are given
        logfile: if not ``None`` log messages will be stored to this file
        sampling_rate: sampling rate in Hz.
            If ``None`` it will call ``process_func`` with the actual
            sampling rate of the signal.
        channels: channel selection, see :func:`audresample.remix`
        mixdown: apply mono mix-down on selection
        resample: if ``True`` enforces given sampling rate by resampling
        segment: when a :class:`audinterface.Segment` object is provided,
            it will be used to find a segmentation of the input signal.
            Afterwards processing is applied to each segment
        keep_nat: if the end of segment is set to ``NaT`` do not replace
            with file duration in the result
        num_workers: number of parallel jobs or 1 for sequential
            processing. If ``None`` will be set to the number of
            processors on the machine multiplied by 5 in case of
            multithreading and number of processors in case of
            multiprocessing
        multiprocessing: use multiprocessing instead of multithreading
        verbose: show debug messages

    Examples:
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

    .. _`hidden arguments`: https://audeering.github.io/audobject/usage.html#hidden-arguments

    """  # noqa: E501

    @audobject.init_decorator(
        borrow={
            "sampling_rate": "process",
            "channels": "process",
            "mixdown": "process",
            "resample": "process",
        },
        hide=[
            "keep_nat",
            "logfile",
            "loglevel",
            "num_workers",
            "multiprocessing",
            "segment",
            "verbose",
        ],
        resolvers={
            "feature_set": FeatureSetResolver,
            "feature_level": FeatureLevelResolver,
        },
    )
    @audeer.deprecated_keyword_argument(
        deprecated_argument="num_channels",
        removal_version="0.13.0",
        new_argument="channels",
        mapping=lambda x: range(x),
    )
    def __init__(
        self,
        feature_set: str | FeatureSet = FeatureSet.ComParE_2016,
        feature_level: str | FeatureLevel = FeatureLevel.Functionals,
        *,
        options: dict = None,
        loglevel: int = 2,
        logfile: str = None,
        sampling_rate: int = None,
        channels: int | Sequence[int] = 0,
        mixdown: bool = False,
        resample: bool = False,
        segment: audinterface.Segment = None,
        keep_nat: bool = False,
        num_workers: int | None = 1,
        multiprocessing: bool = False,
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
            name="smile",
            params=None,
            process_func=self._extract,
            num_workers=num_workers,
            sampling_rate=sampling_rate,
            resample=resample,
            channels=channels,
            mixdown=mixdown,
            segment=segment,
            keep_nat=keep_nat,
            multiprocessing=multiprocessing,
            verbose=verbose,
        )
        self.params = self.to_dict(flatten=True)

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
        r"""Check if feature set is deprecated."""
        deprecated_feature_sets = {  # deprecated: recommended
            FeatureSet.GeMAPS: FeatureSet.GeMAPSv01b,
            FeatureSet.GeMAPSv01a: FeatureSet.GeMAPSv01b,
            FeatureSet.eGeMAPS: FeatureSet.eGeMAPSv01b,
            FeatureSet.eGeMAPSv01a: FeatureSet.eGeMAPSv02,
            FeatureSet.eGeMAPSv01b: FeatureSet.eGeMAPSv02,
        }
        if (
            type(self.feature_set) is FeatureSet
            and self.feature_set in deprecated_feature_sets
        ):
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
        signal = signal.copy()
        signal *= 32768
        signal = signal.astype(np.int16)

        ys = []
        starts = []
        ends = []

        for x in signal:
            y = []
            starts = []
            ends = []

            options = self._options()
            options["source"] = os.path.join(
                self.default_config_root, config.EXTERNAL_INPUT_CONFIG
            )
            options["sampleRate"] = sampling_rate
            options["nBits"] = 16

            smile = self._smile(options=options)
            smile.external_sink_set_callback_ex(
                config.EXTERNAL_OUTPUT_COMPONENT, Smile._sink_callback(y, starts, ends)
            )
            smile.external_audio_source_write_data(
                config.EXTERNAL_SOURCE_COMPONENT, bytes(x)
            )
            smile.external_audio_source_set_eoi(config.EXTERNAL_SOURCE_COMPONENT)
            smile.run()
            smile.free()

            if not y:
                warnings.warn(UserWarning("Segment too short, filling with NaN."))
                y.append(np.ones(self.num_features) * np.nan)
                starts.append(0)
                ends.append(signal.size / sampling_rate)

            starts = np.vstack(starts).squeeze()
            ends = np.vstack(ends).squeeze()
            if starts.shape:
                starts = pd.to_timedelta(starts, "s")
                ends = pd.to_timedelta(ends, "s")
            else:
                starts = pd.TimedeltaIndex([pd.to_timedelta(starts, "s")])
                ends = pd.TimedeltaIndex([pd.to_timedelta(ends, "s")])

            y = np.vstack(y)
            ys.append(y)

        return starts, ends, np.concatenate(ys, axis=1)

    def _feature_names(self) -> list[str]:
        r"""Read feature names from config file."""
        options = self._options()
        options["source"] = os.path.join(
            self.default_config_root, config.EXTERNAL_INPUT_CONFIG
        )
        smile = self._smile(options=options)
        num_elements = smile.external_sink_get_num_elements(
            config.EXTERNAL_OUTPUT_COMPONENT
        )
        names = [
            smile.external_sink_get_element_name(config.EXTERNAL_OUTPUT_COMPONENT, idx)
            for idx in range(num_elements)
        ]
        smile.free()
        return names

    def _options(self) -> dict:
        r"""Fill options dictionary."""
        options = self.options.copy()
        options["sink"] = os.path.join(
            self.default_config_root, config.EXTERNAL_OUTPUT_SINGLE_CONFIG
        )
        if type(self.feature_level) is FeatureLevel:
            options["sinkLevel"] = self.feature_level.value
        else:
            options["sinkLevel"] = self.feature_level
        options["bufferModeRbConf"] = os.path.join(
            self.default_config_root, "shared/BufferModeRb.conf.inc"
        )
        if "frameModeFunctionalsConf" not in options:
            options["frameModeFunctionalsConf"] = os.path.join(
                self.default_config_root, "shared/FrameModeFunctionals.conf.inc"
            )
        return options

    def _series_to_frame(
        self,
        series: pd.Series,
    ) -> pd.DataFrame:
        r"""Convert series to frame.

        Usually, we need to figure out start and end times
        from ``win_dur`` and ``hop_dur``.
        But since openSMILE provides segment times,
        we can skip this step and use them directly.

        """
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
                    names=["file", "start", "end"],
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
                    names=["start", "end"],
                )
                frames[idx] = pd.DataFrame(
                    index=index,
                    data=values,
                    columns=self.column_names,
                )
        return pd.concat(frames, axis="index")

    def _smile(self, options: dict) -> OpenSMILE:
        r"""Set up smile instance."""
        smile = OpenSMILE()
        smile.initialize(
            config_file=self.config_path,
            options=options,
            loglevel=self.loglevel,
            log_file=self.logfile,
            debug=self.verbose,
        )
        return smile

    @staticmethod
    def _sink_callback(
        y: list[np.ndarray], starts: list[float], ends: list[float]
    ) -> Callable[[np.ndarray, FrameMetaData], None]:
        r"""Return callback where features are collected."""

        def callback(data: np.ndarray, meta: FrameMetaData):
            y.append(data.copy())
            starts.append(meta.time)
            ends.append(meta.time + meta.lengthSec)

        return callback

    def __call__(
        self,
        signal: np.ndarray,
        sampling_rate: int,
    ) -> np.ndarray:
        r"""Apply processing to signal.

        This function processes the signal **without** transforming the output
        into a :class:`pd.DataFrame`. Instead it will return the raw processed
        signal. However, if channel selection, mixdown and/or resampling
        is enabled, the signal will be first remixed and resampled if the
        input sampling rate does not fit the expected sampling rate.

        Args:
            signal: signal values
            sampling_rate: sampling rate in Hz

        Returns:
            Processed signal

        Raises:
            RuntimeError: if sampling rates do not match
            RuntimeError: if channel selection is invalid

        """
        # process functions returns (starts, values, values)
        # but we only want to return values here
        y = self.process(signal, sampling_rate)[2]
        # reshape to (channels, features, frames)
        y = y.T.reshape(self.num_channels, self.num_features, -1)
        return y
