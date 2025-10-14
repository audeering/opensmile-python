from __future__ import annotations

import enum

import audobject


class FeatureSet(enum.Enum):
    r"""Enumeration of standard feature sets.

    The following feature sets are available:

    * :attr:`ComParE_2016`
    * :attr:`GeMAPS`, deprecated alias for :attr:`GeMAPSv01a`
    * :attr:`GeMAPSv01a`
    * :attr:`GeMAPSv01b`
    * :attr:`eGeMAPS`, deprecated alias for :attr:`eGeMAPSv01a`
    * :attr:`eGeMAPSv01a`
    * :attr:`eGeMAPSv01b`
    * :attr:`eGeMAPSv02`
    * :attr:`emobase`
    * :attr:`IS09`
    * :attr:`IS10`
    * :attr:`IS11`
    * :attr:`IS12`
    * :attr:`IS13`

    For references, see the papers on:

    * `ComParE 2016`_
    * GeMAPS_
    * eGeMAPS_
    * emobase_
    * IS09_
    * IS10_
    * IS11_
    * IS12_
    * IS13_

    .. _ComParE 2016:
        https://livrepository.liverpool.ac.uk/3003234/1/is2016_compare.pdf
    .. _GeMAPS:
        https://sail.usc.edu/publications/files/eyben-preprinttaffc-2015.pdf
    .. _eGeMAPS:
        https://sail.usc.edu/publications/files/eyben-preprinttaffc-2015.pdf
    .. _IS09:
        https://opus.bibliothek.uni-augsburg.de/opus4/files/66757/i09_0312.pdf
    .. _IS10:
        https://opus.bibliothek.uni-augsburg.de/opus4/files/66767/i10_2794.pdf
    .. _IS11:
        https://opus.bibliothek.uni-augsburg.de/opus4/files/66989/i11_3201.pdf
    .. _IS12:
        https://opus.bibliothek.uni-augsburg.de/opus4/files/66988/i12_0254.pdf
    .. _IS13:
        http://www5.informatik.uni-erlangen.de/Forschung/Publikationen/2013/Schuller13-TI2.pdf

    """

    ComParE_2016 = "compare/ComParE_2016"
    GeMAPS = "gemaps/v01a/GeMAPSv01a"  # legacy
    GeMAPSv01a = "gemaps/v01a/GeMAPSv01a"
    GeMAPSv01b = "gemaps/v01b/GeMAPSv01b"
    eGeMAPS = "egemaps/v01a/eGeMAPSv01a"  # legacy
    eGeMAPSv01a = "egemaps/v01a/eGeMAPSv01a"
    eGeMAPSv01b = "egemaps/v01b/eGeMAPSv01b"
    eGeMAPSv02 = "egemaps/v02/eGeMAPSv02"
    emobase = "emobase/emobase"
    IS09 = "is09-13/IS09_emotion"
    IS10 = "is09-13/IS10_paraling_compat"
    IS11 = "is09-13/IS11_speaker_state"
    IS12 = "is09-13/IS12_speaker_trait_compat"
    IS13 = "is09-13/IS13_ComParE"


class FeatureSetResolver(audobject.resolver.Base):
    r"""Custom value resolver for :class:`opensmile.FeatureSet`."""

    def decode(self, value: str) -> str | FeatureSet:
        if value in FeatureSet.__members__:
            value = FeatureSet[value]
        return value

    def encode(self, value: str | FeatureSet) -> str:
        if isinstance(value, FeatureSet):
            value = str(value).split(".")[-1]
        return value

    def encode_type(self):
        return str


class FeatureLevel(enum.Enum):
    r"""Enumeration of standard feature levels.

    * :attr:`LowLevelDescriptors` - low-level descriptors (LLD) calculated
      over a sliding window
    * :attr:`LowLevelDescriptors_Deltas` - Delta regression of LLDs
    * :attr:`Functionals` - statistical functionals mapping variable series of
      LLDs to static values

    For more information see https://mediatum.ub.tum.de/doc/1082431/1082431.pdf

    """

    LowLevelDescriptors = "lld"
    LowLevelDescriptors_Deltas = "lld_de"
    Functionals = "func"


class FeatureLevelResolver(audobject.resolver.Base):
    r"""Custom value resolver for :class:`opensmile.FeatureLevel`."""

    def decode(self, value: str) -> str | FeatureLevel:
        if value in FeatureLevel.__members__:
            value = FeatureLevel[value]
        return value

    def encode(self, value: str | FeatureLevel) -> str:
        if isinstance(value, FeatureLevel):
            value = str(value).split(".")[-1]
        return value

    def encode_type(self):
        return str
