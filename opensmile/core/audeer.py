import concurrent.futures
import glob
import os
import typing

import tqdm


class config:
    """Get/set defaults for :mod:`audeer`.

    For example, when you want to change the default number of columns
    for the progress bar::

        import audeer
        audeer.config.TQDM_COLUMNS = 50

    """

    TQDM_DESCLEN = 60
    """Length of progress bar description."""

    TQDM_FORMAT = (
        '{percentage:3.0f}%|{bar} [{elapsed}<{remaining}] '
        '{desc:' + str(TQDM_DESCLEN) + '}'
    )
    """Format of progress bars."""

    TQDM_COLUMNS = 100
    """Number of columns of progress bars."""

    TQDM_LEAVE = False
    """Leave progress bar on screen after finishing."""


config = config()


def format_display_message(
        text: str,
        pbar: bool = False
) -> str:
    """Ensure a fixed length of text printed to screen.

    The length of the text message is the same as the overall
    progress bar length as given by :attr:`audeer.config.TQDM_COLUMNS`.

    Args:
        text: text to be displayed
        pbar: if a progress bar is displayed as well.
            This will shorten the text to the given progress bar
            description length :attr:`audeer.config.TQDM_DESCLEN`

    Returns:
        formatted text message

    Example:
        >>> config.TQDM_COLUMNS = 20
        >>> format_display_message('Long text that will be shorten to fit')
        'Long te...n to fit'

    """
    if not text:
        return text
    if pbar:
        n = config.TQDM_DESCLEN - 2
    else:
        n = config.TQDM_COLUMNS - 2
    if len(text) == n:
        return text
    elif len(text) < n:
        return text.ljust(n)
    else:
        m = (n - 3) // 2
        return f'{text[:m]}...{text[len(text) - (n - m - 3):]}'


def list_file_names(
        path: typing.Union[str, bytes],
        *,
        filetype: str = ''
) -> typing.List:
    """List of file names inferred from provided path.

    Args:
        path: path to file, directory or pattern
        filetype: optional consider only this filetype

    Returns:
        list of path(s) to file(s)

    Example:
        >>> path = mkdir('path1')
        >>> open(os.path.join(path, 'file1'), 'a').close()
        >>> [os.path.basename(p) for p in list_file_names(path)]
        ['file1']

    """
    path = safe_path(path)
    if os.path.isfile(path):
        search_pattern = path
    else:
        if os.path.isdir(path):
            # Ensure / at the end
            path = os.path.join(path, '')
        search_pattern = f'{path}*{filetype}'
    # Get list of files matching search pattern
    file_names = sorted(glob.glob(search_pattern))
    return [f for f in file_names if not os.path.isdir(f)]


def _progress_bar(
        iterable: typing.Sequence = None,
        *,
        total: int = None,
        desc: str = None,
        disable: bool = False
) -> tqdm:
    r"""Progress bar with optional text on the right.

    Args:
        iterable: sequence to iterate through
        total: total number of iterations
        desc: text shown on the right of the progress bar
        disable: don't show the display bar

    Returns:
        progress bar object

    """
    if desc is None:
        desc = ''
    return tqdm.tqdm(
        iterable=iterable,
        ncols=config.TQDM_COLUMNS,
        bar_format=config.TQDM_FORMAT,
        total=total,
        disable=disable,
        desc=format_display_message(desc, pbar=True),
        leave=config.TQDM_LEAVE,
    )


def run_tasks(
        task_func: typing.Callable,
        params: typing.Sequence[
            typing.Tuple[
                typing.Sequence[typing.Any],
                typing.Dict[str, typing.Any],
            ]
        ],
        *,
        num_workers: int = None,
        multiprocessing: bool = False,
        progress_bar: bool = False,
        task_description: str = None
) -> typing.Sequence[typing.Any]:
    r"""Run parallel tasks using multprocessing.

    .. note:: Result values are returned in order of ``params``.

    Args:
        task_func: task function with one or more
            parameters, e.g. ``x, y, z``, and optionally returning a value
        params: sequence of tuples holding parameters for each task.
            Each tuple contains a sequence of positional arguments and a
            dictionary with keyword arguments, e.g.:
            ``[((x1, y1), {'z': z1}), ((x2, y2), {'z': z2}), ...]``
        num_workers: number of parallel jobs or 1 for sequential
            processing. If ``None`` will be set to the number of
            processors on the machine multiplied by 5 in case of
            multithreading and number of processors in case of
            multiprocessing
        multiprocessing: use multiprocessing instead of multithreading
        progress_bar: show a progress bar
        task_description: task description
            that will be displayed next to progress bar

    Example:
        >>> power = lambda x, n: x ** n
        >>> params = [([2, n], {}) for n in range(10)]
        >>> run_tasks(power, params, num_workers=3)
        [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]

    """
    num_tasks = max(1, len(params))
    results = [None] * num_tasks

    if num_workers == 1:  # sequential

        with _progress_bar(
            params,
            total=len(params),
            desc=task_description,
            disable=not progress_bar,
        ) as pbar:
            for index, param in enumerate(pbar):
                results[index] = task_func(*param[0], **param[1])

    else:  # parallel

        if multiprocessing:
            executor = concurrent.futures.ProcessPoolExecutor
        else:
            executor = concurrent.futures.ThreadPoolExecutor
        with executor(max_workers=num_workers) as pool:
            with _progress_bar(
                    total=len(params),
                    desc=task_description,
                    disable=not progress_bar,
            ) as pbar:
                futures = []
                for param in params:
                    future = pool.submit(task_func, *param[0], **param[1])
                    future.add_done_callback(lambda p: pbar.update())
                    futures.append(future)
                for idx, future in enumerate(futures):
                    result = future.result()
                    results[idx] = result

    return results


def safe_path(
        path: typing.Union[str, bytes]
) -> str:
    """Ensure the path is absolute and doesn't include `..` or `~`.

    Args:
        path: path to file, directory

    Returns:
        expanded path

    Example:
        >>> home = safe_path('~')
        >>> path = safe_path('~/path/.././path')
        >>> path[len(home):]
        '/path'

    """
    if path:
        path = os.path.realpath(os.path.expanduser(path))
        # Convert bytes to str, see https://stackoverflow.com/a/606199
        if type(path) == bytes:
            path = path.decode('utf-8').strip('\x00')
    return path

