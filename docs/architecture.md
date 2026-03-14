# Architecture

## Ecosystem position

`qsp-filter` is a Layer 1 library in the RQM Technologies ecosystem.
It sits directly above `qsp-core` and provides a focused set of signal-filtering
utilities that downstream applications (Layer 2) can depend on.

```
┌─────────────────────────────────────────────────────────────────┐
│  Layer 2 – Applications                                         │
│  eigenclock · quaternionic-modem · quaternionic-navigation      │
└───────────────────────────────┬─────────────────────────────────┘
                                │ depends on
┌───────────────────────────────▼─────────────────────────────────┐
│  Layer 1 – QSP libraries                                        │
│  qsp-core  qsp-fft  qsp-filter  qsp-modulation                 │
└───────────────────────────────┬─────────────────────────────────┘
                                │ all Layer 1 libs depend on
┌───────────────────────────────▼─────────────────────────────────┐
│  qsp-core                                                        │
│  Quaternion · SU(2) · basic clip · basic moving_average         │
└─────────────────────────────────────────────────────────────────┘
```

## Module layout

```
qsp_filter/
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

Internal validation helpers shared across the `qsp_filter` modules.
These helpers are specific to the filtering layer; lower-level validation
utilities live in `qsp.utils` inside qsp-core.

## Dependency rules

- `qsp_filter` → `qsp-core` (required runtime dependency)
- `qsp_filter` → nothing else (no optional dependencies in core modules)
- Quaternion and SU(2) primitives must **not** be re-implemented here
- Tests use only the standard library and pytest
