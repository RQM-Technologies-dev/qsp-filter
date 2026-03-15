# Dependency on qsp-core

## Why qsp-core?

`qsp-filter` is part of the RQM Technologies QSP ecosystem.
`qsp-core` is the shared foundation that all Layer 1 libraries build on.
By importing from `qsp-core` instead of reimplementing shared logic,
`qsp-filter` stays small, consistent, and easy to maintain.

## What is imported from qsp-core

### `qsp.filters.moving_average`

`qsp.filter.smoothing.moving_average` is a thin wrapper around
`qsp.filters.moving_average`. The wrapper adds local input validation
(`ensure_positive_int`) before delegating, so callers get clear error
messages regardless of which package they call.

```python
# qsp/filter/smoothing.py
from qsp.filters import moving_average as _core_moving_average
```

### `qsp.filters.clip`

`qsp.filter.clipping.clip_signal` delegates to `qsp.filters.clip`
after validating the `minimum` and `maximum` arguments locally.

```python
# qsp/filter/clipping.py
from qsp.filters import clip as _core_clip
```

## What is NOT reimplemented

The following primitives live exclusively in `qsp-core` and must never
be copied or re-implemented in `qsp-filter`:

| Primitive | qsp-core location |
|---|---|
| `Quaternion` | `qsp.quaternion` |
| `is_unit_quaternion`, `normalize_quaternion` | `qsp.su2` |
| `quaternion_to_su2`, `su2_to_quaternion` | `qsp.su2` |
| `matrix_trace` | `qsp.su2` |
| `dft`, `idft` | `qsp.transforms` |

## Installing qsp-core

`qsp-core` is listed as a required dependency in `pyproject.toml`.
It is installed automatically when you install `qsp-filter`:

```bash
pip install -e .
```

If you want to install `qsp-core` separately first:

```bash
# from source
pip install git+https://github.com/RQM-Technologies-dev/qsp-core.git

# then install qsp-filter
pip install -e .
```

## Version constraint

`pyproject.toml` requires `qsp-core>=0.1.0`.
Keep this constraint loose to avoid unnecessary breakage as both
packages evolve in tandem.
