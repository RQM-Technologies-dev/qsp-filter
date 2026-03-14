# Downstream Usage

This document explains how downstream systems and pipelines may use `qsp-filter`
as a building block.

---

## Overview

`qsp-filter` provides the QSP ecosystem's reusable filtering and signal-conditioning
primitives. Higher-level repositories and pipelines consume these helpers to stabilize,
normalize, and bound signals before or after more complex analysis steps.

`qsp-filter` is intentionally small. It does not provide FFT, modulation, orientation,
or application-level logic. Downstream systems assemble those capabilities from the
appropriate sibling repositories.

---

## Responsibility Matrix

| Repository | Responsibility | Typical relation to qsp-filter |
|---|---|---|
| **qsp-core** | Quaternion math, SU(2), basic filters | Foundation; qsp-filter extends it |
| **qsp-filter** | Smoothing, normalization, clipping | This repo |
| **qsp-fft** | Spectral transforms, DFT/IDFT | Consumes qsp-filter output |
| **qsp-modulation** | Symbol mapping, IQ processing | Consumes qsp-filter output |
| **qsp-orientation** | Attitude estimation, IMU fusion, frame transforms | May use qsp-filter for preprocessing |
| **quaternionic-modem** | Layer-2 communications system | Composes qsp-filter + qsp-modulation |
| **quaternionic-navigation** | Layer-2 navigation system | Composes qsp-filter + qsp-orientation |

---

## Common Usage Patterns

### Smoothing before FFT analysis

Apply a moving average before passing a signal to `qsp-fft` to reduce noise that
would otherwise widen spectral peaks or raise the noise floor.

```python
from qsp_filter import moving_average
from qsp.transforms import dft  # qsp-fft

raw_signal = [...]
smoothed = moving_average(raw_signal, window_size=5)
spectrum = dft(smoothed)
```

### Normalizing modulation inputs

Normalize a signal to `[0, 1]` or zero mean / unit variance before passing it to
`qsp-modulation` to ensure consistent amplitude ranges across batches.

```python
from qsp_filter import min_max_normalize

raw_signal = [...]
normalized = min_max_normalize(raw_signal)
# pass `normalized` to qsp-modulation processing
```

### Clipping sensor values before diagnostics

Clip sensor readings to a known safe range before running diagnostics to prevent
transient spikes from corrupting statistics.

```python
from qsp_filter import clip_signal

sensor_data = [...]
safe_data = clip_signal(sensor_data, minimum=-1.0, maximum=1.0)
# pass `safe_data` to diagnostics pipeline
```

### Soft clipping for smooth saturation

Use soft clipping when abrupt truncation would create artifacts. The tanh-based
saturation curve gracefully compresses large values.

```python
from qsp_filter import soft_clip_signal

signal = [...]
saturated = soft_clip_signal(signal, limit=0.8)
```

### Combining qsp-filter with qsp-orientation

A sensor fusion pipeline might smooth raw IMU data before passing it to orientation
estimation helpers in `qsp-orientation`.

```python
from qsp_filter import exponential_moving_average

raw_imu = [...]
smoothed_imu = exponential_moving_average(raw_imu, alpha=0.3)
# pass `smoothed_imu` to qsp-orientation fusion helpers
```

### Full preprocessing chain

A complete preprocessing chain might combine smoothing, normalization, and clipping
before handing data to spectral or modulation analysis.

```python
from qsp_filter import (
    exponential_moving_average,
    z_score_normalize,
    clip_signal,
)

raw = [...]
smoothed = exponential_moving_average(raw, alpha=0.2)
normalized = z_score_normalize(smoothed)
bounded = clip_signal(normalized, minimum=-3.0, maximum=3.0)
# `bounded` is ready for qsp-fft or qsp-modulation
```

---

## What qsp-filter Does Not Provide

Downstream systems that need the following must use the appropriate sibling repository:

| Capability | Use instead |
|---|---|
| Spectral transforms, DFT/IDFT | `qsp-fft` |
| Symbol mapping, IQ modulation | `qsp-modulation` |
| Attitude estimation, IMU fusion | `qsp-orientation` |
| Adaptive equalizers | `quaternionic-modem` or downstream |
| Application-level control logic | `quaternionic-navigation` or downstream |

---

## Version Stability

The public API of `qsp-filter` is designed to be stable. Filtering conventions
(output lengths, normalization ranges, soft-clip semantics) are documented in
[`architecture.md`](architecture.md) and must not change without a version bump.
Downstream systems may depend on these conventions remaining consistent.
