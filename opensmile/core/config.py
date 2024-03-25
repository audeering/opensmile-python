class config:
    r"""Get/set defaults for the :mod:`opensmile` module."""

    CONFIG_ROOT = "config"
    """Root directory of config files."""

    CONFIG_EXT = ".conf"
    """Extension of config files."""

    EXTERNAL_SOURCE_COMPONENT = "extsource"
    """Standard component name for external input."""

    EXTERNAL_OUTPUT_COMPONENT = "extsink"
    """Standard component name for external data output."""

    FILE_INPUT_CONFIG = "shared/standard_wave_input.conf.inc"
    """Standard config name for wave input from file."""

    EXTERNAL_INPUT_CONFIG = "shared/standard_external_wave_input.conf.inc"
    """Standard config name for external wave input."""

    EXTERNAL_OUTPUT_SINGLE_CONFIG = (
        "shared/standard_external_data_output_single.conf.inc"
    )
    """Standard config name for external data output from a single level."""

    EXTERNAL_OUTPUT_MULTI_CONFIG = "shared/standard_external_data_output_multi.conf.inc"
    """Standard config name for external data output from multiple levels."""

    FILE_OUTPUT_CONFIG = "shared/standard_data_output.conf.inc"
    """Standard config name for external data output."""

    FILE_OUTPUT_CONFIG_NO_LLD_DE = "shared/standard_data_output_no_lld_de.conf.inc"
    """Standard config name for external data output without lld_de level."""
