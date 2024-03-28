import os
import platform

import setuptools


# Include only the platform specific pre-compiled binary.
# For sources see https://github.com/audeering/opensmile


def platform_name():
    r"""Platform name used in pip tag.

    Expected outcomes are:

    ==================== ======================
    Linux, 64-bit        manylinux_2_17_x86_64
    Raspberry Pi, 32-bit manylinux_2_17_armv7l
    Raspberry Pi, 64-bit manylinux_2_17_aarch64
    Windows              win_amd64
    MacOS Intel          macosx_10_4_x86_64
    MacOS M1             macosx_11_0_arm64
    ==================== ======================

    Under Linux the manylinux version
    can be extracted
    by inspecting the wheel
    with ``auditwheel``.

    Too see all supported tags on your system run:

    .. code-block:: bash

        $ pip debug --verbose

    """
    system = platform.system()
    machine = platform.machine().lower()

    if system == "Linux":  # pragma: no cover
        system = "manylinux_2_17"
    elif system == "Windows":  # pragma: no cover
        system = "win"
    elif system == "Darwin":  # pragma: no cover
        if machine == "x86_64":
            system = "macosx_10_4"
        else:
            system = "macosx_11_0"
    else:  # pragma: no cover
        raise RuntimeError(f"Unsupported platform {system}")

    return f"{system}_{machine}"


# Look for enrionment variable PLAT_NAME
# to be able to enforce
# different platform names
# in CI on the same runner
plat_name = os.environ.get("PLAT_NAME", platform_name())

if "linux" in plat_name:
    library = "*.so"
elif "macos" in plat_name:
    library = "*.dylib"
elif "win" in plat_name:
    library = "*.dll"

setuptools.setup(
    package_data={
        "opensmile.core": [
            f"bin/{plat_name}/{library}",
            "config/compare/*",
            "config/egemaps/v01a/*",
            "config/egemaps/v01b/*",
            "config/egemaps/v02/*",
            "config/emobase/*",
            "config/gemaps/v01a/*",
            "config/gemaps/v01b/*",
            "config/shared/*",
        ],
    },
    # python -m build --wheel
    # does no longer accept the --plat-name option,
    # but we can set the desired platform as an option
    # (https://stackoverflow.com/a/75010995)
    options={
        "bdist_wheel": {"plat_name": plat_name},
    },
)
