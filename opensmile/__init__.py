from opensmile.core.config import config
from opensmile.core.define import (
    FeatureSet,
    FeatureLevel,
)
from opensmile.core.smile import (
    Smile,
)


__all__ = []


__version__ = 'unknown'

# Dynamically get the version of the installed module
try:
    import pkg_resources
    __version__ = pkg_resources.get_distribution(__name__).version
except Exception:  # pragma: no cover
    pkg_resources = None  # pragma: no cover
finally:
    del pkg_resources
