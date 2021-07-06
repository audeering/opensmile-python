from setuptools import setup


package_data = {
    'opensmile': [
        'core/bin/linux/*',
        'core/bin/osx/*',
        'core/bin/win/*',
        'core/config/compare/*',
        'core/config/egemaps/v01a/*',
        'core/config/egemaps/v01b/*',
        'core/config/egemaps/v02/*',
        'core/config/emobase/*',
        'core/config/gemaps/v01a/*',
        'core/config/gemaps/v01b/*',
        'core/config/shared/*',
    ]
}

setup(
    use_scm_version=True,
    package_data=package_data
)
