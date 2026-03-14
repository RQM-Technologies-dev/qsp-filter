# qsp-filter

`qsp-filter` is the filtering library of the RQM Technologies Quaternionic Signal Processing (QSP)
ecosystem. It is built on [`qsp-core`](https://github.com/RQM-Technologies-dev/qsp-core) and
provides smoothing, normalization, and clipping utilities for real-valued signals.

## Ecosystem context

```
RQM-Technologies
├── qsp-core       ← shared quaternion math and basic utilities  (dependency)
├── qsp-fft        ← spectral transforms built on qsp-core
├── qsp-filter     ← THIS REPO: filtering layer built on qsp-core
└── qsp-modulation ← modulation library built on qsp-core
```

Quaternion primitives and SU(2) helpers belong in `qsp-core`, not here.
`qsp-filter` imports those primitives and focuses exclusively on filtering logic.

## What belongs here vs. in qsp-core

| Concern | Where it lives |
|---|---|
| `Quaternion` type, SU(2) helpers | `qsp-core` |
| Basic `moving_average`, `clip`, `normalize_signal` | `qsp-core` |
| Spectral transforms (DFT/IDFT) | `qsp-fft` |
| Weighted & exponential moving averages | **qsp-filter** |
| Min-max, z-score, L2 normalization | **qsp-filter** |
| Hard clip, soft clip | **qsp-filter** |

## Installation

```bash
pip install qsp-core   # install the dependency first
pip install -e .       # install qsp-filter in editable mode
```

## Package structure

```
qsp_filter/
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

- [`docs/architecture.md`](docs/architecture.md) – ecosystem placement and module layout
- [`docs/api-overview.md`](docs/api-overview.md) – public function signatures
- [`docs/dependency-on-qsp-core.md`](docs/dependency-on-qsp-core.md) – what is imported from qsp-core and why
