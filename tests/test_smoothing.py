"""Tests for qsp.filter.smoothing."""

import math
import pytest

from qsp.filter.smoothing import (
    exponential_moving_average,
    moving_average,
    weighted_moving_average,
)


class TestMovingAverage:
    def test_basic_average(self):
        result = moving_average([1.0, 2.0, 3.0, 4.0, 5.0], window_size=3)
        assert result == [2.0, 3.0, 4.0]

    def test_window_equals_signal_length(self):
        result = moving_average([1.0, 2.0, 3.0], window_size=3)
        assert result == [2.0]

    def test_window_size_one_is_identity(self):
        signal = [1.0, 2.0, 3.0]
        assert moving_average(signal, window_size=1) == signal

    def test_single_element_signal(self):
        assert moving_average([7.0], window_size=1) == [7.0]

    def test_window_exceeds_signal_raises(self):
        with pytest.raises(ValueError):
            moving_average([1.0, 2.0], window_size=5)

    def test_zero_window_raises(self):
        with pytest.raises(ValueError):
            moving_average([1.0, 2.0], window_size=0)

    def test_negative_window_raises(self):
        with pytest.raises(ValueError):
            moving_average([1.0, 2.0], window_size=-1)

    def test_non_integer_window_raises(self):
        with pytest.raises((TypeError, ValueError)):
            moving_average([1.0, 2.0], window_size=1.5)  # type: ignore[arg-type]


class TestWeightedMovingAverage:
    def test_uniform_weights_match_moving_average(self):
        signal = [1.0, 2.0, 3.0, 4.0]
        result = weighted_moving_average(signal, weights=[1.0, 1.0, 1.0])
        expected = moving_average(signal, window_size=3)
        for r, e in zip(result, expected):
            assert math.isclose(r, e, rel_tol=1e-9)

    def test_linearly_increasing_weights(self):
        result = weighted_moving_average([1.0, 2.0, 3.0], weights=[1.0, 2.0])
        # window [1,2]: (1*1 + 2*2) / 3 = 5/3
        # window [2,3]: (1*2 + 2*3) / 3 = 8/3
        assert math.isclose(result[0], 5 / 3, rel_tol=1e-9)
        assert math.isclose(result[1], 8 / 3, rel_tol=1e-9)

    def test_single_weight(self):
        assert weighted_moving_average([3.0, 5.0, 7.0], weights=[2.0]) == [3.0, 5.0, 7.0]

    def test_weights_exceed_signal_raises(self):
        with pytest.raises(ValueError):
            weighted_moving_average([1.0], weights=[1.0, 1.0])

    def test_negative_weight_raises(self):
        with pytest.raises(ValueError):
            weighted_moving_average([1.0, 2.0, 3.0], weights=[-1.0, 1.0])

    def test_all_zero_weights_raises(self):
        with pytest.raises(ValueError):
            weighted_moving_average([1.0, 2.0, 3.0], weights=[0.0, 0.0])


class TestExponentialMovingAverage:
    def test_alpha_one_is_identity(self):
        signal = [1.0, 2.0, 3.0, 4.0]
        assert exponential_moving_average(signal, alpha=1.0) == signal

    def test_output_length_matches_input(self):
        signal = [1.0, 2.0, 3.0, 4.0, 5.0]
        result = exponential_moving_average(signal, alpha=0.5)
        assert len(result) == len(signal)

    def test_first_element_unchanged(self):
        signal = [10.0, 1.0, 1.0, 1.0]
        result = exponential_moving_average(signal, alpha=0.3)
        assert result[0] == 10.0

    def test_smoothing_reduces_variation(self):
        signal = [0.0, 10.0, 0.0, 10.0]
        smoothed = exponential_moving_average(signal, alpha=0.2)
        # variation in smoothed signal should be lower
        raw_var = max(signal) - min(signal)
        smooth_var = max(smoothed) - min(smoothed)
        assert smooth_var < raw_var

    def test_alpha_zero_raises(self):
        with pytest.raises(ValueError):
            exponential_moving_average([1.0, 2.0], alpha=0.0)

    def test_alpha_above_one_raises(self):
        with pytest.raises(ValueError):
            exponential_moving_average([1.0, 2.0], alpha=1.5)

    def test_single_element_signal(self):
        assert exponential_moving_average([5.0], alpha=0.5) == [5.0]
