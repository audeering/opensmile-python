from opensmile.core.config import config
from opensmile.core.define import FeatureLevel
from opensmile.core.define import FeatureSet
from opensmile.core.smile import Smile


__all__ = []


__version__ = "unknown"

# Dynamically get the version of the installed module
try:
    import importlib.metadata

    __version__ = importlib.metadata.version(__name__)
except Exception:  # pragma: no cover
    importlib = None  # pragma: no cover
finally:
    del importlib
