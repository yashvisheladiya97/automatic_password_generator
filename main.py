"""Entry point for the local password toolkit."""
from __future__ import annotations

import getpass
import sys

from checker import check_password
from generator import generate_password
from utils import copy_to_clipboard, validate_length


def prompt_yes_no(label: str, default: bool = True) -> bool:
    """Read a yes/no response, returning default on empty input."""
    suffix = "Y/n" if default else "y/N"
    while True:
        answer = input(f"{label} [{suffix}]: ").strip().lower()
        if not answer:
            return default
        if answer in {"y", "yes"}:
            return True
        if answer in {"n", "no"}:
            return False
        print("Please enter y or n.")


def generate_flow() -> None:
    """Interactively generate a password and optionally copy it."""
    while True:
        raw_length = input("Password length (minimum 8, recommended 16+): ").strip()
        try:
            length = validate_length(raw_length)
            break
        except ValueError as exc:
            print(f"Error: {exc}")

    options = {
        "uppercase": prompt_yes_no("Include uppercase letters (A-Z)?"),
        "lowercase": prompt_yes_no("Include lowercase letters (a-z)?"),
        "digits": prompt_yes_no("Include digits (0-9)?"),
        "symbols": prompt_yes_no("Include symbols (!@#...)?"),
    }
    try:
        password = generate_password(length=length, **options)
    except ValueError as exc:
        print(f"Error: {exc}")
        return

    print("\nGenerated password (shown only in this terminal):")
    print(password)
    if prompt_yes_no("Copy password to clipboard?", default=False):
        if copy_to_clipboard(password):
            print("Copied. Be aware that clipboard managers may retain clipboard history.")
        else:
            print("Clipboard copy was unavailable. Select and copy the password manually.")
    # Python strings cannot be reliably zeroized; drop our reference as soon as practical.
    del password


def check_flow() -> None:
    """Check a password without echoing it to the terminal."""
    password = getpass.getpass("Enter password to check (input hidden): ")
    result = check_password(password)
    print(f"\nAssessment: {result.label} ({result.score}/100)")
    for item in result.feedback:
        print(f"- {item}")
    del password


def main() -> int:
    """Run the command-line menu."""
    print("Secure Password Toolkit")
    print("Passwords are processed locally; this program does not save or transmit them.")
    while True:
        print("\n1. Generate password\n2. Check password strength\n3. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            generate_flow()
        elif choice == "2":
            check_flow()
        elif choice == "3":
            print("Goodbye.")
            return 0
        else:
            print("Choose 1, 2, or 3.")


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (KeyboardInterrupt, EOFError):
        print("\nCancelled.", file=sys.stderr)
        raise SystemExit(130)
