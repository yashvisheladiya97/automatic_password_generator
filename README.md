# Secure Password Toolkit

A local-only Python command-line application for generating cryptographically secure passwords and assessing password strength. It uses Python's standard library and makes no network requests.

> **Privacy note:** The application does not intentionally save, log, or transmit passwords. Passwords exist in process memory while being handled. Python cannot reliably zeroize immutable strings from memory, and your terminal, operating system, clipboard, clipboard history, or screen-recording tools may retain displayed/copied content.

## Features

- Secure generation using `secrets.choice()` and `secrets.randbelow()` (never `random`).
- Custom length from 8 to 256 characters; 16+ characters recommended.
- Choose uppercase, lowercase, digits, and symbols.
- Ensures at least one character from each enabled character set.
- Local strength estimate with actionable guidance for length, diversity, repetition, common passwords, and simple sequences.
- Hidden terminal input when checking a password.
- Optional OS clipboard copy, with no third-party Python dependencies.
- Unit tests and a GitHub-ready structure.

## Project structure

```text
secure-password-toolkit/
├── main.py
├── generator.py
├── checker.py
├── utils.py
├── tests/
│   ├── test_generator.py
│   └── test_checker.py
├── .gitignore
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.10 or newer
- No external packages required

## Installation

```bash
git clone https://github.com/YOUR-USERNAME/secure-password-toolkit.git
cd secure-password-toolkit
python main.py
```

On Windows, use `py main.py` if `python` is not recognized. On macOS/Linux, use `python3 main.py` if needed.

## Usage

Start the menu:

```bash
python main.py
```

Choose **1** to generate a password, enter a length (16 or more is recommended), then choose the character types. You can optionally copy it to the local clipboard.

Choose **2** to check a password. The terminal input is hidden using `getpass`; the checker reports a score, label, and improvement suggestions. The actual password is never included in the result.

### Use as a Python module

```python
from generator import generate_password
from checker import check_password

password = generate_password(
    length=20,
    uppercase=True,
    lowercase=True,
    digits=True,
    symbols=True,
)
print(password)

assessment = check_password("Example-phrase-93!Long")
print(assessment.label, assessment.score)
for suggestion in assessment.feedback:
    print("-", suggestion)
```

Do not hard-code real passwords into source files, tests, screenshots, issue reports, or commits. The example above is illustrative only.

### Screenshots

Add screenshots to a `screenshots/` directory and embed them here, for example:

```markdown
![Application menu](screenshots/menu.png)
![Strength assessment](screenshots/strength-check.png)
```

Before sharing screenshots, ensure no real passwords or sensitive information are visible.

## Security practices

- **Cryptographic randomness:** generation uses `secrets`, intended for security-sensitive randomness.
- **Local-only operation:** no HTTP clients, external APIs, analytics, or telemetry.
- **No password persistence:** the app does not write password values to files or databases.
- **No password logging:** the code does not log password values.
- **Hidden checker input:** `getpass` suppresses terminal echo during strength checks.
- **No third-party runtime dependencies:** reduces supply-chain exposure.
- **Input validation:** length is constrained to 8–256 characters.
- **Safe clipboard invocation:** OS clipboard tools are called with argument lists and timeouts, not shell command interpolation.

### Important limitations

- Strength checking is a heuristic, not a guarantee of how quickly an attacker could guess a password. It does not query breached-password databases, because doing so would transmit information and violate the local-only requirement.
- A strong password should be unique for every account. A reputable password manager is usually safer than memorizing or reusing passwords.
- Python strings are immutable and may be copied internally; deleting a variable does **not** guarantee that the underlying memory is overwritten.
- Clipboard managers and operating systems may retain clipboard contents. Avoid copying passwords on shared devices and clear clipboard history when appropriate.
- The generated password is displayed in the terminal, which may be captured by terminal history, screenshots, or screen recording. The application itself does not save it.

## Tests

Run all unit tests from the project root:

```bash
python -m unittest discover -s tests -v
```

## GitHub setup

```bash
git init
git add .
git commit -m "Build secure password toolkit"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/secure-password-toolkit.git
git push -u origin main
```

Never commit `.env` files, credentials, real passwords, or screenshots containing sensitive data.

## Future enhancements

- Tkinter desktop GUI with masked input and a strength meter.
- Accessibility improvements and localization.
- Optional passphrase generation using a carefully curated local word list.
- Packaging as a standalone executable.
- Additional tests and static analysis in GitHub Actions.

## License

Choose a license before publishing (for example, MIT) and add the corresponding `LICENSE` file.
