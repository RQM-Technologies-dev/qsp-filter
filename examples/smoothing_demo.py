"""Smoothing demo – runnable example for qsp.filter.smoothing.

Run with:
    python examples/smoothing_demo.py
"""

from qsp.filter.smoothing import (
    exponential_moving_average,
    moving_average,
    weighted_moving_average,
)

signal = [1.0, 3.0, 5.0, 7.0, 5.0, 3.0, 1.0, 3.0, 5.0, 7.0]

print("Input signal:")
print(" ", signal)

ma = moving_average(signal, window_size=3)
print("\nMoving average (window=3):")
print(" ", [round(x, 3) for x in ma])

wma = weighted_moving_average(signal, weights=[1.0, 2.0, 3.0])
print("\nWeighted moving average (weights=[1,2,3]):")
print(" ", [round(x, 3) for x in wma])

ema = exponential_moving_average(signal, alpha=0.3)
print("\nExponential moving average (alpha=0.3):")
print(" ", [round(x, 3) for x in ema])
