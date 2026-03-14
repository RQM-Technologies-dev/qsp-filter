<img src="https://github.com/RQM-Technologies-dev/qsp-filter/actions/workflows/ci.yml/badge.svg">

# qsp-filter

`qsp-filter` is the **Layer-1 filtering and signal-conditioning primitives library** of the RQM
Technologies Quaternionic Signal Processing (QSP) ecosystem. It is built on
[`qsp-core`](https://github.com/RQM-Technologies-dev/qsp-core) and provides smoothing,
normalization, and clipping utilities for real-valued signals.

---

## Role in the QSP Ecosystem

`qsp-filter` is the QSP ecosystem's dedicated home for reusable filtering-oriented primitives.
It provides:

- **Smoothing helpers** — moving average, weighted moving average, exponential moving average
- **Normalization helpers** — min-max normalization, z-score standardization, L2 normalization
- **Clipping helpers** — hard clipping, soft clipping (tanh-based saturation)
- **Lightweight signal-conditioning utilities** — reusable preprocessing tools used before or
  after analysis steps such as FFT, modulation, or orientation fusion

`qsp-filter` is intended to support higher-level systems as a focused building block. It does
**not** aim to be a general-purpose DSP framework or a full signal-processing application layer.

---

## QSP Perspective

Within the QSP ecosystem, filtering is not only about removing unwanted variation. It is about
conditioning structured signals so that orientation, phase, amplitude, and downstream comparisons
remain stable and interpretable. `qsp-filter` provides the small reusable primitives needed for
that conditioning step without absorbing broader application logic.

---

## Why This Repo Matters

Signal conditioning is a prerequisite in most analytical workflows:

- **Before spectral analysis** — smoothing reduces noise that would otherwise corrupt FFT output
  in `qsp-fft`
- **Before modulation or comparison** — normalization ensures consistent amplitude ranges before
  `qsp-modulation` processing or correlation
- **In diagnostics pipelines** — clipping and smoothing protect downstream stages from transient
  spikes and outliers
- **In communications, sensing, and autonomy** — lightweight preprocessing helpers are the
  foundation of reproducible analysis pipelines in systems such as `quaternionic-modem` and
  `quaternionic-navigation`

Because these operations appear at the start of nearly every signal-processing workflow, having
them in a small, focused, well-tested package reduces duplication across the QSP ecosystem and
provides a stable dependency surface for downstream repositories.

---

## Ecosystem Context

```
RQM-Technologies
├── qsp-core          ← shared math primitives (Quaternion, SU(2), basic filters)
├── qsp-fft           ← spectral transforms built on qsp-core
├── qsp-filter        ← THIS REPO: filtering / signal-conditioning primitives
├── qsp-modulation    ← modulation library built on qsp-core
├── qsp-orientation   ← attitude estimation, IMU fusion, frame transforms
├── eigenclock
├── quaternionic-modem        ← Layer-2 communications system
├── quaternionic-navigation   ← Layer-2 navigation system
├── website
├── documentation
└── research-notebooks
```

Quaternion primitives and SU(2) helpers belong in `qsp-core`, not here.
`qsp-filter` imports those primitives and focuses exclusively on filtering and
signal-conditioning logic.

---

## Boundary

### What belongs in qsp-filter

| Category | Examples |
|---|---|
| Smoothing helpers | moving average, weighted MA, exponential MA |
| Normalization helpers | min-max, z-score, L2 |
| Clipping helpers | hard clip, soft clip |
| Signal-conditioning utilities | length-preserving or length-reducing filters, scaling helpers |
| Filtering-oriented demos | examples showing smoothing, normalization, clipping workflows |

### What does NOT belong in qsp-filter

| Concern | Correct home |
|---|---|
| Quaternion algebra, SU(2) primitives | `qsp-core` |
| Basic `moving_average`, `clip`, `normalize_signal` | `qsp-core` |
| FFT, IDFT, spectral analysis | `qsp-fft` |
| Digital modulation, IQ processing, symbol mapping | `qsp-modulation` |
| IMU fusion, attitude estimation, frame transforms | `qsp-orientation` |
| Adaptive equalizers, synchronization loops | downstream or sibling repos |
| Channel models, communications-specific conditioning | `quaternionic-modem` |
| Application-level navigation or robotics logic | `quaternionic-navigation` |
| Full FIR/IIR filter design frameworks | downstream repos |
| UI dashboards, deployment code, website content | `website` or deployment repos |

`qsp-filter` is a **building-block filtering library**, not a complete signal-processing system.

---

## Relationship to qsp-core

`qsp-core` is the shared foundation for the entire QSP ecosystem. It provides:

- The `Quaternion` type and SU(2) helpers
- Basic `moving_average`, `clip`, and `normalize_signal` primitives
- Shared low-level validation utilities

`qsp-filter` builds **filtering-specific helpers** on top of that foundation. Where a qsp-core
primitive covers the needed behavior (e.g., simple moving average, hard clip), `qsp-filter`
wraps it with local validation and re-exports it under filtering-layer semantics. Where qsp-core
does not go far enough (e.g., weighted averages, z-score normalization, soft clipping), `qsp-filter`
provides the additional implementation.

This layering is **by design**: qsp-core stays minimal, and qsp-filter extends it without
duplicating primitives. See [`docs/dependency-on-qsp-core.md`](docs/dependency-on-qsp-core.md)
for details.

---

## Relationship to qsp-fft, qsp-modulation, and qsp-orientation

These Layer-1 libraries are complementary and are often used together in pipelines, but their
responsibilities must remain distinct:

| Repository | Responsibility |
|---|---|
| **qsp-filter** | Smoothing, normalization, clipping, signal conditioning |
| **qsp-fft** | Spectral transforms, DFT/IDFT, spectrum extraction |
| **qsp-modulation** | Symbol mapping, IQ processing, digital modulation schemes |
| **qsp-orientation** | Attitude estimation, IMU fusion, frame transforms, diagnostics |

A typical pipeline might apply `qsp-filter` smoothing and normalization **before** handing data
to `qsp-fft` for spectral analysis, or **before** `qsp-modulation` for consistent amplitude
ranges. `qsp-orientation` may use `qsp-filter` helpers as preprocessing steps for sensor fusion.

---

## Filtering Conventions

| Convention | Behavior |
|---|---|
| **Smoothing length** | `moving_average` and `weighted_moving_average` return a **shorter** list than the input (`len - window + 1`); `exponential_moving_average` **preserves length** |
| **Edge handling** | Smoothing helpers do not pad; they reduce length. Callers must account for this. |
| **Normalization output range** | `min_max_normalize` → `[0, 1]`; `z_score_normalize` → zero mean, unit variance; `l2_normalize` → unit Euclidean norm |
| **Constant-input normalization** | All three normalizers return **all zeros** when the input has no variation (constant signal or zero vector) |
| **Hard clip** | Each sample is clamped to `[minimum, maximum]`; delegates to `qsp.filters.clip` |
| **Soft clip** | `limit * tanh(x / limit)`; output is in the open interval `(-limit, +limit)` |
| **Input types** | All helpers accept any `Iterable[float]`; output is always `list[float]` |
| **NumPy arrays** | Accepted as input (treated as iterables); output is `list[float]`, not `ndarray` |

---

## Downstream Systems

`qsp-filter` is one layer in a larger platform. Higher-level systems that depend on it include:

- **quaternionic-modem** — uses normalization and clipping for consistent modulation inputs
- **quaternionic-navigation** — uses smoothing and normalization as sensor-data preprocessing
- **sensor-analysis pipelines** — combine smoothing, normalization, and FFT for diagnostics
- **diagnostics workflows** — use clipping and smoothing to protect analysis from transient noise
- **preprocessing chains** — assemble `qsp-filter`, `qsp-fft`, `qsp-modulation`, and
  `qsp-orientation` tools into full analysis pipelines

See [`docs/downstream-usage.md`](docs/downstream-usage.md) for concrete usage patterns.

---

## Future Extensions

Appropriate future additions to `qsp-filter`:

- Additional smoothing kernels (Gaussian window, median filter)
- Rolling statistics helpers (rolling variance, rolling RMS)
- Robust normalization helpers (percentile-based scaling)
- Outlier-resistant clipping utilities
- Simple signal denoising helpers
- Reusable signal-scaling utilities

Work that must **not** be added here because it belongs elsewhere:

| Capability | Correct destination |
|---|---|
| Adaptive equalizers, synchronization loops | `quaternionic-modem` or downstream |
| Spectral estimators, filter-bank design | `qsp-fft` |
| Communications-specific channel conditioning | `quaternionic-modem` |
| Full FIR/IIR filter design | downstream repos |
| Application-level control or robotics logic | `quaternionic-navigation` or downstream |
| Hardware-specific pipelines | downstream or deployment repos |

See [`docs/repo-roadmap.md`](docs/repo-roadmap.md) for the versioned roadmap.

---

## What belongs here vs. in qsp-core

| Concern | Where it lives |
|---|---|
| `Quaternion` type, SU(2) helpers | `qsp-core` |
| Basic `moving_average`, `clip`, `normalize_signal` | `qsp-core` |
| Spectral transforms (DFT/IDFT) | `qsp-fft` |
| Weighted & exponential moving averages | **qsp-filter** |
| Min-max, z-score, L2 normalization | **qsp-filter** |
| Hard clip, soft clip | **qsp-filter** |

## Publishing

Releases are automatically published to PyPI using GitHub Actions and PyPI Trusted Publishing.
Release artifacts are also attached to GitHub Releases.

## Installation

```bash
pip install qsp-filter
```

## Package structure

```
qsp/
└── filter/
    ├── __init__.py        ← public API surface
    ├── smoothing.py       ← moving_average, weighted_moving_average, exponential_moving_average
    ├── normalization.py   ← min_max_normalize, z_score_normalize, l2_normalize
    ├── clipping.py        ← clip_signal, soft_clip_signal
    └── utils.py           ← shared validation helpers (filtering layer only)
```

## Running tests

```bash
pip install pytest
pytest tests/
```

## Running examples

```bash
python examples/smoothing_demo.py
python examples/normalization_demo.py
```

## Docs

- [`docs/architecture.md`](docs/architecture.md) – ecosystem placement, boundaries, filtering conventions
- [`docs/api-overview.md`](docs/api-overview.md) – public function signatures grouped by category
- [`docs/dependency-on-qsp-core.md`](docs/dependency-on-qsp-core.md) – what is imported from qsp-core and why
- [`docs/downstream-usage.md`](docs/downstream-usage.md) – how downstream systems use qsp-filter
- [`docs/repo-roadmap.md`](docs/repo-roadmap.md) – appropriate future additions and contribution checklist
