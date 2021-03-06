import ast
import subprocess
from pathlib import Path

import pytest

from flake8_file_encoding import EncodingChecker, __version__


FEN001_MSG = "FEN001 open() call has no encoding argument"

current_dir = Path(__file__, "..").resolve()
data_dir = current_dir / "data"


def get_checker(filename):
    """Get an EncodingChecker instance for a given filename."""
    path = data_dir / filename
    with path.open("r", encoding="utf-8") as f:
        code = f.read()
    tree = ast.parse(code, filename=filename)
    return EncodingChecker(tree)


def test_version():
    assert __version__ == "0.1.0"


@pytest.mark.parametrize(
    "filename, return_code, expected_stdout, expected_stderr",
    [
        (
            "open_without_encoding.py",
            1,
            bytes("stdin:1:6: {}\n".format(FEN001_MSG), encoding="ascii"),
            b"",
        ),
        ("open_with_encoding.py", 0, b"", b""),
    ],
)
def test_stdin(filename, return_code, expected_stdout, expected_stderr):
    """Test that Flake8 correctly reads our plugin through stdin."""
    path = data_dir / filename
    with path.open("rb") as f:
        p = subprocess.Popen(
            ["flake8", "--select=FEN", "-"],
            stdin=f,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        actual_stdout, actual_stderr = p.communicate()
    assert p.returncode == return_code
    assert expected_stdout == actual_stdout
    assert expected_stderr == actual_stderr


@pytest.mark.parametrize(
    "filename, expected_errors",
    [
        ("open_without_encoding.py", [(1, 5, FEN001_MSG, EncodingChecker)]),
        ("open_with_encoding.py", []),
        ("open_with_positional_encoding.py", []),
        ("open_with_filename_only.py", [(1, 5, FEN001_MSG, EncodingChecker)]),
        ("open_with_encoding_and_default_mode.py", []),
        ("open_binary.py", []),
        ("open_binary_with_named_mode.py", []),
        ("open_method.py", []),
        ("open_with_bad_mode_type.py", []),
        ("open_with_bad_encoding_type.py", []),
        (
            "two_open_errors.py",
            [(2, 9, FEN001_MSG, EncodingChecker), (6, 5, FEN001_MSG, EncodingChecker)],
        ),
    ],
)
def test_all_rules(filename, expected_errors):
    """Test all of the rules."""
    checker = get_checker(filename)
    actual_errors = list(checker.run())
    assert expected_errors == sorted(actual_errors)
