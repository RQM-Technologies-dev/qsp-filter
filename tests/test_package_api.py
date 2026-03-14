"""Tests for the qsp.filter package API surface."""

import pytest


class TestPublicAPIExists:
    """Verify that all documented public names are importable."""

    def test_import_package(self):
        import qsp.filter  # noqa: F401

    def test_moving_average_importable(self):
        from qsp.filter import moving_average
        assert callable(moving_average)

    def test_weighted_moving_average_importable(self):
        from qsp.filter import weighted_moving_average
        assert callable(weighted_moving_average)

    def test_exponential_moving_average_importable(self):
        from qsp.filter import exponential_moving_average
        assert callable(exponential_moving_average)

    def test_min_max_normalize_importable(self):
        from qsp.filter import min_max_normalize
        assert callable(min_max_normalize)

    def test_z_score_normalize_importable(self):
        from qsp.filter import z_score_normalize
        assert callable(z_score_normalize)

    def test_l2_normalize_importable(self):
        from qsp.filter import l2_normalize
        assert callable(l2_normalize)

    def test_clip_signal_importable(self):
        from qsp.filter import clip_signal
        assert callable(clip_signal)

    def test_soft_clip_signal_importable(self):
        from qsp.filter import soft_clip_signal
        assert callable(soft_clip_signal)


class TestAllDunderList:
    def test_all_names_are_callable(self):
        import qsp.filter
        for name in qsp.filter.__all__:
            assert callable(getattr(qsp.filter, name)), f"{name} should be callable"

    def test_all_contains_expected_names(self):
        import qsp.filter
        expected = {
            "clip_signal",
            "exponential_moving_average",
            "l2_normalize",
            "min_max_normalize",
            "moving_average",
            "soft_clip_signal",
            "weighted_moving_average",
            "z_score_normalize",
        }
        assert expected == set(qsp.filter.__all__)


class TestQspCoreIntegration:
    """Verify that qsp-core primitives are accessible and qsp.filter delegates to them."""

    def test_qsp_core_moving_average_importable(self):
        from qsp.filters import moving_average
        assert callable(moving_average)

    def test_qsp_core_clip_importable(self):
        from qsp.filters import clip
        assert callable(clip)

    def test_moving_average_consistent_with_qsp_core(self):
        """qsp.filter.moving_average must produce the same result as qsp.filters.moving_average."""
        from qsp.filters import moving_average as core_ma
        from qsp.filter import moving_average as filter_ma

        signal = [1.0, 2.0, 3.0, 4.0, 5.0]
        assert filter_ma(signal, 3) == core_ma(signal, 3)

    def test_clip_signal_consistent_with_qsp_core(self):
        """qsp.filter.clip_signal must produce the same result as qsp.filters.clip."""
        from qsp.filters import clip as core_clip
        from qsp.filter import clip_signal

        signal = [-2.0, 0.0, 5.0, 10.0]
        assert clip_signal(signal, -1.0, 8.0) == core_clip(signal, -1.0, 8.0)
