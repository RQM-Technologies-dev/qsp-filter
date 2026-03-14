"""Smoothing filters for real-valued signals.

Depends on qsp-core for the basic moving_average primitive.
This module extends qsp-core with weighted and exponential variants.
"""

from __future__ import annotations

from typing import Iterable

from qsp.filters import moving_average as _core_moving_average

from .utils import ensure_positive_int, ensure_real_number, ensure_real_sequence


def moving_average(values: Iterable[float], window_size: int) -> list[float]:
    """Return the sliding-window moving average of a real-valued signal.

    Delegates to ``qsp.filters.moving_average`` from qsp-core.

    Parameters
    ----------
    values:
        Input signal as an iterable of real numbers.
    window_size:
        Number of samples per window. Must be a positive integer no greater
        than the signal length.

    Returns
    -------
    list[float]
        A list of ``len(values) - window_size + 1`` averaged samples.
    """
    ensure_positive_int(window_size, name="window_size")
    return _core_moving_average(values, window_size)


def weighted_moving_average(values: Iterable[float], weights: Iterable[float]) -> list[float]:
    """Return the weighted moving average of a real-valued signal.

    Each output sample is the dot product of the corresponding window and
    *weights*, divided by the sum of *weights*.

    Parameters
    ----------
    values:
        Input signal as an iterable of real numbers.
    weights:
        Per-sample weights. The window size is ``len(weights)``. All weights
        must be non-negative and at least one must be positive.

    Returns
    -------
    list[float]
        A list of ``len(values) - len(weights) + 1`` smoothed samples.
    """
    signal = ensure_real_sequence(values, name="values")
    w = ensure_real_sequence(weights, name="weights")

    if any(wi < 0 for wi in w):
        raise ValueError("all weights must be non-negative")
    weight_sum = sum(w)
    if weight_sum == 0.0:
        raise ValueError("at least one weight must be positive")

    window_size = len(w)
    if window_size > len(signal):
        raise ValueError("len(weights) must not exceed the signal length")

    return [
        sum(signal[i + j] * w[j] for j in range(window_size)) / weight_sum
        for i in range(len(signal) - window_size + 1)
    ]


def exponential_moving_average(values: Iterable[float], alpha: float) -> list[float]:
    """Return the exponential moving average (EMA) of a real-valued signal.

    The EMA is computed as::

        ema[0] = signal[0]
        ema[t] = alpha * signal[t] + (1 - alpha) * ema[t - 1]

    Parameters
    ----------
    values:
        Input signal as an iterable of real numbers.
    alpha:
        Smoothing factor in the open interval ``(0, 1]``. A value close to 1
        gives little smoothing; a value close to 0 gives heavy smoothing.

    Returns
    -------
    list[float]
        EMA values with the same length as the input signal.
    """
    signal = ensure_real_sequence(values, name="values")
    a = ensure_real_number(alpha, name="alpha")
    if not (0.0 < a <= 1.0):
        raise ValueError("alpha must be in the range (0, 1]")

    result: list[float] = []
    for sample in signal:
        if not result:
            result.append(sample)
        else:
            result.append(a * sample + (1.0 - a) * result[-1])
    return result
