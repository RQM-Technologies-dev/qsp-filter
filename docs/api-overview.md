# API Overview

Complete reference for the `qsp_filter` public API.
All functions are importable directly from `qsp_filter` or from their
respective sub-modules.

---

## Smoothing (`qsp_filter.smoothing`)

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

Weighted sliding-window average.

| Parameter | Type | Description |
|---|---|---|
| `values` | `Iterable[float]` | Input signal |
| `weights` | `Iterable[float]` | Non-negative per-sample weights |

**Returns** `list[float]` — length `len(values) - len(weights) + 1`

---

### `exponential_moving_average(values, alpha)`

Exponential moving average (EMA) with smoothing factor `alpha`.

| Parameter | Type | Description |
|---|---|---|
| `values` | `Iterable[float]` | Input signal |
| `alpha` | `float` | Smoothing factor in `(0, 1]` |

**Returns** `list[float]` — same length as input

---

## Normalization (`qsp_filter.normalization`)

### `min_max_normalize(values)`

Scale signal to the range `[0, 1]`.
Returns all zeros when the signal is constant.

| Parameter | Type | Description |
|---|---|---|
| `values` | `Iterable[float]` | Input signal (non-empty) |

**Returns** `list[float]`

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

**Returns** `list[float]`

---

## Clipping (`qsp_filter.clipping`)

### `clip_signal(values, minimum, maximum)`

Hard-clip each sample to `[minimum, maximum]`.
Delegates to `qsp.filters.clip` (qsp-core).

| Parameter | Type | Description |
|---|---|---|
| `values` | `Iterable[float]` | Input signal |
| `minimum` | `float` | Lower bound |
| `maximum` | `float` | Upper bound (≥ minimum) |

**Returns** `list[float]`

---

### `soft_clip_signal(values, limit=1.0)`

Smooth saturation using a scaled hyperbolic tangent:
`output[t] = limit * tanh(input[t] / limit)`

| Parameter | Type | Description |
|---|---|---|
| `values` | `Iterable[float]` | Input signal |
| `limit` | `float` | Saturation level, default `1.0` (must be positive) |

**Returns** `list[float]` — all values in the open interval `(-limit, limit)`
