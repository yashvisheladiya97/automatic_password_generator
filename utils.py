"""Small utility functions. No password persistence or logging is performed."""
from __future__ import annotations

import shutil
import subprocess
import sys


def validate_length(value: str) -> int:
    """Parse and validate a password length from CLI input."""
    try:
        length = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError("Enter a whole number for the password length.") from exc
    if not 8 <= length <= 256:
        raise ValueError("Choose a length between 8 and 256 characters.")
    return length


def copy_to_clipboard(text: str) -> bool:
    """Copy text using a local OS clipboard utility when available.

    Clipboard history software may retain copied content. No network is used.
    """
    try:
        if sys.platform == "darwin" and shutil.which("pbcopy"):
            subprocess.run(["pbcopy"], input=text, text=True, check=True, timeout=3)
            return True
        if sys.platform.startswith("linux") and shutil.which("wl-copy"):
            subprocess.run(["wl-copy"], input=text, text=True, check=True, timeout=3)
            return True
        if sys.platform.startswith("linux") and shutil.which("xclip"):
            subprocess.run(
                ["xclip", "-selection", "clipboard"],
                input=text, text=True, check=True, timeout=3,
            )
            return True
        if sys.platform == "win32":
            subprocess.run(
                ["clip"], input=text, text=True, check=True, timeout=3,
                shell=False,
            )
            return True
    except (OSError, subprocess.SubprocessError):
        return False
    return False
