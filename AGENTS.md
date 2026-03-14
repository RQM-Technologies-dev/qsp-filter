# RQM Technologies – Agent Instructions

This repository is the **Layer-1 filtering and signal-conditioning primitives library** of the
RQM Technologies QSP ecosystem, built on `qsp-core`.

## Role of this repository

`qsp-filter` provides the QSP ecosystem's reusable filtering-oriented primitives:

- **Smoothing helpers** — moving average, weighted moving average, exponential moving average
- **Normalization helpers** — min-max normalization, z-score standardization, L2 normalization
- **Clipping helpers** — hard clipping, soft clipping (tanh-based saturation)
- **Lightweight signal-conditioning utilities** — validation helpers and reusable preprocessing
  tools used before or after analysis steps

It depends on `qsp-core` for quaternion math, SU(2) helpers, and basic filter/validation
utilities. It must remain small, focused, composable, and dependency-light.

## Ecosystem architecture

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

Full ecosystem:

```
RQM-Technologies
├── qsp-core          ← shared math primitives (Quaternion, SU(2), basic filters)
├── qsp-fft           ← spectral transforms built on qsp-core
├── qsp-filter        ← filtering / signal-conditioning primitives  (THIS REPO)
├── qsp-modulation    ← modulation library built on qsp-core
├── qsp-orientation   ← attitude estimation, IMU fusion, frame transforms
├── eigenclock
├── quaternionic-modem        ← Layer-2 communications system
├── quaternionic-navigation   ← Layer-2 navigation system
├── website
├── documentation
└── research-notebooks
```

## Boundary discipline

**What belongs here:**

- Smoothing filters (moving average, weighted moving average, exponential moving average)
- Normalization utilities (min-max, z-score, L2)
- Clipping utilities (hard clip, soft clip)
- Shared validation helpers specific to the filtering layer
- Filtering-oriented demos and examples

**What does NOT belong here:**

| Concern | Correct home |
|---|---|
| Quaternion algebra, SU(2) primitives | `qsp-core` (`qsp.quaternion`, `qsp.su2`) |
| Basic `moving_average`, `clip`, `normalize_signal` | `qsp-core` (`qsp.filters`) |
| FFT, IDFT, spectral analysis | `qsp-fft` |
| Digital modulation, IQ processing, symbol mapping | `qsp-modulation` |
| IMU fusion, attitude estimation, frame transforms | `qsp-orientation` |
| Adaptive equalizers, synchronization loops | `quaternionic-modem` or downstream |
| Channel models, communications-specific conditioning | `quaternionic-modem` |
| Application-level navigation or robotics logic | `quaternionic-navigation` |
| Full FIR/IIR filter design frameworks | downstream repos |
| Large DSP pipelines | downstream repos |
| UI dashboards, deployment code, website content | `website` or deployment repos |

`qsp-filter` is a **building-block filtering library**, not a complete signal-processing system.
It must not absorb FFT, modulation, orientation, or application-level DSP logic.

## Filtering conventions

Agents must preserve these conventions when modifying the package:

| Convention | Behavior |
|---|---|
| Smoothing length | `moving_average` and `weighted_moving_average` shorten the output (`len - window + 1`); `exponential_moving_average` preserves length |
| Edge handling | No padding; callers must account for reduced length |
| Normalization output range | `min_max_normalize` → `[0, 1]`; `z_score_normalize` → zero mean / unit variance; `l2_normalize` → unit L2 norm |
| Constant-input normalization | All three normalizers return **all zeros** for constant or zero inputs |
| Hard clip | Clamps each sample to `[minimum, maximum]`; delegates to `qsp.filters.clip` |
| Soft clip | `limit * tanh(x / limit)`; output in `(-limit, +limit)` |
| Input types | Any `Iterable[float]`; output is always `list[float]` |

Do not change these conventions without a deliberate, versioned API decision.

## Rules for agents

When making changes to this repository:

1. Do not reimplement Quaternion or SU(2) primitives — import from `qsp-core`.
2. Do not add FFT, modulation, orientation, or adaptive-filter logic — those belong in sibling repos.
3. Do not add UI code, deployment code, or website content.
4. Keep functions small, explicit, and testable.
5. Add tests for all new behavior.
6. Update README.md and docs/ when the public API changes.
7. Prefer pure Python with no new runtime dependencies beyond `qsp-core`.
8. Do not change established filtering conventions without a versioned decision.
9. Preserve repository boundaries — do not let this repo grow into a general DSP framework.
10. When in doubt about scope, consult `docs/architecture.md` and `docs/downstream-usage.md`.

## Repository structure

```
qsp_filter/     ← main package
tests/          ← pytest test suite
examples/       ← small runnable demos
docs/           ← architecture and API documentation
```
