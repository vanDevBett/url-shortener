"""Tests for the Base62 encoding utilities."""

import pytest

from app.core.base62 import ALPHABET, BASE, encode_base62


@pytest.mark.parametrize(
    "number, expected",
    [
        (0, "0"),
        (1, "1"),
        (9, "9"),
        (10, "a"),
        (35, "z"),
        (36, "A"),
        (61, "Z"),
        (62, "10"),
        (125, "21"),
        (3843, "ZZ"),
        (3844, "100"),
    ],
)
def test_encode_known_values(number: int, expected: str) -> None:
    assert encode_base62(number) == expected


def test_encode_uses_only_alphabet_chars() -> None:
    code = encode_base62(987_654_321)
    assert all(ch in ALPHABET for ch in code)


def test_encode_negative_raises() -> None:
    with pytest.raises(ValueError):
        encode_base62(-1)


def test_alphabet_is_well_formed() -> None:
    assert BASE == 62
    assert len(set(ALPHABET)) == 62