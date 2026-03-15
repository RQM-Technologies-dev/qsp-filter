# Repository Roadmap

This document describes appropriate future growth for `qsp-filter`, what must not
be added, versioning guidance, and a contribution checklist.

---

## Current Scope

`qsp-filter` provides:

- Smoothing helpers: `moving_average`, `weighted_moving_average`, `exponential_moving_average`
- Normalization helpers: `min_max_normalize`, `z_score_normalize`, `l2_normalize`
- Clipping helpers: `clip_signal`, `soft_clip_signal`
- Internal validation utilities: `qsp.filter.utils`

All additions to this repository must remain within the filtering and signal-conditioning
primitives category. See [`architecture.md`](architecture.md) for the full boundary definition.

---

## Appropriate Future Additions

The following capabilities are **in scope** for future contributions to `qsp-filter`:

| Capability | Notes |
|---|---|
| Additional smoothing kernels | Gaussian-window smoothing, median filter, Savitzky-Golay-style smoothing |
| Rolling statistics helpers | Rolling variance, rolling RMS, rolling min/max |
| Robust normalization helpers | Percentile-based (IQR) scaling, robust z-score |
| Outlier-resistant clipping | Percentile-based soft threshold, Winsorizing |
| Simple denoising helpers | Threshold-based denoising, simple signal cleaning |
| Reusable signal-scaling utilities | Per-channel scaling, range mapping |
| Additional length-preserving smoothers | Causal and non-causal variants |

All additions must:

- Accept `Iterable[float]` inputs and return `list[float]`
- Be pure Python with no runtime dependencies beyond `qsp-core`
- Include full test coverage in `tests/`
- Be documented in `docs/api-overview.md`
- Preserve the existing filtering conventions unless explicitly changing them with a version bump

---

## What Must NOT Be Added Here

The following capabilities belong in sibling repositories or downstream systems and
must **not** be added to `qsp-filter`:

| Capability | Correct destination |
|---|---|
| Adaptive equalizers, LMS/RLS filters | `quaternionic-modem` or downstream |
| Communications-specific channel conditioning | `quaternionic-modem` |
| Spectral estimators, power spectral density | `qsp-fft` |
| Full FIR/IIR filter design framework | downstream repos |
| FFT-based filtering (bandpass, notch) | `qsp-fft` |
| Modulation-specific normalization | `qsp-modulation` |
| IMU-specific preprocessing | `qsp-orientation` |
| Application-level robotics or navigation logic | `quaternionic-navigation` |
| Hardware-specific sensor pipelines | downstream or deployment repos |
| Full end-to-end DSP workflow engines | downstream repos |
| UI dashboards, visualization code | `website` or downstream apps |

If a proposed addition would substantially change the repository's role from a
filtering-primitives library to a general DSP framework, it does not belong here.

---

## Versioning Guidance

- **Patch releases** (`0.x.y`): bug fixes, documentation updates, non-breaking internal
  refactors.
- **Minor releases** (`0.x.0`): new helpers, new convenience exports, backward-compatible
  additions.
- **Major releases** (`x.0.0`): intentional breaking changes to filtering conventions,
  function signatures, or output semantics. Breaking changes must be documented explicitly
  in a changelog entry with migration guidance.

The filtering conventions documented in [`architecture.md`](architecture.md) are considered
**stable API surface**. Changing them (e.g., changing output length behavior, changing
normalization fallback values) requires a major version bump.

---

## Contribution Checklist

Before submitting a contribution to `qsp-filter`:

- [ ] The change is within the filtering / signal-conditioning primitives scope
- [ ] No new runtime dependencies are introduced beyond `qsp-core`
- [ ] New functions accept `Iterable[float]` and return `list[float]`
- [ ] New functions include input validation with clear error messages
- [ ] Tests are added for all new behavior (including edge cases)
- [ ] `docs/api-overview.md` is updated for any new public functions
- [ ] `README.md` is updated if the public API surface or conventions change
- [ ] Filtering conventions in `docs/architecture.md` are updated if behavior changes
- [ ] AGENTS.md boundary rules are not violated
- [ ] No quaternion, FFT, modulation, or orientation logic is introduced
