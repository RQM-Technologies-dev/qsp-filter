"""Shared validation helpers for qsp.filter modules.

Only helpers that clearly belong in the filtering layer belong here.
Quaternion and SU(2) utilities belong in qsp-core.
"""

from __future__ import annotations

from numbers import Real
from typing import Iterable


def ensure_real_sequence(values: Iterable[float], *, name: str, allow_empty: bool = False) -> tuple[float, ...]:
    """Validate and return a real-valued sequence as a tuple of floats."""
    try:
        items = tuple(float(value) for value in values)
    except (TypeError, ValueError) as error:
        raise TypeError(f"{name} must be an iterable of real numbers") from error

    if not allow_empty and not items:
        raise ValueError(f"{name} must not be empty")
    return items


def ensure_positive_int(value: int, *, name: str) -> int:
    """Validate that *value* is a positive integer."""
    if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
        raise ValueError(f"{name} must be a positive integer")
    return value


def ensure_real_number(value: Real, *, name: str) -> float:
    """Validate and return a real number as a float."""
    if not isinstance(value, Real) or isinstance(value, bool):
        raise TypeError(f"{name} must be a real number")
    return float(value)
