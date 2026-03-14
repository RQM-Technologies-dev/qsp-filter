"""Clipping utilities for real-valued signals.

Depends on qsp-core for the basic hard-clip primitive.
This module adds a soft-clip (tanh-based) variant.
"""

from __future__ import annotations

import math
from typing import Iterable

from qsp.filters import clip as _core_clip

from .utils import ensure_real_number, ensure_real_sequence


def clip_signal(values: Iterable[float], minimum: float, maximum: float) -> list[float]:
    """Hard-clip each sample to the inclusive range ``[minimum, maximum]``.

    Delegates to ``qsp.filters.clip`` from qsp-core.

    Parameters
    ----------
    values:
        Input signal as an iterable of real numbers.
    minimum:
        Lower bound of the clipping range.
    maximum:
        Upper bound of the clipping range. Must be >= *minimum*.

    Returns
    -------
    list[float]
        Signal with every sample clamped to ``[minimum, maximum]``.
    """
    ensure_real_number(minimum, name="minimum")
    ensure_real_number(maximum, name="maximum")
    return _core_clip(values, minimum, maximum)


def soft_clip_signal(values: Iterable[float], limit: float = 1.0) -> list[float]:
    """Soft-clip a signal using a scaled hyperbolic tangent.

    Each sample is mapped through ``limit * tanh(sample / limit)``, which
    smoothly saturates toward ``±limit`` without a hard discontinuity.

    Parameters
    ----------
    values:
        Input signal as an iterable of real numbers.
    limit:
        Saturation level. Must be a positive real number. Defaults to ``1.0``.

    Returns
    -------
    list[float]
        Soft-clipped signal with all samples in ``(-limit, limit)``.
    """
    signal = ensure_real_sequence(values, name="values")
    lim = ensure_real_number(limit, name="limit")
    if lim <= 0.0:
        raise ValueError("limit must be a positive real number")
    return [lim * math.tanh(sample / lim) for sample in signal]
