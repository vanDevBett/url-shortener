"""Base62 encoding utilities for generating short codes."""

ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
BASE = len(ALPHABET)


def encode_base62(number: int) -> str:
    """Encode a non-negative integer into its Base62 representation.

    Args:
        number: The integer to encode. Must be non-negative.

    Returns:
        The Base62 string. ``encode_base62(0)`` returns ``"0"``.

    Raises:
        ValueError: If ``number`` is negative.
    """
    if number < 0:
        raise ValueError("number must be non-negative")
    if number == 0:
        return ALPHABET[0]

    digits: list[str] = []
    while number > 0:
        number, remainder = divmod(number, BASE)
        digits.append(ALPHABET[remainder])

    return "".join(reversed(digits))
