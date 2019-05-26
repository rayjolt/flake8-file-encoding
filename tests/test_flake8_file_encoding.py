import subprocess
from pathlib import Path

import pytest

from flake8_file_encoding import __version__


current_dir = Path(__file__, "..").resolve()
data_dir = current_dir / "data"


def test_version():
    assert __version__ == '0.1.0'


@pytest.mark.parametrize("filename, return_code, expected_stdout, expected_stderr", [
    ("open_without_encoding.py", 1, b'stdin:1:6: FEN001 open() called without an encoding argument\n', b''),
    ("open_with_encoding.py", 0, b'', b''),
])
def test_stdin(filename, return_code, expected_stdout, expected_stderr):
    path = data_dir / filename
    with path.open("rb") as f:
        p = subprocess.Popen(['flake8', '--select=FEN', "-"], stdin=f,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        actual_stdout, actual_stderr = p.communicate()
    assert p.returncode == return_code
    assert expected_stdout == actual_stdout
    assert expected_stderr == actual_stderr
