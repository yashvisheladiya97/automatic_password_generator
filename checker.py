"""Local password-strength heuristic (not a password-cracking oracle)."""
from __future__ import annotations

from dataclasses import dataclass
import math
import re


@dataclass(frozen=True)
class StrengthResult:
    """Structured result returned by check_password."""
    score: int
    label: str
    feedback: tuple[str, ...]


COMMON_PASSWORDS = {
    "password", "password1", "12345678", "123456789", "qwerty123",
    "admin123", "letmein", "welcome123", "iloveyou", "changeme",
}
SEQUENTIAL_PATTERNS = (
    "abcdefghijklmnopqrstuvwxyz",
    "0123456789",
    "qwertyuiop",
    "asdfghjkl",
    "zxcvbnm",
)


def _has_sequence(password: str) -> bool:
    """Detect simple ascending keyboard/alphanumeric sequences of length >= 4."""
    lowered = password.lower()
    for sequence in SEQUENTIAL_PATTERNS:
        for start in range(len(sequence) - 3):
            piece = sequence[start:start + 4]
            if piece in lowered or piece[::-1] in lowered:
                return True
    return False


def check_password(password: str) -> StrengthResult:
    """Estimate password strength without storing or transmitting the input.

    This is a local heuristic, not a guarantee. It intentionally avoids printing
    or returning the password itself.
    """
    if not isinstance(password, str):
        raise TypeError("Password must be a string.")

    if not password:
        return StrengthResult(0, "Very weak", ("Enter a password to assess it.",))

    feedback: list[str] = []
    score = 0
    length = len(password)

    # Length has the largest contribution. Longer unique passwords are preferred.
    if length >= 20:
        score += 45
    elif length >= 16:
        score += 38
    elif length >= 12:
        score += 30
    elif length >= 8:
        score += 18
    else:
        score += max(0, length * 2)
        feedback.append("Make it at least 12 characters long; 16+ is a good target.")

    classes = {
        "lowercase": any(c.islower() for c in password),
        "uppercase": any(c.isupper() for c in password),
        "digits": any(c.isdigit() for c in password),
        "symbols": any(not c.isalnum() and not c.isspace() for c in password),
    }
    class_count = sum(classes.values())
    score += {1: 0, 2: 10, 3: 20, 4: 28}.get(class_count, 0)

    # Rough entropy estimate, capped to avoid implying certainty.
    pool_size = 0
    if classes["lowercase"]:
        pool_size += 26
    if classes["uppercase"]:
        pool_size += 26
    if classes["digits"]:
        pool_size += 10
    if classes["symbols"]:
        pool_size += 32
    if pool_size:
        score += min(15, int(length * math.log2(pool_size) / 10))

    if length < 12:
        feedback.append("Use 12–16+ characters; length matters more than complexity alone.")
    if not classes["uppercase"]:
        feedback.append("Consider adding uppercase letters.")
    if not classes["lowercase"]:
        feedback.append("Consider adding lowercase letters.")
    if not classes["digits"]:
        feedback.append("Consider adding numbers.")
    if not classes["symbols"]:
        feedback.append("Consider adding symbols, or use a longer passphrase.")
    if len(set(password)) <= max(2, length // 4):
        score -= 15
        feedback.append("Avoid repeating the same few characters.")
    if re.search(r"(.)\1{2,}", password):
        score -= 10
        feedback.append("Avoid runs of the same character, such as 'aaa' or '111'.")
    if _has_sequence(password):
        score -= 15
        feedback.append("Avoid predictable sequences such as 'abcd', '1234', or keyboard runs.")
    if password.casefold() in COMMON_PASSWORDS:
        score = min(score, 10)
        feedback.append("This matches a commonly used password. Choose something unique.")
    if re.fullmatch(r"[A-Za-z]+|[0-9]+", password):
        score -= 10
        feedback.append("Avoid using only letters or only numbers.")

    score = max(0, min(100, score))
    if score < 25:
        label = "Very weak"
    elif score < 45:
        label = "Weak"
    elif score < 65:
        label = "Fair"
    elif score < 85:
        label = "Strong"
    else:
        label = "Very strong"

    if not feedback:
        feedback.append("Good structure. Make sure it is unique and not reused on another site.")
    return StrengthResult(score, label, tuple(dict.fromkeys(feedback)))
