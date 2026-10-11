"""Cryptographically secure password generation."""
from __future__ import annotations

import secrets
import string
from collections.abc import Sequence

CHARACTER_SETS = {
    "uppercase": string.ascii_uppercase,
    "lowercase": string.ascii_lowercase,
    "digits": string.digits,
    "symbols": "!@#$%^&*()-_=+[]{};:,.?/\\~",
}


def generate_password(
    length: int = 16,
    *,
    uppercase: bool = True,
    lowercase: bool = True,
    digits: bool = True,
    symbols: bool = True,
) -> str:
    """Generate a password using secrets and ensure every selected class appears.

    Raises:
        ValueError: if the length is invalid or no character classes are selected.
    """
    if not isinstance(length, int) or isinstance(length, bool) or length < 8:
        raise ValueError("Password length must be an integer of at least 8.")

    selected: list[str] = [
        CHARACTER_SETS[name]
        for name, enabled in (
            ("uppercase", uppercase),
            ("lowercase", lowercase),
            ("digits", digits),
            ("symbols", symbols),
        )
        if enabled
    ]
    if not selected:
        raise ValueError("Select at least one character type.")
    if length < len(selected):
        raise ValueError("Length is too short for the selected character types.")

    # Guarantee at least one character from every enabled class.
    chars = [secrets.choice(charset) for charset in selected]
    all_chars = "".join(selected)
    chars.extend(secrets.choice(all_chars) for _ in range(length - len(chars)))

    # Fisher-Yates shuffle driven by cryptographically secure randomness.
    for index in range(len(chars) - 1, 0, -1):
        swap_index = secrets.randbelow(index + 1)
        chars[index], chars[swap_index] = chars[swap_index], chars[index]
    return "".join(chars)
