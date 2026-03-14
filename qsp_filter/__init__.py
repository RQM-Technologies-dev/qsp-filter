"""qsp_filter – filtering layer of the RQM Technologies QSP ecosystem.

This package provides smoothing, normalization, and clipping utilities for
real-valued signals. It depends on ``qsp-core`` for shared quaternion math
and basic filtering primitives.

Typical usage::

    from qsp_filter.smoothing import exponential_moving_average
    from qsp_filter.normalization import z_score_normalize
    from qsp_filter.clipping import soft_clip_signal

Public API surface
------------------
Smoothing
    moving_average, weighted_moving_average, exponential_moving_average

Normalization
    min_max_normalize, z_score_normalize, l2_normalize

Clipping
    clip_signal, soft_clip_signal
"""

from .clipping import clip_signal, soft_clip_signal
from .normalization import l2_normalize, min_max_normalize, z_score_normalize
from .smoothing import exponential_moving_average, moving_average, weighted_moving_average

__all__ = [
    "clip_signal",
    "exponential_moving_average",
    "l2_normalize",
    "min_max_normalize",
    "moving_average",
    "soft_clip_signal",
    "weighted_moving_average",
    "z_score_normalize",
]
