# Architecture

## Role in the QSP Ecosystem

`qsp-filter` is the **Layer-1 filtering and signal-conditioning primitives library** of the RQM
Technologies Quaternionic Signal Processing (QSP) ecosystem. It provides:

- **Smoothing helpers** — moving average, weighted moving average, exponential moving average
- **Normalization helpers** — min-max normalization, z-score standardization, L2 normalization
- **Clipping helpers** — hard clipping, soft clipping (tanh-based saturation)
- **Lightweight signal-conditioning utilities** — reusable preprocessing tools for use before or
  after analysis steps such as FFT, modulation, or orientation fusion

`qsp-filter` is intended to support higher-level systems as a focused, composable building block.
It does **not** aim to be a general-purpose DSP framework or a full signal-processing application
layer.

## QSP Perspective

Within the QSP ecosystem, filtering is not only about removing unwanted variation. It is about
conditioning structured signals so that orientation, phase, amplitude, and downstream comparisons
remain stable and interpretable. `qsp-filter` provides the small reusable primitives needed for
that conditioning step without absorbing broader application logic.

## Ecosystem Position

`qsp-filter` is a Layer-1 library in the RQM Technologies ecosystem.
It sits directly above `qsp-core` and provides a focused set of signal-filtering
utilities that downstream applications (Layer-2) can depend on.

```
┌─────────────────────────────────────────────────────────────────────────┐
│  Layer 2 – Applications                                                  │
│  eigenclock · quaternionic-modem · quaternionic-navigation              │
└───────────────────────────────┬─────────────────────────────────────────┘
                                │ depends on
┌───────────────────────────────▼─────────────────────────────────────────┐
│  Layer 1 – QSP libraries                                                 │
│  qsp-fft · qsp-filter (THIS REPO) · qsp-modulation · qsp-orientation   │
└───────────────────────────────┬─────────────────────────────────────────┘
                                │ all Layer-1 libs depend on
┌───────────────────────────────▼─────────────────────────────────────────┐
│  qsp-core                                                                │
│  Quaternion · SU(2) · basic clip · basic moving_average · utils         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Boundary

### What belongs in qsp-filter

| Category | Examples |
|---|---|
| Smoothing helpers | moving average, weighted MA, exponential MA |
| Normalization helpers | min-max, z-score, L2 |
| Clipping helpers | hard clip, soft clip |
| Signal-conditioning utilities | validation helpers, scaling helpers |
| Filtering-oriented demos | examples showing smoothing, normalization, clipping workflows |

### What does NOT belong in qsp-filter

| Concern | Correct home |
|---|---|
| Quaternion algebra, SU(2) primitives | `qsp-core` |
| Basic `moving_average`, `clip`, `normalize_signal` | `qsp-core` |
| FFT, IDFT, spectral analysis | `qsp-fft` |
| Digital modulation, IQ processing, symbol mapping | `qsp-modulation` |
| IMU fusion, attitude estimation, frame transforms | `qsp-orientation` |
| Adaptive equalizers, synchronization loops | `quaternionic-modem` or downstream |
| Channel models, communications-specific conditioning | `quaternionic-modem` |
| Application-level navigation or robotics logic | `quaternionic-navigation` |
| Full FIR/IIR filter design frameworks | downstream repos |
| UI dashboards, deployment code, website content | `website` or deployment repos |

`qsp-filter` is a **building-block filtering library**, not a complete signal-processing system.

## Relationship to qsp-core

`qsp-core` is the shared foundation for the entire QSP ecosystem. It provides the `Quaternion`
type, SU(2) helpers, basic `moving_average`, `clip`, and `normalize_signal` primitives, and
low-level validation utilities.

`qsp-filter` builds filtering-specific helpers on top of that foundation:

- Where a qsp-core primitive covers the needed behavior, `qsp-filter` wraps it with local
  validation and re-exports it under filtering-layer semantics (e.g., `clip_signal` delegates to
  `qsp.filters.clip`, `moving_average` delegates to `qsp.filters.moving_average`).
- Where qsp-core does not go far enough, `qsp-filter` provides the additional implementation
  (e.g., weighted moving average, z-score normalization, soft clipping).

This layering is **by design**. qsp-core stays minimal; qsp-filter extends it without duplicating
primitives. See [`dependency-on-qsp-core.md`](dependency-on-qsp-core.md) for the full import map.

## Relationship to qsp-fft, qsp-modulation, and qsp-orientation

These Layer-1 libraries are complementary and are often used together in pipelines, but their
responsibilities must remain distinct:

| Repository | Responsibility |
|---|---|
| **qsp-filter** | Smoothing, normalization, clipping, signal conditioning |
| **qsp-fft** | Spectral transforms, DFT/IDFT, spectrum extraction |
| **qsp-modulation** | Symbol mapping, IQ processing, digital modulation schemes |
| **qsp-orientation** | Attitude estimation, IMU fusion, frame transforms, diagnostics |

A typical pipeline might apply `qsp-filter` smoothing and normalization **before** handing data to
`qsp-fft` for spectral analysis, or **before** `qsp-modulation` for consistent amplitude ranges.

## Module Layout

```
qsp/
└── filter/
    ├── __init__.py        Public API re-exports
    ├── smoothing.py       moving_average, weighted_moving_average,
    │                      exponential_moving_average
    ├── normalization.py   min_max_normalize, z_score_normalize,
    │                      l2_normalize
    ├── clipping.py        clip_signal, soft_clip_signal
    └── utils.py           Internal validation helpers
```

### smoothing.py

Provides three sliding-window smoothing filters for real-valued signals.
`moving_average` delegates to `qsp.filters.moving_average` in qsp-core.
`weighted_moving_average` and `exponential_moving_average` are implemented
here because they go beyond the basic primitive provided by qsp-core.

### normalization.py

Provides three normalization strategies.
No qsp-core delegation is needed because qsp-core's `normalize_signal`
is peak-amplitude normalization (max-abs), whereas the three functions
here (min-max, z-score, L2) are distinct algorithms.

### clipping.py

Provides hard clipping (delegated to `qsp.filters.clip`) and soft clipping
(tanh-based, implemented here).

### utils.py

Internal validation helpers shared across the `qsp.filter` modules.
These helpers are specific to the filtering layer; lower-level validation
utilities live in `qsp.utils` inside qsp-core.

## Filtering Conventions

These conventions must remain stable across versions unless explicitly changed with a version bump:

| Convention | Behavior |
|---|---|
| **Smoothing length** | `moving_average` and `weighted_moving_average` return a **shorter** list (`len - window + 1`); `exponential_moving_average` **preserves length** |
| **Edge handling** | Smoothing helpers do not pad; they reduce length. Callers must account for this. |
| **Normalization output range** | `min_max_normalize` → `[0, 1]`; `z_score_normalize` → zero mean, unit variance; `l2_normalize` → unit Euclidean norm |
| **Constant-input normalization** | All three normalizers return **all zeros** when the input has no variation (constant signal or zero vector) |
| **Hard clip** | Each sample is clamped to `[minimum, maximum]`; delegates to `qsp.filters.clip` |
| **Soft clip** | `limit * tanh(x / limit)`; output is in the open interval `(-limit, +limit)` |
| **Input types** | All helpers accept any `Iterable[float]`; output is always `list[float]` |
| **NumPy arrays** | Accepted as input (treated as iterables); output is `list[float]`, not `ndarray` |

## Downstream Systems

`qsp-filter` is one layer in a larger platform. Higher-level systems that depend on it include:

- **quaternionic-modem** — normalization and clipping for consistent modulation inputs
- **quaternionic-navigation** — smoothing and normalization as sensor-data preprocessing
- **sensor-analysis pipelines** — combine smoothing, normalization, and FFT for diagnostics
- **diagnostics workflows** — clipping and smoothing to protect analysis from transient noise

See [`downstream-usage.md`](downstream-usage.md) for concrete usage patterns.

## Dependency Rules

- `qsp.filter` → `qsp-core` (required runtime dependency)
- `qsp.filter` → nothing else (no optional dependencies in core modules)
- Quaternion and SU(2) primitives must **not** be re-implemented here
- Tests use only the standard library and pytest
