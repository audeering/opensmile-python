import glob
import os

import pandas as pd
import pytest

import audeer
import audiofile as af

from opensmile.core.lib import platform_name


pytest.ROOT = os.path.dirname(os.path.realpath(__file__))
pytest.WAV_FILE = os.path.join(pytest.ROOT, "test.wav")
pytest.WAV_ARRAY, pytest.WAV_SR = af.read(pytest.WAV_FILE, always_2d=True)
pytest.FRAME_LIST_STARTS = pd.to_timedelta(["1.0s", "3.0s", "4.0s"])
pytest.FRAME_LIST_ENDS = pd.to_timedelta(["1.5s", "3.5s", "5.0s"])
pytest.CONFIG_FILE = os.path.join(pytest.ROOT, "test.conf")

plat_name = platform_name()
if "linux" in plat_name:
    library = "libSMILEapi.so"
elif "macos" in plat_name:
    library = "libSMILEapi.dylib"
elif "win" in plat_name:
    library = "SMILEapi.dll"

pytest.SMILEXTRACT = audeer.path(
    pytest.ROOT,
    "..",
    "opensmile",
    "core",
    "bin",
    plat_name,
    "SMILExtract",
)


@pytest.fixture(scope="session", autouse=True)
def fixture_clean_session():
    def clean():
        path = os.path.join(pytest.ROOT, "..", ".coverage.*")
        for file in glob.glob(path):
            os.remove(file)

    clean()
    yield
    clean()
