import subprocess
import sys


def test_ruff_check():
    """Run ruff check to ensure code quality."""
    # Run ruff check on the current directory
    result = subprocess.run(
        [sys.executable, "-m", "ruff", "check", "."], capture_output=True, text=True
    )

    # If there are errors, print them for better debugging in pytest output
    if result.returncode != 0:
        print("\n--- Ruff Check Errors ---")
        print(result.stdout)
        print(result.stderr)

    assert result.returncode == 0, (
        "Ruff found linting issues. Run 'ruff check . --fix' to fix them."
    )


def test_ruff_format():
    """Run ruff format --check to ensure code formatting matches standards."""
    result = subprocess.run(
        [sys.executable, "-m", "ruff", "format", "--check", "."],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print("\n--- Ruff Format Errors ---")
        print(result.stdout)
        print(result.stderr)

    assert result.returncode == 0, (
        "Code is not formatted correctly. Run 'ruff format .' to fix."
    )
