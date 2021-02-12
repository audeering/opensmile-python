import enum
import typing


class FeatureSet(enum.Enum):
    r""" Enumeration of standard feature sets.

    The following feature sets are available:

    * :attr:`ComParE_2016`
    * :attr:`GeMAPS`, deprecated alias for :attr:`GeMAPSv01a`
    * :attr:`GeMAPSv01a`
    * :attr:`GeMAPSv01b`
    * :attr:`eGeMAPS`, deprecated alias for :attr:`eGeMAPSv01a`
    * :attr:`eGeMAPSv01a`
    * :attr:`eGeMAPSv01b`
    * :attr:`eGeMAPSv02`

    For references, see the papers on:

    * `ComParE 2016`_
    * GeMAPS_
    * eGeMAPS_

    .. _ComParE 2016:
        http://www.tangsoo.de/documents/Publications/Schuller16-TI2.pdf
    .. _GeMAPS:
        https://sail.usc.edu/publications/files/eyben-preprinttaffc-2015.pdf
    .. _eGeMAPS:
        https://sail.usc.edu/publications/files/eyben-preprinttaffc-2015.pdf

    """
    ComParE_2016 = 'compare/ComParE_2016'
    GeMAPS = 'gemaps/v01a/GeMAPSv01a'  # legacy
    GeMAPSv01a = 'gemaps/v01a/GeMAPSv01a'
    GeMAPSv01b = 'gemaps/v01b/GeMAPSv01b'
    eGeMAPS = 'egemaps/v01a/eGeMAPSv01a'   # legacy
    eGeMAPSv01a = 'egemaps/v01a/eGeMAPSv01a'
    eGeMAPSv01b = 'egemaps/v01b/eGeMAPSv01b'
    eGeMAPSv02 = 'egemaps/v02/eGeMAPSv02'


class FeatureLevel(enum.Enum):
    r""" Enumeration of standard feature levels.

    * :attr:`LowLevelDescriptors` - low-level descriptors (LLD) calculated
      over a sliding window
    * :attr:`LowLevelDescriptors_Deltas` - Delta regression of LLDs
    * :attr:`Functionals` - statistical functionals mapping variable series of
      LLDs to static values

    For more information see https://mediatum.ub.tum.de/doc/1082431/1082431.pdf

    """
    LowLevelDescriptors = 'lld'
    LowLevelDescriptors_Deltas = 'lld_de'
    Functionals = 'func'
