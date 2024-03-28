import os

import numpy as np
import pandas as pd
import pytest

import audeer
import audiofile
import audobject

import opensmile


deprecated_feature_sets = [  # deprecated
    opensmile.FeatureSet.GeMAPS,
    opensmile.FeatureSet.GeMAPSv01a,
    opensmile.FeatureSet.eGeMAPS,
    opensmile.FeatureSet.eGeMAPSv01a,
    opensmile.FeatureSet.eGeMAPSv01b,
]

gemaps_family = [  # no deltas
    opensmile.FeatureSet.GeMAPS,
    opensmile.FeatureSet.GeMAPSv01a,
    opensmile.FeatureSet.GeMAPSv01b,
    opensmile.FeatureSet.eGeMAPS,
    opensmile.FeatureSet.eGeMAPSv01a,
    opensmile.FeatureSet.eGeMAPSv01b,
    opensmile.FeatureSet.eGeMAPSv02,
]


@pytest.mark.parametrize(
    "x,sr,num_channels,feature_set,feature_level",
    [
        (
            pytest.WAV_ARRAY,
            pytest.WAV_SR,
            3,
            pytest.CONFIG_FILE,
            opensmile.FeatureLevel.LowLevelDescriptors,
        ),
        (
            pytest.WAV_ARRAY,
            pytest.WAV_SR,
            5,
            pytest.CONFIG_FILE,
            opensmile.FeatureLevel.Functionals,
        ),
    ],
)
def test_channels(x, sr, num_channels, feature_set, feature_level):
    x = np.repeat(x, num_channels, axis=0)

    # create feature extractor with mixdown

    fex = opensmile.Smile(feature_set, feature_level, mixdown=True)
    fex = audobject.from_yaml_s(fex.to_yaml_s())
    assert isinstance(fex, opensmile.Smile)

    y_mono = fex.process_signal(x, sr)

    # create feature extractor for multiple channels

    fex = opensmile.Smile(
        feature_set,
        feature_level,
        channels=range(num_channels),
    )
    fex = audobject.from_yaml_s(fex.to_yaml_s())
    assert isinstance(fex, opensmile.Smile)

    y = fex.process_signal(x, sr)

    # assertions

    assert y_mono.shape[0] == y.shape[0]
    assert y_mono.shape[1] * len(fex.process.channels) == y.shape[1]
    for c in range(num_channels):
        np.testing.assert_equal(
            y.values[:, c * fex.num_features : (c + 1) * fex.num_features],
            y_mono.values,
        )


@pytest.mark.parametrize(
    "config,level",
    [
        (
            pytest.CONFIG_FILE,
            "lld",
        ),
        (
            pytest.CONFIG_FILE,
            "func",
        ),
        pytest.param(
            "invalid.conf",
            "func",
            marks=pytest.mark.xfail(raises=FileNotFoundError),
        ),
    ],
)
def test_custom(config, level):
    # create feature extractor

    fex = opensmile.Smile(config, level)
    fex = audobject.from_yaml_s(fex.to_yaml_s())
    assert isinstance(fex, opensmile.Smile)

    # extract from file

    y_file = fex.process_file(pytest.WAV_FILE)

    # extract from array

    x, sr = audiofile.read(pytest.WAV_FILE)
    y_array = fex.process_signal(x, sr, file=pytest.WAV_FILE)

    # assertions

    assert fex.config_name == audeer.basename_wo_ext(config)
    assert fex.config_path == audeer.safe_path(config)
    assert fex.num_features == len(fex.feature_names)
    assert fex.feature_names == y_file.columns.to_list()
    pd.testing.assert_frame_equal(y_file, y_array)


@pytest.mark.parametrize("feature_set", [x for x in opensmile.FeatureSet])
@pytest.mark.parametrize("feature_level", [x for x in opensmile.FeatureLevel])
def test_default(tmpdir, feature_set, feature_level):
    deltas = feature_level == opensmile.FeatureLevel.LowLevelDescriptors_Deltas

    if (feature_set in gemaps_family) and deltas:
        # deltas not available

        with pytest.raises(ValueError):
            opensmile.Smile(feature_set, feature_level)

    else:
        # create feature extractor

        if feature_set in deprecated_feature_sets:
            with pytest.warns(UserWarning):
                fex = opensmile.Smile(feature_set, feature_level)
                fex = audobject.from_yaml_s(fex.to_yaml_s())
                assert isinstance(fex, opensmile.Smile)
        else:
            fex = opensmile.Smile(feature_set, feature_level)
            fex = audobject.from_yaml_s(fex.to_yaml_s())
            assert isinstance(fex, opensmile.Smile)

        # extract features from file

        y = fex.process_file(pytest.WAV_FILE)

        # run SMILExtract from same file

        source_config_file = os.path.join(
            fex.default_config_root,
            opensmile.config.FILE_INPUT_CONFIG,
        )
        if feature_set in gemaps_family:
            sink_config_file = os.path.join(
                fex.default_config_root,
                opensmile.config.FILE_OUTPUT_CONFIG_NO_LLD_DE,
            )
        else:
            sink_config_file = os.path.join(
                fex.default_config_root,
                opensmile.config.FILE_OUTPUT_CONFIG,
            )
        output_file = os.path.join(tmpdir, f"{feature_level.value}.csv")
        command = (
            f"{pytest.SMILEXTRACT} "
            f"-C {fex.config_path} "
            f"-source {source_config_file} "
            f"-I {pytest.WAV_FILE} "
            f"-sink {sink_config_file} "
            f"-{feature_level.value}_csv_output {output_file}"
        )
        os.system(command)

        # read output of SMILExtract and compare

        df = pd.read_csv(output_file, sep=";")
        np.testing.assert_allclose(df.values[:, 1:], y.values, rtol=1e-6, atol=0)
        assert fex.num_features == len(df.columns) - 1
        assert fex.feature_names == list(df.columns[1:])


@pytest.mark.parametrize("num_files", [1, 5])
@pytest.mark.parametrize(
    "feature_set,feature_level",
    [
        (pytest.CONFIG_FILE, opensmile.FeatureLevel.LowLevelDescriptors),
        (pytest.CONFIG_FILE, opensmile.FeatureLevel.Functionals),
    ],
)
@pytest.mark.parametrize(
    "num_workers, multiprocessing",
    [(1, False), (5, False), (5, True), (None, False)],
)
def test_files(num_files, feature_set, feature_level, num_workers, multiprocessing):
    # create feature extractor

    fex = opensmile.Smile(
        feature_set,
        feature_level,
        num_workers=num_workers,
        multiprocessing=multiprocessing,
    )
    fex = audobject.from_yaml_s(
        fex.to_yaml_s(),
        override_args={
            "num_workers": num_workers,
            "multiprocessing": multiprocessing,
        },
    )
    assert isinstance(fex, opensmile.Smile)

    # extract from single file

    y_file = fex.process_file(pytest.WAV_FILE)

    # extract from files

    y_files = fex.process_files([pytest.WAV_FILE] * num_files)

    # assertions

    np.testing.assert_equal(np.concatenate([y_file] * num_files), y_files.values)


@pytest.mark.parametrize(
    "feature_set,feature_level",
    [
        (
            pytest.CONFIG_FILE,
            opensmile.FeatureLevel.LowLevelDescriptors,
        ),
        (
            pytest.CONFIG_FILE,
            opensmile.FeatureLevel.Functionals,
        ),
    ],
)
@pytest.mark.parametrize(
    "index",
    [
        pd.MultiIndex.from_arrays(
            [
                [pytest.WAV_FILE] * 3,
                pd.to_timedelta([0, 1, 2], unit="s"),
                pd.to_timedelta([1, 2, 3], unit="s"),
            ],
            names=["file", "start", "end"],
        ),
    ],
)
@pytest.mark.parametrize(
    "num_workers, multiprocessing",
    [(1, False), (5, False), (5, True), (None, False)],
)
def test_index(feature_set, feature_level, index, num_workers, multiprocessing):
    # create feature extractor

    fex = opensmile.Smile(
        feature_set,
        feature_level,
        num_workers=num_workers,
        multiprocessing=multiprocessing,
    )
    fex = audobject.from_yaml_s(
        fex.to_yaml_s(),
        override_args={
            "num_workers": num_workers,
            "multiprocessing": multiprocessing,
        },
    )
    assert isinstance(fex, opensmile.Smile)

    # extract from index

    y = fex.process_index(index)

    # extract from files

    files = index.get_level_values(0)
    starts = index.get_level_values(1)
    ends = index.get_level_values(2)
    y_files = fex.process_files(files, starts=starts, ends=ends)

    # assertions

    pd.testing.assert_frame_equal(y, y_files)


@pytest.mark.parametrize(
    "file,feature_set,feature_level",
    [
        (
            pytest.WAV_FILE,
            pytest.CONFIG_FILE,
            opensmile.FeatureLevel.LowLevelDescriptors,
        ),
        (
            pytest.WAV_FILE,
            pytest.CONFIG_FILE,
            opensmile.FeatureLevel.Functionals,
        ),
    ],
)
def test_signal(file, feature_set, feature_level):
    # create feature extractor

    fex = opensmile.Smile(feature_set, feature_level)
    fex = audobject.from_yaml_s(fex.to_yaml_s())
    assert isinstance(fex, opensmile.Smile)

    # extract from numpy array

    x, sr = audiofile.read(file, always_2d=True)
    y = fex.process_signal(x, sr)
    y_file = fex.process_file(file)
    y_call = fex(x, sr)
    with pytest.warns(UserWarning):
        y_empty = fex.process_signal(x[0, :10], sr)

    # assertions

    assert y_call.ndim == 3
    assert fex.feature_names == y.columns.to_list()
    np.testing.assert_equal(y.values, y_file.values)
    np.testing.assert_equal(y.values.squeeze(), y_call.squeeze().T)
    assert all(y_empty.isna())
