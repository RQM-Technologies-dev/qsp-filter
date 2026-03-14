"""Normalization utilities for real-valued signals.

Provides min-max, z-score, and L2 normalizations.
"""

from __future__ import annotations

import math
from typing import Iterable

from .utils import ensure_real_sequence


def min_max_normalize(values: Iterable[float]) -> list[float]:
    """Scale a signal to the range ``[0, 1]`` using min-max normalization.

    If all samples are identical the function returns a list of zeros to avoid
    division by zero.

    Parameters
    ----------
    values:
        Input signal as an iterable of real numbers.

    Returns
    -------
    list[float]
        Normalized signal in ``[0, 1]``.
    """
    signal = ensure_real_sequence(values, name="values")
    lo = min(signal)
    hi = max(signal)
    span = hi - lo
    if span == 0.0:
        return [0.0] * len(signal)
    return [(sample - lo) / span for sample in signal]


def z_score_normalize(values: Iterable[float]) -> list[float]:
    """Standardize a signal to zero mean and unit variance (z-score).

    If the standard deviation is zero (constant signal) the function returns
    a list of zeros.

    Parameters
    ----------
    values:
        Input signal as an iterable of real numbers.

    Returns
    -------
    list[float]
        Signal with mean 0 and standard deviation 1 (when std > 0).
    """
    signal = ensure_real_sequence(values, name="values")
    n = len(signal)
    mean = sum(signal) / n
    variance = sum((sample - mean) ** 2 for sample in signal) / n
    std = math.sqrt(variance)
    if std == 0.0:
        return [0.0] * n
    return [(sample - mean) / std for sample in signal]


def l2_normalize(values: Iterable[float]) -> list[float]:
    """Scale a signal so that its L2 norm equals one.

    If the signal is all zeros the function returns a list of zeros.

    Parameters
    ----------
    values:
        Input signal as an iterable of real numbers.

    Returns
    -------
    list[float]
        Signal whose Euclidean length is 1 (when the input is non-zero).
    """
    signal = ensure_real_sequence(values, name="values")
    norm = math.sqrt(sum(sample ** 2 for sample in signal))
    if norm == 0.0:
        return [0.0] * len(signal)
    return [sample / norm for sample in signal]
