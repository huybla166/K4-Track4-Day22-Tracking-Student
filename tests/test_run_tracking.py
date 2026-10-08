"""Unit tests for run_tracking pure functions."""

from run_tracking import color_for_id


def test_color_for_id_deterministic() -> None:
    """Cùng track_id phải luôn trả về cùng một màu BGR."""
    c1 = color_for_id(42)
    c2 = color_for_id(42)
    assert c1 == c2


def test_color_for_id_range_and_types() -> None:
    """Mỗi kênh màu phải là số nguyên trong khoảng [64, 254]."""
    for tid in (0, 1, 99, 1000):
        color = color_for_id(tid)
        assert len(color) == 3
        for ch in color:
            assert isinstance(ch, int)
            assert 64 <= ch < 255


def test_color_for_id_distinct() -> None:
    """Hai ID khác nhau phải sinh màu khác nhau trong hầu hết trường hợp."""
    assert color_for_id(1) != color_for_id(2)

