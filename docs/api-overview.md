# API Overview

Complete reference for the `qsp_filter` public API.
All functions listed here are importable directly from `qsp_filter` or from their
respective sub-modules.

`qsp_filter` is designed for downstream reuse. Consumers import these helpers to
condition signals before FFT analysis, modulation, orientation fusion, or any other
processing step that requires stable, normalized, or bounded inputs.

---

## Smoothing Helpers (`qsp_filter.smoothing`)

Smoothing helpers reduce high-frequency variation in real-valued signals. Note that
`moving_average` and `weighted_moving_average` **shorten** the output sequence;
`exponential_moving_average` **preserves** the input length.

### `moving_average(values, window_size)`

Sliding-window simple moving average.
Delegates to `qsp.filters.moving_average` (qsp-core).

| Parameter | Type | Description |
|---|---|---|
| `values` | `Iterable[float]` | Input signal |
| `window_size` | `int` | Window length (positive, ≤ signal length) |

**Returns** `list[float]` — length `len(values) - window_size + 1`

---

### `weighted_moving_average(values, weights)`

Weighted sliding-window average. Each window position is averaged using the
provided per-sample weights. Useful when more recent or more central samples
should contribute more to the smoothed value.

| Parameter | Type | Description |
|---|---|---|
| `values` | `Iterable[float]` | Input signal |
| `weights` | `Iterable[float]` | Non-negative per-sample weights |

**Returns** `list[float]` — length `len(values) - len(weights) + 1`

---

### `exponential_moving_average(values, alpha)`

Exponential moving average (EMA) with smoothing factor `alpha`.
Higher `alpha` tracks the input more closely; lower `alpha` smooths more heavily.
Length-preserving: the first output equals the first input sample.

| Parameter | Type | Description |
|---|---|---|
| `values` | `Iterable[float]` | Input signal |
| `alpha` | `float` | Smoothing factor in `(0, 1]` |

**Returns** `list[float]` — same length as input

---

## Normalization Helpers (`qsp_filter.normalization`)

Normalization helpers rescale signals for downstream consistency. All three helpers
return **all zeros** when the input has no variation (constant signal or zero vector).
This is a safe, predictable fallback that prevents division-by-zero errors.

### `min_max_normalize(values)`

Scale signal to the range `[0, 1]`.
Returns all zeros when the signal is constant.

| Parameter | Type | Description |
|---|---|---|
| `values` | `Iterable[float]` | Input signal (non-empty) |

**Returns** `list[float]` — all values in `[0, 1]`

---

### `z_score_normalize(values)`

Standardize signal to zero mean and unit variance.
Returns all zeros when the standard deviation is zero.

| Parameter | Type | Description |
|---|---|---|
| `values` | `Iterable[float]` | Input signal (non-empty) |

**Returns** `list[float]`

---

### `l2_normalize(values)`

Scale signal so its Euclidean (L2) norm equals one.
Returns all zeros when the signal is the zero vector.

| Parameter | Type | Description |
|---|---|---|
| `values` | `Iterable[float]` | Input signal (non-empty) |

**Returns** `list[float]` — unit L2 norm (or all zeros)

---

## Clipping Helpers (`qsp_filter.clipping`)

Clipping helpers bound signal values to prevent downstream overflow or saturation.
Hard clipping is useful for strict range enforcement; soft clipping provides a smooth
saturation curve that avoids abrupt discontinuities.

### `clip_signal(values, minimum, maximum)`

Hard-clip each sample to `[minimum, maximum]`.
Delegates to `qsp.filters.clip` (qsp-core).

| Parameter | Type | Description |
|---|---|---|
| `values` | `Iterable[float]` | Input signal |
| `minimum` | `float` | Lower bound |
| `maximum` | `float` | Upper bound (≥ minimum) |

**Returns** `list[float]` — all values in `[minimum, maximum]`

---

### `soft_clip_signal(values, limit=1.0)`

Smooth saturation using a scaled hyperbolic tangent:
`output[t] = limit * tanh(input[t] / limit)`

Unlike hard clipping, soft clipping gradually compresses large values rather than
truncating them, which preserves more signal shape near the boundary.

| Parameter | Type | Description |
|---|---|---|
| `values` | `Iterable[float]` | Input signal |
| `limit` | `float` | Saturation level, default `1.0` (must be positive) |

**Returns** `list[float]` — all values in the open interval `(-limit, limit)`

---

## Utility Helpers (`qsp_filter.utils`)

These are **internal** validation helpers shared across `qsp_filter` modules.
They are not part of the public API surface and may change without notice.

- `ensure_non_empty(values, name)` — raises `ValueError` if the sequence is empty
- `ensure_positive_int(value, name)` — raises `ValueError` if the value is not a
  positive integer
- `ensure_non_negative_weights(weights)` — raises `ValueError` if any weight is
  negative

Downstream code should not import directly from `qsp_filter.utils`.

---

## Top-Level Imports

All public functions are re-exported from `qsp_filter` directly:

```python
from qsp_filter import (
    # Smoothing
    moving_average,
    weighted_moving_average,
    exponential_moving_average,
    # Normalization
    min_max_normalize,
    z_score_normalize,
    l2_normalize,
    # Clipping
    clip_signal,
    soft_clip_signal,
)
```
