import os
import typing

import numpy as np
import pandas as pd

import audeer

import opensmile.core.utils as utils


class Process:  # pragma: no cover
    r"""Processing interface.

    Args:
        process_func: processing function,
            which expects the two positional arguments ``signal``
            and ``sampling_rate``
            and any number of additional keyword arguments.
        keep_nat: if the end of segment is set to ``NaT`` do not replace
            with file duration in the result
        num_workers: number of parallel jobs or 1 for sequential
            processing. If ``None`` will be set to the number of
            processors on the machine multiplied by 5 in case of
            multithreading and number of processors in case of
            multiprocessing
        multiprocessing: use multiprocessing instead of multithreading
        verbose: show debug messages
        kwargs: additional keyword arguments to the processing function

    """
    def __init__(
            self,
            *,
            process_func: typing.Callable[..., typing.Any] = None,
            keep_nat: bool = False,
            num_workers: typing.Optional[int] = 1,
            multiprocessing: bool = False,
            verbose: bool = False,
            **kwargs,
    ):
        self.keep_nat = keep_nat
        self.num_workers = num_workers
        self.multiprocessing = multiprocessing
        self.verbose = verbose
        if process_func is None:
            def process_func(signal, _):
                return signal
        self.process_func = process_func
        self.process_func_kwargs = kwargs

    def _process_file(
            self,
            file: str,
            *,
            start: pd.Timedelta = None,
            end: pd.Timedelta = None,
            channel: int = None,
    ) -> pd.Series:

        signal, sampling_rate = self.read_audio(
            file,
            channel=channel,
            start=start,
            end=end,
        )
        y = self._process_signal(
            signal,
            sampling_rate,
            file=file,
        )

        if start is None or pd.isna(start):
            start = y.index.levels[1][0]
        if end is None or (pd.isna(end) and not self.keep_nat):
            end = y.index.levels[2][0] + start

        y.index = y.index.set_levels([[start], [end]], [1, 2])

        return y

    def process_file(
            self,
            file: str,
            *,
            start: pd.Timedelta = None,
            end: pd.Timedelta = None,
            channel: int = None,
    ) -> pd.Series:
        r"""Process the content of an audio file.

        Args:
            file: file path
            start: start processing at this position
            end: end processing at this position
            channel: channel number

        Returns:
            Series with processed file

        """
        return self._process_file(
            file, start=start, end=end, channel=channel,
        )

    def process_files(
            self,
            files: typing.Sequence[str],
            *,
            starts: typing.Sequence[pd.Timedelta] = None,
            ends: typing.Sequence[pd.Timedelta] = None,
            channel: int = None,
    ) -> pd.Series:
        r"""Process a list of files.

        Args:
            files: list of file paths
            channel: channel number
            starts: list with start positions
            ends: list with end positions

        Returns:
            Series with processed files

        """
        if starts is None:
            starts = [None] * len(files)
        if ends is None:
            ends = [None] * len(files)

        params = [
            (
                (file, ),
                {'start': start, 'end': end, 'channel': channel},
            ) for file, start, end in zip(files, starts, ends)
        ]
        y = audeer.run_tasks(
            self.process_file,
            params,
            num_workers=self.num_workers,
            multiprocessing=self.multiprocessing,
            progress_bar=self.verbose,
            task_description=f'Process {len(files)} files',
        )
        return pd.concat(y)

    def process_folder(
            self,
            root: str,
            *,
            channel: int = None,
            filetype: str = 'wav',
    ) -> pd.Series:
        r"""Process files in a folder.

        .. note:: At the moment does not scan in sub-folders!

        Args:
            root: root folder
            channel: channel number
            filetype: file extension

        Returns:
            Series with processed files

        """
        files = audeer.list_file_names(root, filetype=filetype)
        files = [os.path.join(root, os.path.basename(f)) for f in files]
        return self.process_files(files, channel=channel)

    def _process_signal(
            self,
            signal: np.ndarray,
            sampling_rate: int,
            *,
            file: str = None,
            start: pd.Timedelta = None,
            end: pd.Timedelta = None,
    ) -> pd.Series:

        signal = np.atleast_2d(signal)

        # Find start and end index
        if start is None or pd.isna(start):
            start = pd.to_timedelta(0)
        if end is None or (pd.isna(end) and not self.keep_nat):
            end = pd.to_timedelta(
                signal.shape[-1] / sampling_rate, unit='sec'
            )
        start_i, end_i = utils.segment_to_indices(
            signal, sampling_rate, start, end,
        )

        # Trim signal
        signal = signal[:, start_i:end_i]

        # Process signal
        y = self.process_func(
            signal,
            sampling_rate,
            **self.process_func_kwargs,
        )

        # Create index
        if file is not None:
            index = pd.MultiIndex.from_tuples(
                [(file, start, end)], names=['file', 'start', 'end']
            )
        else:
            index = pd.MultiIndex.from_tuples(
                [(start, end)], names=['start', 'end']
            )

        return pd.Series([y], index)

    def process_signal(
            self,
            signal: np.ndarray,
            sampling_rate: int,
            *,
            file: str = None,
            start: pd.Timedelta = None,
            end: pd.Timedelta = None,
    ) -> typing.Any:
        r"""Process audio signal and return result.

        .. note:: If a ``file`` is given, the index of the returned frame
            has levels ``file``, ``start`` and ``end``. Otherwise,
            it consists only of ``start`` and ``end``.

        Args:
            signal: signal values
            sampling_rate: sampling rate in Hz
            file: file path
            start: start processing at this position
            end: end processing at this position

        Returns:
            Series with processed signal

        """
        return self._process_signal(
            signal, sampling_rate, file=file, start=start, end=end,
        )

    def read_audio(
            self,
            path: str,
            start: pd.Timedelta = None,
            end: pd.Timedelta = None,
            channel: int = None,
    ):
        return utils.read_audio(path, start, end, channel)


class Feature:  # pragma: no cover
    r"""Feature extraction interface.

    The features are returned as a :class:`pd.DataFrame`.
    If your input signal is of size ``(num_channels, num_time_steps)``,
    the returned dataframe will have ``num_channels * num_features``
    columns.
    It will have one row per file or signal.
    If features are extracted using a sliding window,
    each window will be stored as one row.
    If ``win_dur`` is specified ``start`` and ``end`` indices
    are referred from the original ``start`` and ``end`` arguments
    and the window positions.
    Otherwise, the original ``start`` and ``end`` indices
    are kept.

    Args:
        feature_names: features are stored as columns in a data frame,
            this defines the names of the columns
        process_func: feature extraction function,
            which expects the two positional arguments ``signal``
            and ``sampling_rate``
            and any number of additional keyword arguments.
            The function must return features in the shape of
            ``(num_channels, num_features)``
            or ``(num_channels, num_features, num_time_steps)``.
        num_channels: the expected number of channels
        keep_nat: if the end of segment is set to ``NaT`` do not replace
            with file duration in the result
        num_workers: number of parallel jobs or 1 for sequential
            processing. If ``None`` will be set to the number of
            processors on the machine multiplied by 5 in case of
            multithreading and number of processors in case of
            multiprocessing
        multiprocessing: use multiprocessing instead of multithreading
        verbose: show debug messages
        kwargs: additional keyword arguments to the processing function

    """
    def __init__(
            self,
            feature_names: typing.Sequence[str],
            *,
            process_func: typing.Callable[..., np.ndarray] = None,
            num_channels: int = 1,
            keep_nat: bool = False,
            num_workers: typing.Optional[int] = 1,
            multiprocessing: bool = False,
            verbose: bool = False,
            **kwargs,
    ):
        self.process = Process(
            process_func=process_func,
            keep_nat=keep_nat,
            num_workers=num_workers,
            multiprocessing=multiprocessing,
            verbose=verbose,
            **kwargs,
        )
        self.num_channels = num_channels
        self.num_features = len(feature_names)
        self.feature_names = list(feature_names)
        if num_channels > 1:
            self.column_names = []
            for channel in range(num_channels):
                self.column_names.extend(
                    [f'{name}-{channel}' for name in feature_names]
                )
        else:
            self.column_names = self.feature_names
        self.verbose = verbose

    def process_file(
            self,
            file: str,
            *,
            start: pd.Timedelta = None,
            end: pd.Timedelta = None,
            channel: int = None,
    ) -> pd.DataFrame:
        r"""Extract features from an audio file.

        Args:
            file: file path
            channel: channel number
            start: start processing at this position
            end: end processing at this position

        Raises:
            RuntimeError: if number of channels do not match

        """
        series = self.process.process_file(
            file, start=start, end=end, channel=channel,
        )
        return self._series_to_frame(series)

    def process_files(
            self,
            files: typing.Sequence[str],
            *,
            starts: typing.Sequence[pd.Timedelta] = None,
            ends: typing.Sequence[pd.Timedelta] = None,
            channel: int = None,
    ) -> pd.DataFrame:
        r"""Extract features for a list of files.

        Args:
            files: list of file paths
            starts: list with start positions
            ends: list with end positions
            channel: channel number

        Raises:
            RuntimeError: if number of channels do not match

        """
        series = self.process.process_files(
            files, starts=starts, ends=ends, channel=channel,
        )
        return self._series_to_frame(series)

    def process_folder(
            self,
            root: str,
            *,
            filetype: str = 'wav',
            channel: int = None,
    ) -> pd.DataFrame:
        r"""Extract features from files in a folder.

        .. note:: At the moment does not scan in sub-folders!

        Args:
            root: root folder
            filetype: file extension
            channel: channel number

        Raises:
            RuntimeError: if number of channels do not match

        """
        files = audeer.list_file_names(root, filetype=filetype)
        files = [os.path.join(root, os.path.basename(f)) for f in files]
        return self.process_files(files, channel=channel)

    def process_signal(
            self,
            signal: np.ndarray,
            sampling_rate: int,
            *,
            file: str = None,
            start: pd.Timedelta = None,
            end: pd.Timedelta = None,
    ) -> pd.DataFrame:
        r"""Extract features for an audio signal.

        .. note:: If a ``file`` is given, the index of the returned frame
            has levels ``file``, ``start`` and ``end``. Otherwise,
            it consists only of ``start`` and ``end``.

        Args:
            signal: signal values
            sampling_rate: sampling rate in Hz
            file: file path
            start: start processing at this position
            end: end processing at this position

        Raises:
            RuntimeError: if number of channels do not match

        """
        series = self.process.process_signal(
            signal,
            sampling_rate,
            file=file,
            start=start,
            end=end,
        )
        return self._series_to_frame(series)

    def _series_to_frame(
            self,
            series: pd.Series,
    ) -> pd.DataFrame:
        raise NotImplementedError()
