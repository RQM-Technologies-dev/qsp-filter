# RQM Technologies – Agent Instructions

This repository is the **filtering layer** of the RQM Technologies ecosystem, built on `qsp-core`.

## Role of this repository

`qsp-filter` provides signal filtering utilities for the RQM Technologies QSP ecosystem.
It depends on `qsp-core` for quaternion math, SU(2) helpers, and basic validation utilities.

This repository must remain:

- small and focused on filtering logic
- modular and pure Python
- dependency-light (only `qsp-core` as a runtime dependency)
- mathematically clear and well-tested

## Boundary discipline

**What belongs here:**

- Smoothing filters (moving average, weighted moving average, exponential moving average)
- Normalization utilities (min-max, z-score, L2)
- Clipping utilities (hard clip, soft clip)
- Shared validation helpers specific to the filtering layer

**What does NOT belong here:**

- Quaternion or SU(2) primitives — import from `qsp-core` (`qsp.quaternion`, `qsp.su2`)
- Basic `moving_average`, `clip`, and `normalize_signal` reimplementations — import from `qsp-core` (`qsp.filters`)
- Spectral transforms (DFT/IDFT) — those belong in `qsp-fft`
- Modulation utilities — those belong in `qsp-modulation`
- UI code, deployment code, or website content

## Ecosystem architecture

```
RQM-Technologies
├── qsp-core          ← shared math primitives (Quaternion, SU(2), basic filters)
├── qsp-fft           ← spectral transforms built on qsp-core
├── qsp-filter        ← filtering library built on qsp-core  (THIS REPO)
├── qsp-modulation    ← modulation library built on qsp-core
├── eigenclock
├── quaternionic-modem
├── quaternionic-navigation
├── website
├── documentation
└── research-notebooks
```

## Rules for agents

When making changes to this repository:

1. Do not reimplement Quaternion or SU(2) primitives — import from `qsp-core`.
2. Do not add UI code.
3. Do not add deployment code.
4. Keep functions small, explicit, and testable.
5. Add tests for all new behavior.
6. Update README and docs when the public API changes.
7. Prefer pure Python with no new runtime dependencies beyond `qsp-core`.

## Repository structure

```
qsp_filter/     ← main package
tests/          ← pytest test suite
examples/       ← small runnable demos
docs/           ← architecture and API documentation
```
