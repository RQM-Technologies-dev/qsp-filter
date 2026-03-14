"""Tests for qsp.filter.clipping."""

import math
import pytest

from qsp.filter.clipping import clip_signal, soft_clip_signal


class TestClipSignal:
    def test_values_within_range_unchanged(self):
        assert clip_signal([1.0, 2.0, 3.0], minimum=0.0, maximum=5.0) == [1.0, 2.0, 3.0]

    def test_values_below_minimum_clipped(self):
        assert clip_signal([-5.0, 0.0, 5.0], minimum=0.0, maximum=10.0) == [0.0, 0.0, 5.0]

    def test_values_above_maximum_clipped(self):
        assert clip_signal([0.0, 5.0, 15.0], minimum=0.0, maximum=10.0) == [0.0, 5.0, 10.0]

    def test_all_samples_clamped(self):
        result = clip_signal([-10.0, 0.0, 10.0], minimum=-1.0, maximum=1.0)
        assert result == [-1.0, 0.0, 1.0]

    def test_minimum_equals_maximum(self):
        result = clip_signal([0.0, 5.0, 10.0], minimum=3.0, maximum=3.0)
        assert result == [3.0, 3.0, 3.0]

    def test_minimum_greater_than_maximum_raises(self):
        with pytest.raises(ValueError):
            clip_signal([1.0, 2.0], minimum=5.0, maximum=1.0)

    def test_empty_signal(self):
        assert clip_signal([], minimum=0.0, maximum=1.0) == []

    def test_non_real_minimum_raises(self):
        with pytest.raises(TypeError):
            clip_signal([1.0], minimum="zero", maximum=1.0)  # type: ignore[arg-type]


class TestSoftClipSignal:
    def test_output_length_matches_input(self):
        result = soft_clip_signal([1.0, 2.0, 3.0], limit=1.0)
        assert len(result) == 3

    def test_large_positive_saturates_below_limit(self):
        result = soft_clip_signal([10.0], limit=1.0)
        assert result[0] < 1.0
        assert result[0] > 0.99

    def test_large_negative_saturates_above_negative_limit(self):
        result = soft_clip_signal([-10.0], limit=1.0)
        assert result[0] > -1.0
        assert result[0] < -0.99

    def test_zero_input_gives_zero_output(self):
        result = soft_clip_signal([0.0], limit=1.0)
        assert math.isclose(result[0], 0.0, abs_tol=1e-12)

    def test_custom_limit(self):
        result = soft_clip_signal([50.0], limit=5.0)
        assert result[0] < 5.0
        assert result[0] > 4.9

    def test_zero_limit_raises(self):
        with pytest.raises(ValueError):
            soft_clip_signal([1.0], limit=0.0)

    def test_negative_limit_raises(self):
        with pytest.raises(ValueError):
            soft_clip_signal([1.0], limit=-1.0)

    def test_odd_symmetry(self):
        signal = [1.0, 2.0, 3.0]
        pos = soft_clip_signal(signal, limit=1.0)
        neg = soft_clip_signal([-s for s in signal], limit=1.0)
        for p, n in zip(pos, neg):
            assert math.isclose(p, -n, rel_tol=1e-9)
