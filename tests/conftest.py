import glob
import os
import sys

import pytest
import pandas as pd

import audeer
import audiofile


def safe_path(path):
    if path:
        path = os.path.realpath(os.path.expanduser(path))
        # Convert bytes to str, see https://stackoverflow.com/a/606199
        if type(path) == bytes:
            path = path.decode('utf-8').strip('\x00')
    return path


pytest.ROOT = os.path.dirname(os.path.realpath(__file__))
pytest.WAV_FILE = os.path.join(pytest.ROOT, 'test.wav')
pytest.WAV_ARRAY, pytest.WAV_SR = audiofile.read(
    pytest.WAV_FILE, always_2d=True,
)
pytest.FRAME_LIST_STARTS = pd.to_timedelta(['1.0s', '3.0s', '4.0s'])
pytest.FRAME_LIST_ENDS = pd.to_timedelta(['1.5s', '3.5s', '5.0s'])
pytest.CONFIG_FILE = os.path.join(pytest.ROOT, 'test.conf')

if sys.platform == "win32":  # pragma: no cover
    platform = 'win'
elif sys.platform == "darwin":  # pragma: no cover
    platform = 'osx'
else:  # pragma: no cover
    platform = 'linux'

pytest.SMILEXTRACT = audeer.safe_path(
    os.path.join(
        pytest.ROOT, '..', 'opensmile', 'core', 'bin', platform, 'SMILExtract'
    )
)


@pytest.fixture(scope='session', autouse=True)
def fixture_clean_session():
    def clean():
        path = os.path.join(pytest.ROOT, '..', '.coverage.*')
        for file in glob.glob(path):
            os.remove(file)
    clean()
    yield
    clean()
