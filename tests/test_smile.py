import os

import numpy as np
import pandas as pd
import pytest

import audiofile
import audeer

import opensmile


deprecated_feature_sets = [  # deprecated: recommended
    opensmile.FeatureSet.GeMAPS,
    opensmile.FeatureSet.GeMAPSv01a,
    opensmile.FeatureSet.eGeMAPS,
    opensmile.FeatureSet.eGeMAPSv01a,
]


@pytest.mark.parametrize('x,sr,num_channels,feature_set,feature_level', [
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
])
def test_channels(x, sr, num_channels, feature_set, feature_level):

    # create feature extractor for single channel

    fex = opensmile.Smile(feature_set, feature_level)

    y_mono = fex.process_signal(x, sr)

    # create feature extractor for multiple channels

    fex = opensmile.Smile(
        feature_set, feature_level, num_channels=num_channels,
    )

    with pytest.raises(RuntimeError):
        fex.process_signal(x, sr)  # channel mismatch
    x = np.repeat(x, num_channels, axis=0)
    y = fex.process_signal(x, sr)

    # assertions

    assert y_mono.shape[0] == y.shape[0]
    assert y_mono.shape[1] * fex.num_channels == y.shape[1]
    for c in range(num_channels):
        np.testing.assert_equal(
            y.values[:, c * fex.num_features:(c + 1) * fex.num_features],
            y_mono.values,
        )


@pytest.mark.parametrize('config,level', [
    (
        pytest.CONFIG_FILE,
        'lld',
    ),
    (
        pytest.CONFIG_FILE,
        'func',
    ),
    pytest.param(
        'invalid.conf',
        'func',
        marks=pytest.mark.xfail(raises=FileNotFoundError),
    ),
])
def test_custom(config, level):

    # create feature extractor

    fex = opensmile.Smile(config, level)

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


@pytest.mark.parametrize(
    'feature_set',
    [
        x for x in opensmile.FeatureSet
    ]
)
@pytest.mark.parametrize(
    'feature_level',
    [
        x for x in opensmile.FeatureLevel
    ]
)
def test_default(tmpdir, feature_set, feature_level):

    # create feature extractor

    if feature_set in deprecated_feature_sets:
        with pytest.warns(UserWarning):
            fex = opensmile.Smile(feature_set, feature_level)
    else:
        fex = opensmile.Smile(feature_set, feature_level)

    # extract features from file

    y = fex.process_file(pytest.WAV_FILE)

    # run SMILExtract from same file

    source_config_file = os.path.join(
        fex.default_config_root,
        opensmile.config.FILE_INPUT_CONFIG,
    )
    sink_config_file = os.path.join(
        fex.default_config_root,
        opensmile.config.FILE_OUTPUT_CONFIG,
    )
    output_file = os.path.join(tmpdir, f'{feature_level.value}.csv')
    command = f'{pytest.SMILEXTRACT} ' \
              f'-C {fex.config_path} ' \
              f'-source {source_config_file} ' \
              f'-I {pytest.WAV_FILE} ' \
              f'-sink {sink_config_file} ' \
              f'-{feature_level.value}_csv_output {output_file}'
    os.system(command)

    # read output of SMILExtract and compare

    df = pd.read_csv(output_file, sep=';')
    np.testing.assert_allclose(df.values[:, 1:],
                               y.values,
                               rtol=1e-6,
                               atol=0)
    assert fex.num_features == len(df.columns) - 1
    assert fex.feature_names == list(df.columns[1:])


@pytest.mark.parametrize('num_files', [
    1, 5
])
@pytest.mark.parametrize('feature_set,feature_level', [
    (
        pytest.CONFIG_FILE,
        opensmile.FeatureLevel.LowLevelDescriptors
    ),
    (
        pytest.CONFIG_FILE,
        opensmile.FeatureLevel.Functionals
    ),
])
@pytest.mark.parametrize('num_workers', [1, 5, None])
def test_files(num_files, feature_set, feature_level, num_workers):

    # create feature extractor

    fex = opensmile.Smile(
        feature_set, feature_level, num_workers=num_workers,
    )

    # extract from single file

    y_file = fex.process_file(pytest.WAV_FILE)

    # extract from files

    y_files = fex.process_files([pytest.WAV_FILE] * num_files)

    # assertions

    np.testing.assert_equal(np.concatenate([y_file] * num_files),
                            y_files.values)


@pytest.mark.parametrize('file,feature_set,feature_level', [
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
])
def test_signal(file, feature_set, feature_level):

    # create feature extractor

    fex = opensmile.Smile(feature_set, feature_level)

    # extract from numpy array

    x, sr = audiofile.read(file, always_2d=True)
    y = fex.process_signal(x, sr)
    y_file = fex.process_file(file)
    with pytest.warns(UserWarning):
        y_empty = fex.process_signal(x[0, :10], sr)

    # assertions

    assert fex.feature_names == y.columns.to_list()
    np.testing.assert_equal(y.values, y_file.values)
    assert all(y_empty.isna())
