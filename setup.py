import os
from setuptools import setup


package_data = {
    'opensmile': [
        'core/bin/*',
        'core/config/shared/*',
        'core/config/compare/*',
        'core/config/gemaps/v01a/*',
        'core/config/gemaps/v01b/*',
        'core/config/egemaps/v01a/*',
        'core/config/egemaps/v01b/*',
    ]
}

setup(
    use_scm_version=True,
    package_data=package_data
)
