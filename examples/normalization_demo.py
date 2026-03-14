"""Normalization demo – runnable example for qsp.filter.normalization.

Run with:
    python examples/normalization_demo.py
"""

from qsp.filter.normalization import l2_normalize, min_max_normalize, z_score_normalize

signal = [-4.0, -2.0, 0.0, 2.0, 4.0]

print("Input signal:")
print(" ", signal)

mm = min_max_normalize(signal)
print("\nMin-max normalized (range [0, 1]):")
print(" ", [round(x, 4) for x in mm])

zs = z_score_normalize(signal)
print("\nZ-score normalized (mean=0, std=1):")
print(" ", [round(x, 4) for x in zs])

l2 = l2_normalize(signal)
print("\nL2 normalized (unit Euclidean length):")
print(" ", [round(x, 4) for x in l2])
