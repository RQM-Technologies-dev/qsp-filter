"""Tests for qsp_filter.normalization."""

import math
import pytest

from qsp_filter.normalization import l2_normalize, min_max_normalize, z_score_normalize


class TestMinMaxNormalize:
    def test_basic_range(self):
        result = min_max_normalize([0.0, 5.0, 10.0])
        assert result == [0.0, 0.5, 1.0]

    def test_single_element(self):
        assert min_max_normalize([3.0]) == [0.0]

    def test_constant_signal_returns_zeros(self):
        assert min_max_normalize([7.0, 7.0, 7.0]) == [0.0, 0.0, 0.0]

    def test_negative_values(self):
        result = min_max_normalize([-2.0, 0.0, 2.0])
        assert math.isclose(result[0], 0.0)
        assert math.isclose(result[1], 0.5)
        assert math.isclose(result[2], 1.0)

    def test_output_bounds(self):
        signal = [-100.0, 0.0, 42.0, 100.0]
        result = min_max_normalize(signal)
        assert min(result) == 0.0
        assert max(result) == 1.0

    def test_empty_signal_raises(self):
        with pytest.raises(ValueError):
            min_max_normalize([])


class TestZScoreNormalize:
    def test_zero_mean(self):
        result = z_score_normalize([1.0, 2.0, 3.0, 4.0, 5.0])
        mean = sum(result) / len(result)
        assert math.isclose(mean, 0.0, abs_tol=1e-9)

    def test_unit_std(self):
        result = z_score_normalize([1.0, 2.0, 3.0, 4.0, 5.0])
        mean = sum(result) / len(result)
        variance = sum((x - mean) ** 2 for x in result) / len(result)
        assert math.isclose(variance, 1.0, rel_tol=1e-9)

    def test_constant_signal_returns_zeros(self):
        assert z_score_normalize([5.0, 5.0, 5.0]) == [0.0, 0.0, 0.0]

    def test_single_element_constant(self):
        assert z_score_normalize([42.0]) == [0.0]

    def test_empty_signal_raises(self):
        with pytest.raises(ValueError):
            z_score_normalize([])


class TestL2Normalize:
    def test_unit_norm(self):
        result = l2_normalize([3.0, 4.0])
        norm = math.sqrt(sum(x ** 2 for x in result))
        assert math.isclose(norm, 1.0, rel_tol=1e-9)

    def test_zero_signal_returns_zeros(self):
        assert l2_normalize([0.0, 0.0, 0.0]) == [0.0, 0.0, 0.0]

    def test_already_unit_vector(self):
        result = l2_normalize([1.0, 0.0, 0.0])
        assert result == [1.0, 0.0, 0.0]

    def test_single_positive_element(self):
        result = l2_normalize([5.0])
        assert math.isclose(result[0], 1.0)

    def test_negative_values(self):
        result = l2_normalize([-3.0, 4.0])
        norm = math.sqrt(sum(x ** 2 for x in result))
        assert math.isclose(norm, 1.0, rel_tol=1e-9)

    def test_empty_signal_raises(self):
        with pytest.raises(ValueError):
            l2_normalize([])
