import concurrent.futures
import typing

import numpy as np
import pandas as pd

import audeer

import audiofile as af


def check_index(
        index: pd.MultiIndex
):  # pragma: no cover
    if len(index.levels) == 2:
        if not index.empty:
            if not pd.core.dtypes.common.is_datetime_or_timedelta_dtype(
                    index.levels[0]
            ):
                raise ValueError(f'Level 0 has type '
                                 f'{type(index.levels[0].dtype)}'
                                 f', expected timedelta64[ns].')
            if not pd.core.dtypes.common.is_datetime_or_timedelta_dtype(
                    index.levels[1]
            ):
                raise ValueError(f'Level 1 has type '
                                 f'{type(index.levels[1].dtype)}'
                                 f', expected timedelta64[ns].')
    elif len(index.levels) == 3:
        if not index.names == ('file', 'start', 'end'):
            raise ValueError('Not a segmented index conform to Unified Format')
        if not index.empty:
            if not pd.core.dtypes.common.is_datetime_or_timedelta_dtype(
                    index.levels[1]
            ):
                raise ValueError(f'Level 1 has type '
                                 f'{type(index.levels[1].dtype)}'
                                 f', expected timedelta64[ns].')
            if not pd.core.dtypes.common.is_datetime_or_timedelta_dtype(
                    index.levels[2]
            ):
                raise ValueError(f'Level 2 has type '
                                 f'{type(index.levels[2].dtype)}'
                                 f', expected timedelta64[ns].')
    else:
        raise ValueError(f'Index has {len(index.levels)} levels, '
                         f'expected 2 or 3.')


def read_audio(
        path: str,
        start: pd.Timedelta = None,
        end: pd.Timedelta = None,
        channel: int = None,
) -> typing.Tuple[np.ndarray, int]:  # pragma: no cover
    """Reads (segment of an) audio file.

    Args:
        path: path to audio file
        start: read from this position
        end: read until this position
        channel: channel number

    Returns:
        signal: array with signal values in shape ``(channels, samples)``
        sampling_rate: sampling rate in Hz

    """
    if start is None or pd.isna(start):
        offset = 0
    else:
        offset = start.total_seconds()

    if end is None or pd.isna(end):
        duration = None
    else:
        duration = end.total_seconds() - offset

    # load raw audio
    signal, sampling_rate = af.read(
        audeer.safe_path(path),
        always_2d=True,
        offset=offset,
        duration=duration,
    )

    # mix down
    if channel is not None:
        if channel < 0 or channel >= signal.shape[0]:
            raise ValueError(
                f'We need 0<=channel<{signal.shape[0]}, '
                f'but we have channel={channel}.'
            )
        signal = signal[channel, :]

    return signal, sampling_rate


def segment_to_indices(
        signal: np.ndarray,
        sampling_rate: int,
        start: pd.Timedelta,
        end: pd.Timedelta,
) -> typing.Tuple[int, int]:  # pragma: no cover
    if pd.isna(end):
        end = pd.to_timedelta(
            signal.shape[-1] / sampling_rate, unit='sec'
        )
    max_i = signal.shape[-1]
    start_i = int(round(start.total_seconds() * sampling_rate))
    start_i = min(start_i, max_i)
    end_i = int(round(end.total_seconds() * sampling_rate))
    end_i = min(end_i, max_i)
    return start_i, end_i


def segments_to_indices(
        signal: np.ndarray,
        sampling_rate: int,
        index: pd.MultiIndex,
) -> typing.Tuple[
    typing.Sequence[int], typing.Sequence[int]
]:  # pragma: no cover
    starts_i = [0] * len(index)
    ends_i = [0] * len(index)
    for idx, (start, end) in enumerate(index):
        start_i, end_i = segment_to_indices(signal, sampling_rate, start, end)
        starts_i[idx] = start_i
        ends_i[idx] = end_i
    return starts_i, ends_i
